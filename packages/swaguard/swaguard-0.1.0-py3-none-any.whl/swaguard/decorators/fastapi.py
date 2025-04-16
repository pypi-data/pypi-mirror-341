from typing import Callable, Optional, List
from functools import wraps

from fastapi import Request, HTTPException
from fastapi.security import APIKeyCookie

from ..config import config
from ..core.auth import verify_auth_cookie


def get_cookie_name() -> str:
    """인증 쿠키 이름을 가져옵니다."""
    return config.get("cookie_name", "swaguard_auth")


# 쿠키 기반 인증을 위한 의존성
cookie_scheme = APIKeyCookie(name=get_cookie_name())

def swagger_protect(paths: Optional[List[str]] = None):
    """
    Swagger UI 및 관련 경로를 보호하는 데코레이터
    
    Args:
        paths: 보호할 추가 경로 목록 (기본값 외에 추가로 보호할 경로)
        
    Example:
        @app.get("/docs")
        @swagger_protect()
        async def get_swagger_ui():
            ...
    """
    # 경로 목록이 제공되면 보호 대상 경로에 추가
    if paths:
        for path in paths:
            config.add_protected_path(path)
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # FastAPI의 Request 객체를 찾아 인증 수행
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request and 'request' in kwargs:
                request = kwargs['request']
            
            if not request:
                raise ValueError("Request object not found in function arguments")
            
            # 쿠키 검증
            cookie_name = get_cookie_name()
            cookie = request.cookies.get(cookie_name)
            
            if not cookie:
                raise HTTPException(status_code=401, detail="Unauthorized: Authentication required")
            
            username = verify_auth_cookie(cookie)
            if not username:
                raise HTTPException(status_code=401, detail="Unauthorized: Invalid or expired token")
            
            # 인증 성공 시 원래 함수 실행
            return await func(*args, **kwargs)
        
        return wrapper
    
    return decorator
