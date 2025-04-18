# gpushare/client.py
import os
import getpass
import re
import requests
from datetime import datetime
from .exceptions import (
    GPUShareError, AuthenticationError, AuthorizationError, APIError
)
import base64

class GPUShareClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self.authenticated = False
        self.gpu_id = None
        self.mode = "user"
        self.allowed_roles = []

    # --------------------
    # Authentication
    # --------------------

    def login(self, email: str, password: str, random_token: str, mode: str = "user"):
        """
        Initiate login with email, password, and the 8‑char random_token.
        Server will send an OTP to the user's email or device.
        """

        def prompt_for_otp(prompt="Enter OTP (6 digits): ", attempts=3, length=6):
            """
            Prompt the user to enter their OTP securely, validate format,
            and allow a limited number of retries.
            """
            for i in range(attempts):
                # Use getpass to avoid echoing the OTP
                otp = getpass.getpass(prompt)
                if not otp:
                    print("No input received.")
                elif not re.fullmatch(rf"\d{{{length}}}", otp):
                    print(f"Invalid format. Please enter exactly {length} digits.")
                else:
                    return otp
                remaining = attempts - i - 1
                if remaining:
                    print(f"{remaining} attempt{'s' if remaining>1 else ''} remaining.\n")
            raise AuthenticationError("Failed to provide a valid OTP after multiple attempts.")

        if mode not in ("user","owner","admin","moderator"):
            raise ValueError("Mode must be one of user, owner, admin, moderator.")
        self.mode = mode

        url = f"{self.base}/api/login"
        r = self.session.post(url, json={
            "email": email,
            "password": password,
            "random_token": random_token
        })
        data = self._parse_response(r)

        # Expecting server to return something like {"otp_required": true}
        if not data.get("otp_required"):
            raise AuthenticationError("Login failed.")
        print("OTP sent to your email: {email}")
        print("you will need to enter otp to complete login.")
        otp = prompt_for_otp()
        self.verify_otp(email=email, otp=otp)


    def verify_otp(self, email, otp: str):
        """
        Complete login by verifying the OTP you received.
        On success, server returns an API token.
        """
        url = f"{self.base}/api/verify_otp"
        r = self.session.post(url, json={"email": email, "otp": otp})
        data = self._parse_response(r)
        token = data.get("api_token")
        if not token:
            raise AuthenticationError("OTP verification failed.")
        self.token = token
        self.authenticated = True
        print("Login successful; API token set.")

    def get_api_token(self):
        url = f"{self.base}/get_api_token"
        r = self.session.get(url)
        if r.status_code != 200:
            raise APIError("Failed to get API token")
        m = re.search(r"<pre.*?>([\w\-\._~\+/=]+)</pre>", r.text)
        if not m:
            raise APIError("API token not found in response")
        self.token = m.group(1)
        self.authenticated = True
        print("API token acquired.")

    def set_api_token(self, token: str):
        """
        Directly set a pre‑obtained API token. 
        Bypass login/OTP flow.
        """
        if not token or not isinstance(token, str):
            raise AuthenticationError("API token must be a non‑empty string.")
        self.token = token
        self.authenticated = True
        print("API token set; you are now authenticated.")

    # --------------------
    # Internal Helpers
    # --------------------

    def _auth_headers(self):
        if not self.token:
            raise AuthenticationError("No API token; call get_api_token() first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _parse_response(self, r: requests.Response):
        if not r.ok:
            # Try to extract JSON error
            try:
                err = r.json().get("error", r.text)
            except Exception:
                err = r.text or f"HTTP {r.status_code}"
            raise APIError(err)
        ct = r.headers.get("Content-Type", "")
        if "application/json" in ct:
            return r.json()
        return r.text

    # --------------------
    # Role & GPU Selection
    # --------------------

    def select_gpu(self, gpu_id: int):
        if not self.authenticated:
            raise AuthenticationError("Authenticate before selecting a GPU.")
        self.gpu_id = gpu_id
        url = f"{self.base}/api/gpu_roles/{gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        data = self._parse_response(r)
        self.allowed_roles = data.get("roles", [])
        print("Allowed roles:", self.allowed_roles)

    def switch_mode(self, mode: str):
        if mode not in self.allowed_roles:
            raise AuthorizationError(f"You do not have role '{mode}' for GPU {self.gpu_id}")
        self.mode = mode
        print("Switched mode to:", mode)

    def whoami(self):
        """
        If not authenticated, requires otp to complete login.
        Returns user/session info.
        """
        if not self.token:
            if otp is None:
                raise AuthenticationError("No API token. Call whoami(otp) with the 8‑char OTP.")
            # Complete login with stored creds
            self.login(self._email, self._password, otp, self.mode)

        # Now we have token
        url = f"{self.base}/api/whoami"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)
    
    def whoami_quick(self, random_token: str):
        """
        Quick whoami using the 8‑char random_token (no login required).
        """

        if not random_token or len(random_token) != 8:
            raise APIError("random_token must be an 8‑character string.")
        url = f"{self.base}/api/whoami_quick/{random_token}"
        r = self.session.get(url,  headers=self._auth_headers())
        data = self._parse_response(r)
        return data


    # --------------------
    # GPU & Access APIs
    # --------------------

    def list_available_gpus(self):
        url = f"{self.base}/api/available_gpus?mode={self.mode}"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def get_gpu_detail(self):
        """
        Fetch metadata for the selected GPU.
        Returns a dict on success, or None if the endpoint returns 404.
        """
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/gpu_detail/{self.gpu_id}"
        r = self.session.get(url, headers=self._auth_headers())
        if r.status_code == 404:
            # Endpoint missing or no access: return None
            return None
        return self._parse_response(r)

    def request_access(self, code: str = None):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/request_gpu/{self.gpu_id}"
        payload = {}
        if code:
            payload["code"] = code
        r = self.session.post(url, headers=self._auth_headers(), json=payload)
        return self._parse_response(r)

    def get_my_requests(self):
        url = f"{self.base}/api/my_requests"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def approve_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot approve in current mode.")
        url = f"{self.base}/api/approve_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    def deny_request(self, req_id: int):
        if self.mode not in ("owner","admin","moderator"):
            raise AuthorizationError("Cannot deny in current mode.")
        url = f"{self.base}/api/deny_request/{req_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    def revoke_access(self, request_id: int):
        if self.mode not in ("owner","admin","user"):
            raise AuthorizationError("Cannot revoke in current mode.")
        url = f"{self.base}/api/revoke_access/{request_id}"
        r = self.session.post(url, headers=self._auth_headers())
        return self._parse_response(r)

    def set_gpu_idle(self, idle: bool):
        """
        If in owner mode, mark the selected GPU as idle or busy.
        """
        if self.mode != "owner":
            raise AuthorizationError("Only owners can set GPU idle status.")
        if self.gpu_id is None:
            raise APIError("No GPU selected.")

        url = f"{self.base}/api/set_gpu_idle/{self.gpu_id}"
        r = self.session.post(
            url,
            headers=self._auth_headers(),
            json={"idle": idle}
        )
        return self._parse_response(r)

    # --------------------
    # Code Review & Execution
    # --------------------

    def download_reviewed_code(self, review_id: int, dest_path: str):
        url = f"{self.base}/api/download_review/{review_id}"
        r = self.session.get(url, headers=self._auth_headers(), stream=True)
        if r.status_code != 200:
            raise APIError("Failed to download reviewed code.")
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"Review {review_id} downloaded to {dest_path}")

    def run_reviewed_code(self, review_id: int):
        url = f"{self.base}/api/run_reviewed_code/{review_id}"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)

    def execute_code(self, code: str):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        r = self.session.post(url, headers=self._auth_headers(), json={"code": code})
        data = self._parse_response(r)
        if isinstance(data, dict) and "output" in data:
            return data["output"]
        return data
    
    # --------------------
    # Token Management
    # --------------------

    '''def get_token_info(self):
        """
        Returns a dict with:
          - issued_at: ISO8601 string
          - expires_at: ISO8601 string
        """
        if not self.token:
            raise AuthenticationError("No API token set.")
        url = f"{self.base}/api/token_info"
        r = self.session.get(url, headers=self._auth_headers())
        data = self._parse_response(r)
        return data'''
    
    def get_token_info(self):
        """
        Returns a dict with:
          - issued_at: ISO8601 string
          - expires_at: ISO8601 string
        """
        if not self.token:
            raise AuthenticationError("No API token set.")
        url = f"{self.base}/api/token_info"
        data = self._parse_response(self.session.get(url, headers=self._auth_headers()))
        return {
            "created_at": data["created_at"],
            "expires_at": data["expires_at"],
            "revoked": data["revoked"]
        }
        
    def refresh_token(self):
        """
        Requests the server to extend your token's expiry.
        Returns the new token and expiry.
        """
        if not self.token:
            raise AuthenticationError("No API token to refresh.")
        url = f"{self.base}/api/refresh_token"
        r = self.session.post(url, headers=self._auth_headers())
        data = self._parse_response(r)
        new_token = data.get("token")
        if not new_token:
            raise APIError("Server did not return a new token.")
        self.token = new_token
        print("API token refreshed; new expiry:", data.get("expires_at"))
        return data

    def kill_token(self):
        """
        Revokes the current API token so it can no longer be used.
        """
        if not self.token:
            raise AuthenticationError("No API token to revoke.")
        url = f"{self.base}/api/revoke_token"
        r = self.session.post(url, headers=self._auth_headers())
        self._parse_response(r)
        print("API token revoked.")
        self.token = None
        self.authenticated = False


    # --------------------
    # Admin Dashboard
    # --------------------

    def get_admin_dashboard(self):
        if self.mode != "admin":
            raise AuthorizationError("Only admin mode can access dashboard.")
        url = f"{self.base}/api/admin_dashboard"
        r = self.session.get(url, headers=self._auth_headers())
        return self._parse_response(r)


    def execute_code(self, code: str):
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")
        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        r = self.session.post(url, headers=self._auth_headers(), json={"code": code})
        data = self._parse_response(r)
        # If JSON, expect an "output" key; otherwise, return raw text
        if isinstance(data, dict) and "output" in data:
            return data["output"]
        return data.get("output", data)


    def run_file(self, filepath: str):
        """
        Read a local .py file, send it to the GPU, and execute.
        Returns the execution output.
        """
        if self.gpu_id is None:
            raise APIError("Select a GPU first.")

        if not os.path.isfile(filepath):
            raise APIError(f"File not found: {filepath}")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            raise APIError(f"Failed to read file: {e}")

        if not code.strip():
            raise APIError("File is empty.")

        return self.execute_code(code)
        '''with open(filepath, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        url = f"{self.base}/api/execute_code/{self.gpu_id}"
        payload = {
            "filename": os.path.basename(filepath),
            "file_data": b64
        }
        r = self.session.post(url, headers=self._auth_headers(), json=payload)
        data = self._parse_response(r)
        # data could be dict with "output" or text
        return data.get("output") if isinstance(data, dict) else data'''
