###
import requests
from User.user_schema import SocialMember

import jwt
from datetime import datetime, timedelta, timezone

GOOGLE_CLIENT_ID = "30161074278-idj5eof64nb5hv3tfat6btggtb7lei4c.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_REDIRECT_URI = "http://localhost:8000/user/googlelogin"

def oauth_google(code : str):
    try:
        token_url = f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_REDIRECT_URI}"

        token_response = requests.post(token_url)

        # Access token 요청 실패 시 에러 처리
        if token_response.status_code != 200:
            raise Exception(f"Failed to fetch access token: {token_response.status_code}, {token_response.text}")

        # Access token 추출
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        if not access_token:
            raise Exception("Access token not found in response")

        # google에 회원 정보 요청
        user_info_url = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
        user_response = requests.get(user_info_url)

        # 사용자 정보 요청 실패 시 에러 처리
        if user_response.status_code != 200:
            raise Exception(f"Failed to fetch user info: {user_response.status_code}, {user_response.text}")

        # 사용자 정보 추출
        info = user_response.json()
        print("---------------------------------------------------")
        print(info)
        print("---------------------------------------------------")
        return SocialMember(
            name=info.get('name'),
            email=info.get('email'),
        )

    except Exception as e:
        # 에러 로그를 출력하여 문제를 추적할 수 있도록 상세 메시지 출력
        print(f"Error in Google OAuth process: {str(e)}")
        raise Exception("Google OAuth error")
    


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