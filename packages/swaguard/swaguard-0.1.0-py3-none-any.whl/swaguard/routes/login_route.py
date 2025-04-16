from typing import Optional
from fastapi import APIRouter, Request, Response, Form, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel

from ..config import config
from ..core.auth import authenticate_user, create_auth_cookie, authenticate_google_user


class LoginForm(BaseModel):
    username: str
    password: str


def create_login_router() -> APIRouter:
    """
    로그인 및 로그아웃 라우트를 포함하는 FastAPI 라우터를 생성합니다.
    
    Returns:
        FastAPI APIRouter 객체
    """
    router = APIRouter()
    
    @router.get(config.get("swaguard_login_path", "/swaguard/login"), response_class=HTMLResponse, include_in_schema=False)
    async def login_page(request: Request, next: Optional[str] = None):
        """로그인 페이지를 제공합니다."""
        # Google OAuth 정보 가져오기
        client_id = config.get("swaguard_oauth_google_client_id", "")
        redirect_uri = config.get("swaguard_oauth_google_redirect_uri", "")
        auth_type = config.get("swaguard_auth_type", "password")  # 기본값은 password
        
        # UI 정보 가져오기
        title = config.get("swaguard_title", "Swaguard")
        description = config.get("swaguard_description", "API 문서 보안 시스템")
        contact_name = config.get("swaguard_contact_name", "")
        contact_email = config.get("swaguard_contact_email", "")
        contact_url = config.get("swaguard_contact_url", "")
        
        # Google OAuth URL 생성
        google_oauth_url = ""
        if client_id and redirect_uri and auth_type != "password":
            # Google OAuth URL 생성
            google_oauth_url = (
                f"https://accounts.google.com/o/oauth2/v2/auth"
                f"?client_id={client_id}"
                f"&redirect_uri={redirect_uri}"
                f"&response_type=code"
                f"&scope=email profile"
                f"&prompt=select_account"
            )
            if next:
                google_oauth_url += f"&state={next}"
        
        # 인증 방식에 따른 UI 조정
        password_disabled = "disabled" if auth_type == "google" else ""
        google_button_hidden = "display: none;" if auth_type == "password" else ""
        password_form_hidden = "display: none;" if auth_type == "google" else ""
        
        # 로그인 양식 선택 스크립트
        auth_selection_script = ""
        if auth_type == "both":
            auth_selection_script = """
            function selectAuthMethod(method) {
                document.getElementById('password-form').style.display = method === 'password' ? 'block' : 'none';
                document.getElementById('google-button').style.display = method === 'google' ? 'block' : 'none';
                document.getElementById('auth-selector').style.display = 'none';
                document.getElementById('back-button').style.display = 'block';
            }
            
            function resetAuthSelection() {
                document.getElementById('password-form').style.display = 'none';
                document.getElementById('google-button').style.display = 'none';
                document.getElementById('auth-selector').style.display = 'block';
                document.getElementById('back-button').style.display = 'none';
            }
            """
        
        login_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title} - 로그인</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --primary-color: #4285F4;
                    --primary-hover: #357ae8;
                    --secondary-color: #34A853;
                    --secondary-hover: #2E7D32;
                    --error-color: #EA4335;
                    --warning-color: #FBBC05;
                    --text-color: #202124;
                    --text-secondary: #5f6368;
                    --background-color: #f8f9fa;
                    --card-background: #ffffff;
                    --border-color: #dadce0;
                    --shadow-color: rgba(60, 64, 67, 0.3);
                }}
                
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    font-family: 'Roboto', Arial, sans-serif;
                    background-color: var(--background-color);
                    color: var(--text-color);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .login-container {{
                    background-color: var(--card-background);
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px 0 rgba(60, 64, 67, 0.3), 0 4px 8px 3px rgba(60, 64, 67, 0.15);
                    width: 100%;
                    max-width: 400px;
                }}
                
                .login-header {{
                    text-align: center;
                    margin-bottom: 24px;
                }}
                
                .login-header h1 {{
                    font-size: 24px;
                    font-weight: 500;
                    color: var(--text-color);
                    margin-bottom: 8px;
                }}
                
                .login-header p {{
                    font-size: 14px;
                    color: var(--text-secondary);
                    margin-bottom: 16px;
                }}
                
                .login-header .contact-info {{
                    font-size: 12px;
                    color: var(--text-secondary);
                }}
                
                .form-group {{
                    margin-bottom: 16px;
                }}
                
                label {{
                    display: block;
                    margin-bottom: 8px;
                    font-size: 14px;
                    font-weight: 500;
                    color: var(--text-color);
                }}
                
                input {{
                    width: 100%;
                    padding: 12px;
                    border: 1px solid var(--border-color);
                    border-radius: 4px;
                    font-size: 16px;
                    transition: border-color 0.2s;
                }}
                
                input:focus {{
                    outline: none;
                    border-color: var(--primary-color);
                    box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
                }}
                
                button {{
                    background-color: var(--secondary-color);
                    color: white;
                    border: none;
                    padding: 12px 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 14px;
                    font-weight: 500;
                    letter-spacing: 0.25px;
                    transition: background-color 0.2s, box-shadow 0.2s;
                }}
                
                button:hover {{
                    background-color: var(--secondary-hover);
                    box-shadow: 0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
                }}
                
                .error-message {{
                    color: var(--error-color);
                    margin-top: 16px;
                    text-align: center;
                    font-size: 14px;
                }}
                
                .auth-button {{
                    margin-bottom: 12px;
                }}
                
                .back-btn {{
                    background-color: var(--text-secondary);
                    margin-top: 16px;
                }}
                
                .back-btn:hover {{
                    background-color: #4a4f55;
                }}
                
                .auth-option-title {{
                    text-align: center;
                    margin-bottom: 16px;
                    font-size: 16px;
                    font-weight: 500;
                }}
                
                .divider {{
                    display: flex;
                    align-items: center;
                    margin: 20px 0;
                }}
                
                .divider::before, .divider::after {{
                    content: "";
                    flex: 1;
                    border-bottom: 1px solid var(--border-color);
                }}
                
                .divider span {{
                    padding: 0 10px;
                    font-size: 12px;
                    color: var(--text-secondary);
                }}
                
                /* Google 버튼 스타일 */
                .gsi-material-button {{
                    -moz-user-select: none;
                    -webkit-user-select: none;
                    -ms-user-select: none;
                    -webkit-appearance: none;
                    background-color: #FFFFFF;
                    background-image: none;
                    border: 1px solid #747775;
                    -webkit-border-radius: 20px;
                    border-radius: 20px;
                    -webkit-box-sizing: border-box;
                    box-sizing: border-box;
                    color: #1f1f1f;
                    cursor: pointer;
                    font-family: 'Roboto', arial, sans-serif;
                    font-size: 14px;
                    height: 40px;
                    letter-spacing: 0.25px;
                    outline: none;
                    overflow: hidden;
                    padding: 0 12px;
                    position: relative;
                    text-align: center;
                    transition: background-color 0.01s, border-color 0.01s, box-shadow 0.01s;
                    vertical-align: middle;
                    white-space: nowrap;
                    width: auto;
                    max-width: 400px;
                    min-width: min-content;
                }}

                .gsi-material-button .gsi-material-button-icon {{
                    height: 20px;
                    margin-right: 12px;
                    min-width: 20px;
                    width: 20px;
                }}

                .gsi-material-button .gsi-material-button-content-wrapper {{
                    -webkit-align-items: center;
                    align-items: center;
                    display: flex;
                    -webkit-flex-direction: row;
                    flex-direction: row;
                    -webkit-flex-wrap: nowrap;
                    flex-wrap: nowrap;
                    height: 100%;
                    justify-content: space-between;
                    position: relative;
                    width: 100%;
                }}

                .gsi-material-button .gsi-material-button-contents {{
                    -webkit-flex-grow: 1;
                    flex-grow: 1;
                    font-family: 'Roboto', arial, sans-serif;
                    font-weight: 500;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    vertical-align: top;
                }}

                .gsi-material-button .gsi-material-button-state {{
                    -webkit-transition: opacity .218s;
                    transition: opacity .218s;
                    bottom: 0;
                    left: 0;
                    opacity: 0;
                    position: absolute;
                    right: 0;
                    top: 0;
                }}

                .gsi-material-button:disabled {{
                    cursor: default;
                    background-color: #ffffff61;
                    border-color: #1f1f1f1f;
                }}

                .gsi-material-button:disabled .gsi-material-button-contents {{
                    opacity: 38%;
                }}

                .gsi-material-button:disabled .gsi-material-button-icon {{
                    opacity: 38%;
                }}

                .gsi-material-button:not(:disabled):active,
                .gsi-material-button:not(:disabled):focus {{
                    background-color: #f1f1f1;
                }}

                .gsi-material-button:not(:disabled):active .gsi-material-button-state, 
                .gsi-material-button:not(:disabled):focus .gsi-material-button-state {{
                    background-color: #f1f1f1;
                    opacity: 1; 
                }}

                .gsi-material-button:not(:disabled):hover {{
                    background-color: #f1f1f1;
                    -webkit-box-shadow: 0 1px 2px 0 rgba(60, 64, 67, .30), 0 1px 3px 1px rgba(60, 64, 67, .15);
                    box-shadow: 0 1px 2px 0 rgba(60, 64, 67, .30), 0 1px 3px 1px rgba(60, 64, 67, .15);
                    transition: background-color 0.01s;
                }}

                .gsi-material-button:not(:disabled):hover .gsi-material-button-state {{
                    background-color: #f1f1f1;
                    opacity: 1;
                }}
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="login-header">
                    <h1>{title}</h1>
                    <p>{description}</p>
                    {f'<div class="contact-info">' if contact_name or contact_email or contact_url else ''}
                    {f'<div>{contact_name}</div>' if contact_name else ''}
                    {f'<div><a href="mailto:{contact_email}">{contact_email}</a></div>' if contact_email else ''}
                    {f'<div><a href="{contact_url}" target="_blank">{contact_url}</a></div>' if contact_url else ''}
                    {f'</div>' if contact_name or contact_email or contact_url else ''}
                </div>
                
                <!-- 인증 방식 선택 (auth_type이 both일 때) -->
                <div id="auth-selector" style="{'display: block;' if auth_type == 'both' else 'display: none;'}">
                    <button class="auth-button" onclick="selectAuthMethod('password')">비밀번호로 로그인</button>
                    <button class="gsi-material-button" onclick="selectAuthMethod('google')" style="width: 100%; margin-top: 12px;">
                        <div class="gsi-material-button-state"></div>
                        <div class="gsi-material-button-content-wrapper">
                            <div class="gsi-material-button-icon">
                                <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="display: block;">
                                    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                                    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                                    <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                                    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                                    <path fill="none" d="M0 0h48v48H0z"></path>
                                </svg>
                            </div>
                            <span class="gsi-material-button-contents">Google로 로그인</span>
                        </div>
                    </button>
                </div>
                
                <!-- 뒤로 가기 버튼 (인증 방식 선택으로 돌아가기) -->
                <div id="back-button" style="{'display: none;' if auth_type == 'both' else 'display: none;'}">
                    <button class="back-btn" onclick="resetAuthSelection()">뒤로 가기</button>
                </div>
                
                <!-- 비밀번호 로그인 폼 -->
                <form id="password-form" method="post" style="{password_form_hidden if auth_type == 'google' else 'display: none;' if auth_type == 'both' else ''}">
                    <div class="form-group">
                        <label for="username">사용자 이름:</label>
                        <input type="text" id="username" name="username" required {password_disabled}>
                    </div>
                    <div class="form-group">
                        <label for="password">비밀번호:</label>
                        <input type="password" id="password" name="password" required {password_disabled}>
                    </div>
                    <input type="hidden" name="next" value="{next or '/docs'}">
                    <button type="submit" {password_disabled}>로그인</button>
                </form>
                
                <!-- Google 로그인 버튼 -->
                <div id="google-button" style="{google_button_hidden if auth_type == 'both' else google_button_hidden}">
                    <a href="{google_oauth_url}" style="text-decoration: none; display: block; width: 100%;">
                        <button class="gsi-material-button" type="button" style="width: 100%;">
                            <div class="gsi-material-button-state"></div>
                            <div class="gsi-material-button-content-wrapper">
                                <div class="gsi-material-button-icon">
                                    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="display: block;">
                                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
                                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                                        <path fill="none" d="M0 0h48v48H0z"></path>
                                    </svg>
                                </div>
                                <span class="gsi-material-button-contents">Google로 로그인</span>
                            </div>
                        </button>
                    </a>
                </div>
                
                <div id="error-message" class="error-message"></div>
            </div>
            <script>
                // URL에서 에러 메시지 파라미터 가져오기
                const urlParams = new URLSearchParams(window.location.search);
                const error = urlParams.get('error');
                if (error) {{
                    document.getElementById('error-message').textContent = decodeURIComponent(error);
                }}
                
                {auth_selection_script}
                
                // auth_type이 both이면 초기 화면에서 선택 UI만 표시
                {f"if ('{auth_type}' === 'both') {{ resetAuthSelection(); }}" if auth_type == 'both' else ""}
            </script>
        </body>
        </html>
        """
        
        return HTMLResponse(content=login_html)
    
    @router.post(config.get("swaguard_login_path", "/swaguard/login"), include_in_schema=False)
    async def login(
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
        next: str = Form("/docs")
    ):
        """비밀번호 로그인 요청을 처리합니다."""
        # 사용자 인증
        if not authenticate_user(username, password):
            # 인증 실패 시 오류 메시지와 함께 로그인 페이지로 리다이렉트
            login_path = config.get("swaguard_login_path", "/swaguard/login")
            error_message = "Invalid username or password"
            redirect_url = f"{login_path}?error={error_message}"
            if next and next != "/docs":
                redirect_url += f"&next={next}"
            return RedirectResponse(redirect_url, status_code=303)
        
        # 인증 성공 시 쿠키 생성
        cookie_value, cookie_options = create_auth_cookie(username)
        
        # 쿠키 설정
        cookie_name = config.get("swaguard_cookie_name", "swaguard_auth")
        response = RedirectResponse(next, status_code=303)
        response.set_cookie(
            key=cookie_name,
            value=cookie_value,
            httponly=True,
            secure=cookie_options["secure"] == "true",
            samesite=cookie_options["samesite"],
            path="/",
            max_age=int(cookie_options["max-age"])
        )
        
        return response
    
    @router.get("/oauth/google/callback", include_in_schema=False)
    async def google_oauth_callback(
        code: str = Query(...),
        state: Optional[str] = Query(None),
        error: Optional[str] = Query(None)
    ):
        """Google OAuth 콜백을 처리합니다."""
        login_path = config.get("swaguard_login_path", "/swaguard/login")
        next_url = state or "/docs"
        
        # 에러가 있으면 로그인 페이지로 리다이렉트
        if error:
            redirect_url = f"{login_path}?error={error}"
            if state:
                redirect_url += f"&next={state}"
            return RedirectResponse(redirect_url, status_code=303)
        
        # Google 인증 코드로 사용자 정보 얻기
        user_info = await authenticate_google_user(code)
        if not user_info:
            redirect_url = f"{login_path}?error=Failed to authenticate with Google"
            if state:
                redirect_url += f"&next={state}"
            return RedirectResponse(redirect_url, status_code=303)
        
        # 쿠키 생성 (이메일을 사용자 이름으로 사용)
        username = user_info.get("email")
        cookie_value, cookie_options = create_auth_cookie(username)
        
        # 쿠키 설정
        cookie_name = config.get("swaguard_cookie_name", "swaguard_auth")
        response = RedirectResponse(next_url, status_code=303)
        response.set_cookie(
            key=cookie_name,
            value=cookie_value,
            httponly=True,
            secure=cookie_options["secure"] == "true",
            samesite=cookie_options["samesite"],
            path="/",
            max_age=int(cookie_options["max-age"])
        )
        
        return response
    
    @router.get(config.get("swaguard_logout_path", "/swaguard/logout"))
    async def logout():
        """로그아웃 요청을 처리합니다."""
        # 쿠키 삭제
        cookie_name = config.get("swaguard_cookie_name", "swaguard_auth")
        json_response = JSONResponse(
            content={"message": "Logged out successfully. Please refresh the page."},
            status_code=200
        )
        json_response.delete_cookie(
            key=cookie_name,
            path="/",
            secure=config.get("swaguard_cookie_secure", True),
            httponly=config.get("swaguard_cookie_httponly", True)
        )
        
        return json_response
    
    return router
