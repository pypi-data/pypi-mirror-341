import argparse
import atexit
import json
import logging
import os
import tempfile

import httplib2
import pydantic
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from oauth2client.client import (
    Credentials,
    FlowExchangeError,
    OAuth2Credentials,
    flow_from_clientsecrets,
)

# Add this global variable at the module level after imports
_memory_credentials_storage = {}

# Global vars to track temp files for cleanup
_temp_files = []


def _cleanup_temp_files():
    """Clean up temporary files at exit"""
    global _temp_files
    for file_path in _temp_files:
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logging.warning(f"Failed to delete temporary file {file_path}: {e}")


# Register cleanup function
atexit.register(_cleanup_temp_files)


def should_use_memory_storage() -> bool:
    import os

    return os.environ.get("GSUITE_USE_MEMORY_STORAGE", "").lower() == "true"


def get_gauth_file() -> str:
    import os

    oauth_config = os.environ.get("GSUITE_OAUTH_CONFIG")
    if oauth_config:
        # Create a temporary file with the contents of the environment variable
        try:
            # Validate the JSON structure
            json.loads(oauth_config)
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as temp:
                temp.write(oauth_config)
                _temp_files.append(temp.name)  # Add to cleanup list
                return temp.name
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in GSUITE_OAUTH_CONFIG: {e}")
            # Fall back to file-based configuration

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gauth-file",
        type=str,
        default="./.gauth.json",
        help="Path to client secrets file",
    )
    args, _ = parser.parse_known_args()
    return args.gauth_file


CLIENTSECRETS_LOCATION = get_gauth_file()

REDIRECT_URI = "http://localhost:4100/code"
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive"
]


class AccountInfo(pydantic.BaseModel):

    email: str
    account_type: str
    extra_info: str

    def __init__(self, email: str, account_type: str, extra_info: str = ""):
        super().__init__(email=email, account_type=account_type, extra_info=extra_info)

    def to_description(self):
        return f"""Account for email: {self.email} of type: {self.account_type}. Extra info for: {self.extra_info}"""


def get_accounts_file() -> str:
    import os

    accounts_config = os.environ.get("GSUITE_ACCOUNTS_CONFIG")
    if accounts_config:
        # Create a temporary file with the contents of the environment variable
        try:
            # Parse and validate the JSON accounts array
            accounts_array = json.loads(accounts_config)
            if not isinstance(accounts_array, list):
                raise ValueError("GSUITE_ACCOUNTS_CONFIG must be a JSON array")

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False
            ) as temp:
                accounts_dict = {"accounts": accounts_array}
                json.dump(accounts_dict, temp)
                _temp_files.append(temp.name)  # Add to cleanup list
                return temp.name
        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Invalid JSON in GSUITE_ACCOUNTS_CONFIG: {e}")
            # Fall back to file-based configuration

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--accounts-file",
        type=str,
        default="./.accounts.json",
        help="Path to accounts configuration file",
    )
    args, _ = parser.parse_known_args()
    return args.accounts_file


def get_account_info() -> list[AccountInfo]:
    accounts_file = get_accounts_file()
    with open(accounts_file) as f:
        data = json.load(f)
        accounts = data.get("accounts", [])
        return [AccountInfo.model_validate(acc) for acc in accounts]


class GetCredentialsException(Exception):
    """Error raised when an error occurred while retrieving credentials.

    Attributes:
      authorization_url: Authorization URL to redirect the user to in order to
                         request offline access.
    """

    def __init__(self, authorization_url):
        """Construct a GetCredentialsException."""
        self.authorization_url = authorization_url


class CodeExchangeException(GetCredentialsException):
    """Error raised when a code exchange has failed."""


class NoRefreshTokenException(GetCredentialsException):
    """Error raised when no refresh token has been found."""


class NoUserIdException(Exception):
    """Error raised when no user ID could be retrieved."""


def get_credentials_dir() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credentials-dir",
        type=str,
        default=".",
        help="Directory to store OAuth2 credentials",
    )
    args, _ = parser.parse_known_args()
    return args.credentials_dir


def _get_credential_filename(user_id: str) -> str:
    creds_dir = get_credentials_dir()
    return os.path.join(creds_dir, f".oauth2.{user_id}.json")


