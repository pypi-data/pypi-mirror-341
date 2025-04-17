import requests
import os
from dotenv import load_dotenv

# Load environment variables if using .env file
load_dotenv()

class Config:
    # Use environment variables if available, otherwise use hardcoded values
    SUPABASE_CLIENT_ID = os.getenv("SUPABASE_CLIENT_ID", "17b95e33-baee-425e-bf85-db5669c4d571")
    SUPABASE_CLIENT_SECRET = os.getenv("SUPABASE_CLIENT_SECRET", "sba_81ea66ebb5754cd43476c67bd1bb3701529c5146")

def refresh_token(refresh_token):
    """
    Refresh a Supabase access token using a refresh token
    
    Args:
        refresh_token (str): The refresh token to use
        
    Returns:
        dict: The response containing the new access token and refresh token
    """
    refresh_url = "https://api.supabase.com/v1/oauth/token"
    
    payload = (f"grant_type=refresh_token&client_id={Config.SUPABASE_CLIENT_ID}&"
               f"client_secret={Config.SUPABASE_CLIENT_SECRET}&refresh_token={refresh_token}")
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(refresh_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing token: {e}")
        return None

if __name__ == "__main__":
    # Get refresh token from command line or environment variable
    user_refresh_token = input("Enter your Supabase refresh token: ")
    
    if not user_refresh_token:
        print("No refresh token provided. Exiting.")
        exit(1)
    
    # Refresh the token
    result = refresh_token(user_refresh_token)
    
    if result:
        print("\nToken refresh successful!")
        print(f"Access Token: {result.get('access_token')}")
        print(f"Refresh Token: {result.get('refresh_token')}")
        print(f"Token Type: {result.get('token_type')}")
        print(f"Expires In: {result.get('expires_in')} seconds")
    else:
        print("Token refresh failed.")


# {'access_token': 'sbp_oauth_f4964a7bcad7b2345566461a0a47934d5a3a99f5', 'refresh_token': 'CBAcFQdUAzCEAfdopK', 'expires_in': 86400, 'token_type': 'Bearer'}