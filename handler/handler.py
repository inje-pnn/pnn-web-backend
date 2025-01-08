###
import requests
from User.user_schema import SocialMember
import jwt
from datetime import datetime, timedelta, timezone

GOOGLE_CLIENT_ID = "30161074278-idj5eof64nb5hv3tfat6btggtb7lei4c.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/user/googlelogin"

def oauth_google(code: str):
    token_url = f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_REDIRECT_URI}"

    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    try:
        # 1. Access Token 요청
        token_response = requests.post(token_url)

        if token_response.status_code != 200:
            raise Exception(f"Failed to fetch access token: {token_response.text}")

        token_json = token_response.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise Exception("Access token not found in response")

        # 2. 사용자 정보 요청
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = requests.get(user_info_url, headers=headers)
        if user_response.status_code != 200:
            raise Exception(f"User info fetch failed: {user_response.text}")

        user_json = user_response.json()
        user_json['id'] = user_json.get('id', 0)  # 기본값 설정
        user_json['verified_email'] = user_json.get('verified_email', False)
        return SocialMember(
            id=user_json.get('id'),
            name=user_json.get('name'),
            email=user_json.get('email'),
            verified_email=user_json.get('verified_email', False)
        )

    except Exception as e:
        print(f"Error in Google OAuth process: {e}")
        raise Exception(e)


ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = 'HS256'
JWT_SECRET_KEY = "guswlgns"+"rlaghdus"+"tlsdkdnf"+"whdnwn"+"qkqhemf"

def create_access_token(payload, expires_delta: timedelta | None = None):
    to_encode = {"sub": payload}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