def get_stored_credentials(user_id: str) -> OAuth2Credentials | None:
    """Retrieved stored credentials for the provided user ID.

    Args:
    user_id: User's ID.
    Returns:
    Stored oauth2client.client.OAuth2Credentials if found, None otherwise.
    """
    global _memory_credentials_storage

    # Check if we should use memory storage
    if should_use_memory_storage():
        if user_id in _memory_credentials_storage:
            return _memory_credentials_storage[user_id]
        return None

    try:
        cred_file_path = _get_credential_filename(user_id=user_id)
        if not os.path.exists(cred_file_path):
            logging.warning(
                f"No stored Oauth2 credentials yet at path: {cred_file_path}"
            )
            return None

        with open(cred_file_path, "r") as f:
            data = f.read()
            return Credentials.new_from_json(data)
    except Exception as e:
        logging.error(e)
        return None

    raise None


def store_credentials(credentials: OAuth2Credentials, user_id: str):
    """Store OAuth 2.0 credentials in the specified directory."""
    global _memory_credentials_storage

    # Check if we should use memory storage
    if should_use_memory_storage():
        _memory_credentials_storage[user_id] = credentials
        return

    cred_file_path = _get_credential_filename(user_id=user_id)
    os.makedirs(os.path.dirname(cred_file_path), exist_ok=True)

    data = credentials.to_json()
    with open(cred_file_path, "w") as f:
        f.write(data)


def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                        credentials.
    Returns:
    oauth2client.client.OAuth2Credentials instance.
    Raises:
    CodeExchangeException: an error occurred.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, " ".join(SCOPES))
    flow.redirect_uri = REDIRECT_URI
    try:
        credentials = flow.step2_exchange(authorization_code)
        return credentials
    except FlowExchangeError as error:
        logging.error("An error occurred: %s", error)
        raise CodeExchangeException(None)


def get_user_info(credentials):
    """Send a request to the UserInfo API to retrieve the user's information.

    Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
    Returns:
    User information as a dict.
    """
    user_info_service = build(
        serviceName="oauth2", version="v2", http=credentials.authorize(httplib2.Http())
    )
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    if user_info and user_info.get("id"):
        return user_info
    else:
        raise NoUserIdException()


def get_authorization_url(email_address, state):
    """Retrieve the authorization URL.

    Args:
    email_address: User's e-mail address.
    state: State for the authorization URL.
    Returns:
    Authorization URL to redirect the user to.
    """
    flow = flow_from_clientsecrets(
        CLIENTSECRETS_LOCATION, " ".join(SCOPES), redirect_uri=REDIRECT_URI
    )
    flow.params["access_type"] = "offline"
    flow.params["approval_prompt"] = "force"
    flow.params["user_id"] = email_address
    flow.params["state"] = state
    return flow.step1_get_authorize_url(state=state)


def get_credentials(authorization_code, state):
    """Retrieve credentials using the provided authorization code.

    This function exchanges the authorization code for an access token and queries
    the UserInfo API to retrieve the user's e-mail address.
    If a refresh token has been retrieved along with an access token, it is stored
    in the application database using the user's e-mail address as key.
    If no refresh token has been retrieved, the function checks in the application
    database for one and returns it if found or raises a NoRefreshTokenException
    with the authorization URL to redirect the user to.

    Args:
    authorization_code: Authorization code to use to retrieve an access token.
    state: State to set to the authorization URL in case of error.
    Returns:
    oauth2client.client.OAuth2Credentials instance containing an access and
    refresh token.
    Raises:
    CodeExchangeError: Could not exchange the authorization code.
    NoRefreshTokenException: No refresh token could be retrieved from the
                                available sources.
    """
    email_address = ""
    try:
        credentials = exchange_code(authorization_code)
        user_info = get_user_info(credentials)
        import json

        logging.error(f"user_info: {json.dumps(user_info)}")
        email_address = user_info.get("email")

        if credentials.refresh_token is not None:
            store_credentials(credentials, user_id=email_address)
            return credentials
        else:
            credentials = get_stored_credentials(user_id=email_address)
            if credentials and credentials.refresh_token is not None:
                return credentials
    except CodeExchangeException as error:
        logging.error("An error occurred during code exchange.")
        # Drive apps should try to retrieve the user and credentials for the current
        # session.
        # If none is available, redirect the user to the authorization URL.
        error.authorization_url = get_authorization_url(email_address, state)
        raise error
    except NoUserIdException:
        logging.error("No user ID could be retrieved.")
        # No refresh token has been retrieved.
    authorization_url = get_authorization_url(email_address, state)
    raise NoRefreshTokenException(authorization_url)


