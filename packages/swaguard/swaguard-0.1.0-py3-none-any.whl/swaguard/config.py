import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class SwaguardConfig:
    """
    Swaguard 라이브러리의 설정을 관리하는 클래스
    환경 변수 또는 YAML 설정 파일에서 설정을 로드합니다.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SwaguardConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        # 기본 설정값
        self.config = {
            "swaguard_cookie_name": "swaguard_auth",
            "swaguard_cookie_expire_minutes": 60,
            "swaguard_cookie_secure": True,
            "swaguard_cookie_httponly": True,
            "swaguard_cookie_samesite": "lax",
            "swaguard_login_path": "/swaguard/login",
            "swaguard_logout_path": "/swaguard/logout",
            "swaguard_users": {},  # 빈 사용자 목록으로 시작
            "swaguard_protected_paths": ["/docs", "/redoc", "/openapi.json"],
            # Google OAuth 설정
            "swaguard_oauth_google_client_id": "",
            "swaguard_oauth_google_client_secret": "",
            "swaguard_oauth_google_redirect_uri": "",
            "swaguard_oauth_user_validator": None,  # Google 사용자 정보 검증 콜백 함수
            "swaguard_auth_type": "password",  # 'password', 'google', 'both' 중 선택
            # UI 설정
            "swaguard_title": "Swaguard",
            "swaguard_description": "API 문서 보안 시스템",
            "swaguard_contact_name": "",
            "swaguard_contact_email": "",
            "swaguard_contact_url": "",
            # 사용자 관리 설정
            "swaguard_users_csv_path": "",
            # 필수 설정 값 목록
            "swaguard_required_settings": ["swaguard_auth_type"],
        }
        
        # 환경 변수에서 설정 로드
        self._load_from_env()
        
        # 설정 파일이 있으면 로드
        config_file = os.environ.get("SWAGUARD_CONFIG_FILE", "swaguard_config.yaml")
        if Path(config_file).exists():
            self._load_from_file(config_file)
            
        self._initialized = True

    def _load_from_env(self):
        """환경 변수에서 설정을 로드합니다."""
        env_mappings = {
            "SWAGUARD_COOKIE_NAME": ("swaguard_cookie_name", str),
            "SWAGUARD_COOKIE_EXPIRE_MINUTES": ("swaguard_cookie_expire_minutes", int),
            "SWAGUARD_COOKIE_SECURE": ("swaguard_cookie_secure", lambda x: x.lower() == "true"),
            "SWAGUARD_COOKIE_HTTPONLY": ("swaguard_cookie_httponly", lambda x: x.lower() == "true"),
            "SWAGUARD_COOKIE_SAMESITE": ("swaguard_cookie_samesite", str),
            "SWAGUARD_LOGIN_PATH": ("swaguard_login_path", str),
            "SWAGUARD_LOGOUT_PATH": ("swaguard_logout_path", str),
            "SWAGUARD_AUTH_TYPE": ("swaguard_auth_type", str),
            "SWAGUARD_OAUTH_GOOGLE_CLIENT_ID": ("swaguard_oauth_google_client_id", str),
            "SWAGUARD_OAUTH_GOOGLE_CLIENT_SECRET": ("swaguard_oauth_google_client_secret", str),
            "SWAGUARD_OAUTH_GOOGLE_REDIRECT_URI": ("swaguard_oauth_google_redirect_uri", str),
        }
        
        for env_var, (config_key, converter) in env_mappings.items():
            if env_var in os.environ:
                self.config[config_key] = converter(os.environ[env_var])

    def _load_from_file(self, file_path: str):
        """YAML 설정 파일에서 설정을 로드합니다."""
        try:
            with open(file_path, "r") as f:
                file_config = yaml.safe_load(f)
                if file_config and isinstance(file_config, dict):
                    self.config.update(file_config)
        except Exception as e:
            print(f"설정 파일 로드 중 오류 발생: {e}")

    def add_user(self, username: str, password_hash: str):
        """사용자를 추가합니다."""
        self.config["swaguard_users"][username] = password_hash

    def remove_user(self, username: str):
        """사용자를 제거합니다."""
        if username in self.config["swaguard_users"]:
            del self.config["swaguard_users"][username]

    def get(self, key: str, default: Any = None) -> Any:
        """설정값을 가져옵니다."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """설정값을 설정합니다."""
        self.config[key] = value

    def get_users(self) -> Dict[str, str]:
        """등록된 사용자 목록을 가져옵니다."""
        return self.config.get("swaguard_users", {})

    def add_protected_path(self, path: str):
        """보호할 경로를 추가합니다."""
        if path not in self.config["swaguard_protected_paths"]:
            self.config["swaguard_protected_paths"].append(path)

    def is_configured(self) -> bool:
        """필수 설정이 모두 구성되었는지 확인합니다."""
        required_settings = self.config.get("swaguard_required_settings", [])
        for setting in required_settings:
            value = self.config.get(setting)
            if value is None or (isinstance(value, str) and value == ""):
                return False
        return True

    def save_to_file(self, file_path: Optional[str] = None):
        """설정을 파일에 저장합니다."""
        if file_path is None:
            file_path = os.environ.get("SWAGUARD_CONFIG_FILE", "swaguard_config.yaml")
        
        try:
            with open(file_path, "w") as f:
                yaml.dump(self.config, f)
        except Exception as e:
            print(f"설정 파일 저장 중 오류 발생: {e}")


# 싱글톤 인스턴스를 만들어서 import시 바로 사용할 수 있도록 합니다.
config = SwaguardConfig()
