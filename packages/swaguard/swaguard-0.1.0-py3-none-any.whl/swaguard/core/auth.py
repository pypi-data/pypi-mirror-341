import time
import os
import json
import csv
import logging
from typing import Dict, Optional, Tuple, Any, Callable

import httpx

from ..config import config
from .security import verify_password, create_signed_value, verify_signed_value


# 기본적으로 환경 변수나 설정 파일에서 가져오지 않았다면 랜덤 시크릿 키 생성
SECRET_KEY = os.environ.get("SWAGUARD_SECRET_KEY", "")
if not SECRET_KEY:
    from .security import generate_secret_key
    SECRET_KEY = generate_secret_key()


def load_users_from_csv() -> Dict[str, str]:
    """
    CSV 파일에서 사용자 정보를 로드합니다.
    CSV 파일 형식: username,password
    
    Returns:
        사용자 이름과 비밀번호 해시의 딕셔너리
    """
    users = {}
    csv_path = config.get("swaguard_users_csv_path", "")
    
    if not csv_path or not os.path.exists(csv_path):
        return users
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # 헤더 건너뛰기
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    username = row[0].strip()
                    password = row[1].strip()
                    if username and password:
                        # 비밀번호를 해시하지 않고 그대로 저장 (인증 시 해시 처리)
                        users[username] = password
    except Exception as e:
        logging.error(f"CSV 파일에서 사용자 로드 중 오류 발생: {e}")
    
    return users


def authenticate_user(username: str, password: str) -> bool:
    """
    사용자를 인증합니다.
    
    Args:
        username: 사용자 이름
        password: 비밀번호
        
    Returns:
        인증 성공 시 True, 실패 시 False
    """
    # 인증 타입이 'google'인 경우 비밀번호 인증 거부
    if config.get("swaguard_auth_type") == "google":
        return False
    
    # 먼저 설정에서 사용자 확인
    users = config.get_users()
    if username in users:
        stored_password_hash = users[username]
        return verify_password(password, stored_password_hash)
    
    # CSV 파일에서 사용자 확인
    csv_users = load_users_from_csv()
    if username in csv_users:
        stored_password = csv_users[username]
        # CSV에서는 평문 비밀번호를 저장하므로 직접 비교
        return password == stored_password
    
    return False


async def authenticate_google_user(auth_code: str) -> Optional[Dict[str, Any]]:
    """
    Google OAuth 인증 코드를 사용하여 사용자를 인증합니다.
    
    Args:
        auth_code: Google에서 받은 인증 코드
        
    Returns:
        인증 성공 시 사용자 정보 딕셔너리, 실패 시 None
    """
    # 인증 타입이 'password'인 경우 Google 인증 거부
    if config.get("swaguard_auth_type") == "password":
        return None
        
    # Google OAuth 설정 가져오기
    client_id = config.get("swaguard_oauth_google_client_id")
    client_secret = config.get("swaguard_oauth_google_client_secret")
    redirect_uri = config.get("swaguard_oauth_google_redirect_uri")
    
    if not all([client_id, client_secret, redirect_uri]):
        logging.error("Google OAuth 설정이 완료되지 않았습니다.")
        return None
    
    try:
        # 액세스 토큰 요청
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": auth_code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                }
            )
            
            if token_response.status_code != 200:
                logging.error(f"Google OAuth 토큰 요청 실패: {token_response.text}")
                return None
                
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                return None
            
            # 사용자 정보 요청
            user_response = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                logging.error(f"Google 사용자 정보 요청 실패: {user_response.text}")
                return None
                
            user_info = user_response.json()
            
            # 사용자 검증 콜백 함수 호출
            validator_func = config.get("swaguard_oauth_user_validator")
            if validator_func and callable(validator_func):
                if not validator_func(user_info):
                    logging.warning(f"사용자 검증 실패: {user_info.get('email')}")
                    return None
            
            return user_info
            
    except Exception as e:
        logging.error(f"Google OAuth 인증 처리 중 오류 발생: {str(e)}")
        return None


def create_auth_cookie(username: str) -> Tuple[str, Dict[str, str]]:
    """
    인증 쿠키를 생성합니다.
    
    Args:
        username: 인증된 사용자 이름
        
    Returns:
        (쿠키 값, 쿠키 설정 옵션) 튜플
    """
    # 현재 시간과 만료 시간 계산
    now = int(time.time())
    expires = now + (config.get("swaguard_cookie_expire_minutes", 60) * 60)
    
    # 쿠키 데이터 생성
    cookie_data = {
        "sub": username,  # subject (사용자)
        "iat": now,       # issued at (발급 시간)
        "exp": expires,   # expiration (만료 시간)
    }
    
    # 서명된 쿠키 값 생성
    cookie_value = create_signed_value(SECRET_KEY, cookie_data)
    
    # 쿠키 설정 옵션
    cookie_options = {
        "httponly": str(config.get("swaguard_cookie_httponly", True)).lower(),
        "secure": str(config.get("swaguard_cookie_secure", True)).lower(),
        "samesite": config.get("swaguard_cookie_samesite", "lax"),
        "path": "/",
        "max-age": str(config.get("swaguard_cookie_expire_minutes", 60) * 60),
    }
    
    return cookie_value, cookie_options


def verify_auth_cookie(cookie_value: Optional[str]) -> Optional[str]:
    """
    인증 쿠키를 확인합니다.
    
    Args:
        cookie_value: 쿠키 값 문자열
        
    Returns:
        쿠키가 유효하면 사용자 이름, 그렇지 않으면 None
    """
    if not cookie_value:
        return None
        
    data = verify_signed_value(SECRET_KEY, cookie_value)
    if not data:
        return None
        
    # 쿠키에서 사용자 이름 추출
    return data.get("sub")


def is_path_protected(path: str) -> bool:
    """
    주어진 경로가 보호되어야 하는지 확인합니다.
    
    Args:
        path: 확인할 경로
        
    Returns:
        경로가 보호되어야 하면 True, 그렇지 않으면 False
    """
    protected_paths = config.get("swaguard_protected_paths", [])
    return any(path.startswith(protected) for protected in protected_paths)
