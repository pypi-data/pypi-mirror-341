# gpushare

Python client for the GPU Share service.</br>

Note: Before start using this library, Please make sure to login to our service <a href="https://gpushare.srimanhq.com" class="btn btn-primary">
  GPUShare
</a> and get your API key and logins ready.</br>

## Installation
```bash
pip install gpushare
```
pypi library <a href="https://pypi.org/project/gpushare/" class="btn btn-primary">
  gpushare
</a>
## Quickstart
```python
from gpushare import GPUShareClient, AuthenticationError, APIError

client = GPUShareClient("https://gpushare.srimanhq.com")

# 1. Authenticate (OTP flow):
client.login("you@example.com", "yourpassword", "8bit string")
# then enter the OTP when prompted

# or, if you already have a token:
client.set_api_token("YOUR_API_TOKEN")

# 2. Pick a GPU
client.select_gpu(1)

# 3. Execute code
output = client.execute_code("print('Hello from GPU!')")
print(output)
```


## API Reference
### Authentication
<strong>login(email: str, password: str, random_token: str, mode: str = "user"):</strong></br>
Starts the OTP login flow, sending an OTP to your email/device.

```python
client.login("you@example.com", "pass123", "AbCd1234")
# prompts for OTP, then calls verify_otp() internally
```

<strong>verify_otp(email: str, otp: str):</strong></br>
Complete OTP verification and retrieve your API token.

```python
client.verify_otp("you@example.com", "123456")
```

<strong>get_api_token():</strong></br>
Fetch a new token directly from the web endpoint (parses HTML).

```python
client.get_api_token()
```

<strong>set_api_token(token: str):</strong></br>
Manually set a pre‑obtained API token.

```python
client.set_api_token("YOUR_API_TOKEN")
```

## Token Management

<strong>get_token_info() -> dict:</strong></br>
Returns { created_at, expires_at, revoked }
```python
info = client.get_token_info()
print(info["expires_at"])
```

<strong>refresh_token() -> dict:</strong></br>
Extend token expiry; returns the new token and expiry.
```python
new_info = client.refresh_token()
print(new_info["token"], new_info["expires_at"])
```

<strong>kill_token():</strong></br>
Revoke the current API token.
```python
client.kill_token()
```

## GPU Selection & Roles
<strong>select_gpu(gpu_id: int):</strong></br>
Choose which GPU you want to control.
```python
client.select_gpu(2)
```

<strong>switch_mode(mode: str):</strong></br>
Switch your role ("user", "owner", "admin", "moderator"):</br>
currently moderator is not completely implemented i will update it soon :)
```python
client.switch_mode("owner")
```

## User Info
<strong>whoami() -> dict:</strong></br>
Get full session info (requires OTP if not authenticated).
```python
info = client.whoami()
```

<strong>whoami_quick(8bit_token: str) -> dict:</strong></br>
Quick lookup using your 8‑char token when you first logged in.
```python
info = client.whoami_quick("AbCd1234")
```

## GPU & Access APIs
<strong>list_available_gpus() -> list:</strong></br>
List all GPUs you can request, in your current mode.
```python
gpus = client.list_available_gpus()
```

<strong>get_gpu_detail() -> dict | None:</strong></br>
Fetch metadata for the selected GPU.
```python
detail = client.get_gpu_detail()
```

<strong>request_access(code: str = None) -> dict:</strong></br>
Request access to the GPU (if not already a user).
```python
resp = client.request_access(code="Please grant access")
```

<strong>get_my_requests() -> list:</strong></br>
List your own pending/approved/denied requests.
```python
my_reqs = client.get_my_requests()
```

<strong>approve_request(req_id: int) -> dict:</strong></br>
Approve someone’s request (owner/admin only). For this you have to change set_mode() to owner as i have to open sourced the server side code yet, you guys cant use the admin mode. Soon, i will open-source.
```python
client.approve_request(42)
```

<strong>deny_request(req_id: int) -> dict:</strong></br>
denying someone’s request (owner/admin only). For this too you have to change set_mode() to owner.
```python
client.deny_request(43)
```

<strong>revoke_access(request_id: int) -> dict:</strong></br>
Revoke a granted access (owner/admin/user).
```python
client.revoke_access(10)
```

<strong>set_gpu_idle(idle: bool) -> dict:</strong></br>
Mark the GPU idle or busy (owner only). Must set mode to owner not even admin can change it to idle. You must be in owner mode to operate this.
```python
client.set_gpu_idle(True)   # mark idle
client.set_gpu_idle(False)  # mark active
```

## Code Review & Execution

<strong>download_reviewed_code(review_id: int, dest_path: str):</strong></br>
Download a reviewed code bundle to disk. Currently broken, did a oopsie. will fix it.
```python
client.download_reviewed_code(123, "reviewed.py")
```

<strong>run_reviewed_code(review_id: int) -> str:</strong></br>
Execute a previously reviewed code snippet. Currently broken.
```python
output = client.run_reviewed_code(123)
```

<strong>execute_code(code: str) -> str:</strong></br>
Send arbitrary Python to run on the GPU. GPU is either have to be previously approved by owner or should be owner to run this part.
```python
out = client.execute_code("for i in range(3): print(i)")
print(out)
```

<strong>run_file(filepath: str) -> str:</strong></br>
Read a local .py file and execute its contents remotely. GPU is either have to be previously approved by owner or should be owner to run this part.
```python
out = client.run_file("script.py")
```

# Admin Dashboard
## Curently unavailable for anybody until open-sourced
<strong>get_admin_dashboard() -> dict:</strong></br>
Fetch global stats (admin mode only).
```python
dashboard = client.get_admin_dashboard()
```


# Error Handling
<strong>All methods will raise one of:</strong></br></br>

* AuthenticationError (login/token issues)</br></br>

* AuthorizationError (permission errors)</br></br>

* APIError (other API failures)</br></br>
```python
from gpushare import AuthenticationError, AuthorizationError, APIError

try:
    client.select_gpu(1)
except APIError as e:
    print("API error:", e)
```

Currently only support Windows and RTX only Tested and remaining lack of resources to test.</br></br>
you can download the host agent for windows from the link below:</br>
<a href="https://cloud.srimanhq.com/index.php/s/8wKYeNRn2pQriG2" class="btn btn-primary">
  Download Host Agent
</a></br></br>
Download the archive, extract it, and navigate to the dist folder. Run the gpu_agent_gui app to start the host agent (currently only tested on Windows with RTX and Quadro GPUs; other GPUs have not been tested due to lack of resources).</br></br>
you will download from a private cloud hosted at 'https://cloud.srimanhq.com' anyone in need for private cloud storage with good research idea can approach my [email](mailto:yalavarthisriman@gmail.com) to send why you need it and how much you need it. I will review it and make decision.</br></br>
you data will be safe and almost currently 95% uptime if natural disaster and 100% if informed for specific specific time. data is replicated using raid 1 redundant cause my wallet has issue :')</br></br>
Note: Everything I provide is service for community, Free of charge. Create, Contribute, Communicate.</br></br>
Please make sure to [email](mailto:yalavarthisriman@gmail.com) me any bugs or not properly coded endpoints. Also, Please do understand i am only human, i might have made critical mistakes. I made sure that the Access to your gpu as safe as possible and you, only you can access the GPU until you approve it to your friends or partners, not even admin or i can access without you accepting it. At the end you have the power to do anything with your APIs.</br></br>
<b> YOU HAVE THE FREEDOM TO DO ANYTHING.</b></br></br>
your gentle feedback & suggestions is much appreciated ;)</br>

# License
Not yet Licenced by MIT :<