def get_token_file() -> str:
    """Get the token file path from command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token-file",
        type=str,
        default=None,
        help="Path to pre-authenticated token file",
    )
    parser.add_argument(
        "--use-stored-token",
        action="store_true",
        help="Use pre-authenticated token instead of browser flow",
    )
    args, _ = parser.parse_known_args()
    return args.token_file, args.use_stored_token


def load_token_from_file(token_file: str) -> OAuth2Credentials:
    """Load OAuth credentials from a token file."""
    try:
        with open(token_file, 'r') as f:
            token_data = json.load(f)
            
            # Create OAuth2Credentials from token data
            credentials = OAuth2Credentials(
                access_token=token_data.get('access_token', ''),
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                refresh_token=token_data['refresh_token'],
                token_expiry=None,  # Will be refreshed automatically when needed
                token_uri=token_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
                user_agent=None,
                revoke_uri=None,
                id_token=None,
                token_response=None,
                scopes=SCOPES,
                token_info_uri=None
            )
            
            # Refresh the token to ensure it's valid
            if credentials.access_token_expired:
                http = httplib2.Http()
                credentials.refresh(http)
                
            return credentials
    except Exception as e:
        logging.error(f"Error loading token from file: {e}")
        return None


def get_credentials_non_interactive(email_address: str) -> OAuth2Credentials:
    """Get credentials without requiring browser interaction."""
    token_file, use_stored_token = get_token_file()
    
    if use_stored_token and token_file and os.path.exists(token_file):
        # Load credentials from token file
        credentials = load_token_from_file(token_file)
        if credentials:
            logging.info(f"Successfully loaded credentials from token file for {email_address}")
            return credentials
    
    # Try to get stored credentials
    credentials = get_stored_credentials(user_id=email_address)
    if credentials and credentials.refresh_token is not None:
        logging.info(f"Using stored credentials for {email_address}")
        return credentials
    
    # If we get here, we couldn't get credentials non-interactively
    logging.error("No valid credentials found and interactive authentication not available")
    return None


def authenticate(email_address: str = None):
    """Authenticate with Google, first trying non-interactive, then interactive."""
    # Check for skip-auth flag
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-auth",
        action="store_true",
        help="Skip authentication completely (for testing)",
    )
    args, _ = parser.parse_known_args()
    if args.skip_auth:
        logging.warning("Authentication skipped due to --skip-auth flag")
        return None
    
    token_file, use_stored_token = get_token_file()
    
    # Try to get an account email if not provided
    if not email_address:
        try:
            accounts = get_account_info()
            if accounts:
                email_address = accounts[0].email
            else:
                email_address = "user@example.com"
        except Exception as e:
            logging.error(f"Error getting account info: {e}")
            email_address = "user@example.com"
    
    # Try non-interactive first if requested
    if use_stored_token:
        credentials = get_credentials_non_interactive(email_address)
        if credentials:
            return credentials
        else:
            if token_file:
                logging.error(f"Token file specified ({token_file}) but could not be used for authentication")
                return None
    
    # If we get here, we need interactive authentication
    # Check if we can use browser authentication
    if "GSUITE_SKIP_BROWSER_AUTH" in os.environ and os.environ["GSUITE_SKIP_BROWSER_AUTH"].lower() == "true":
        logging.error("Browser authentication skipped due to GSUITE_SKIP_BROWSER_AUTH=true")
        return None
    
    # Get stored credentials first
    credentials = get_stored_credentials(user_id=email_address)
    if credentials and not credentials.access_token_expired:
        return credentials
    
    # Generate the authorization URL
    auth_url = get_authorization_url(email_address, "interactive")
    print("\n===== AUTHORIZATION REQUIRED =====")
    print(f"Open this URL in your browser: {auth_url}")
    print("After authorization, you'll be redirected to a page with a code.")
    print("Copy that code and paste it below.")
    
    # Wait for user to input the code
    auth_code = input("Enter the authorization code: ")
    
    # Exchange the code for credentials
    try:
        credentials = exchange_code(auth_code)
        user_info = get_user_info(credentials)
        user_email = user_info.get('email')
        
        if credentials.refresh_token is not None:
            store_credentials(credentials, user_id=user_email)
            print(f"Successfully authenticated as {user_email}")
            print(f"Credentials saved.")
            return credentials
        else:
            print("Warning: No refresh token received. Authentication may not persist.")
            return credentials
    except Exception as e:
        logging.error(f"Error during authorization: {e}")
        raise