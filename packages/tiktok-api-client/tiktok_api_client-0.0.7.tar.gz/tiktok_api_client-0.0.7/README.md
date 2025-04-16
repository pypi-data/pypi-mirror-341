# TikTok Open API Client

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This Python library provides a convenient way to interact with the TikTok Open API for authorization and publishing video and photo content. It handles the OAuth 2.0 authorization flow with PKCE, and offers methods for posting videos (from file or URL) and photos.

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Getting Started](#getting-started)
    * [Basic Usage](#basic-usage)
    * [Posting a Video from a URL](#posting-a-video-from-a-url)
    * [Posting a Photo](#posting-a-photo)
* [Class Overview](#class-overview)
    * [`TikTok(client_key, client_secret, redirect_uri, state="", scopes=None)`](#tiktokclient_key-client_secret-redirect_uri-state-scopesnone)
    * [Methods](#methods)
* [Available Scopes](#available-scopes)
* [Error Handling](#error-handling)
* [Contributing](#contributing)
* [License](#license)

## Features

* **OAuth 2.0 Authorization:** Implements the PKCE (Proof Key for Code Exchange) flow for secure authentication.
* **Token Management:** Handles exchanging authorization codes for access tokens, refreshing access tokens, and revoking access tokens.
* **Video Posting:** Supports uploading video files in chunks and posting videos from a URL.
* **Photo Posting:** Enables creating and publishing photo posts with various options.
* **Creator Information:** Allows fetching information about the authenticated TikTok creator.
* **Upload Status:** Provides a way to check the status of video uploads.
* **Error Handling:** Includes custom exceptions for timeout and HTTP errors.
* **Configurable Scopes:** Allows specifying the required TikTok API scopes.

## Installation

You can install the library using pip:

```bash
pip install tiktok-api-client
```


## Getting Started

To use this library, you'll need to obtain the following credentials from your TikTok developer portal:

- **Client Key**
- **Client Secret**
- **Redirect URI** (This URI must be registered in your TikTok developer portal)

## Basic Usage

Here's a basic example of how to initialize the TikTok client and get the authorization URL:

```python
from tiktok-api-client import TikTok

CLIENT_KEY = "YOUR_CLIENT_KEY"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "YOUR_REDIRECT_URI"
STATE = "your_optional_state" # this could be a dict or string that can be used to track the authentication in your REDIRECT endpoint

tik = TikTok(client_key=CLIENT_KEY, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, state=STATE, scopes = [])
#tik = TikTok(client_key="ryjhrhrthrthr", client_secret="dfdbfbfbrtrbtbrtbrtbrt", redirect_uri="https://your-app-url.comp/callback", state={'user_id':'user1', 'name': 'hello'}, scopes=["video.publish", "user.info.basic"])

"""
this are the available scopes
SCOPES = [
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats",
]
"""

auth_url = tik.get_authorization_url()

# Sample Response: https://www.tiktok.com/v2/auth/authorize/?client_key=sbaw0y8rutbd9qx3i1&response_type=code&scope=video.publish&redirect_uri=https%3A%2F%2Fyour-app-url.comp%2Fcallback&code_challenge=zzq1--trJ8aXxqsddsdsdsdrWCaatTBx4&state=%7B%27user_id%27%3A+%mami%27%2C+%name%27%3A+%27hello%27%7D&code_challenge_method=S256'
# visit the endpoint to authentiicate Tiktok on the browser

print(f"Authorize URL: {auth_url}")
```

NOTE: the auth generated a code verifier earlier stored in tik.code_verifier, ensure you store this code verifier along with your states as it will be used to verify the authentication, you can aswell save records in the database that you can query in the callback.
After the user authorizes your application and is redirected back to your `REDIRECT_URI` with an authorization code, you can exchange it for an access token:
the response in your callback response will be like this:

{'code': '9xmQgPZMUTvILmosta-4eC-PXLGFRgjdzXspg2ybTc2AKGDtJU5p6ry2w7wMTejt3jZr4bS0x0z-kOgG655eyX1duD4Ts7I4WE9PqYuZDt_olDm-JxvR-kkP5yc4SryRIqSVUd8doY5ZrmRrN2ODekSPd2LPnuIVj6S9Hi_PTpv2NB4KBLOkoEgsATCCdSiYXdrGZBQ5XBm6c-R2LELM3BdDDMHn2dVWu3OKRRBOHW2Q7ql3iWV1w3sqNpAaHTG7QO9vagKfa-3iFoZtQ51WTw*0!4993.e1', 'scopes': 'user.info.basic,video.publish', 'state': "{'user_id': 'user1', 'name': 'hello'}"}

extract the code.

```python


authorization_code = '9xmQgPZMUTvILmosta-4eC-PXLGFRgjdzXspg2ybTc2AKGDtJU5p6ry2w7wMTejt3jZr4bS0x0z-kOgG655eyX1duD4Ts7I4WE9PqYuZDt_olDm-JxvR-kkP5yc4SryRIqSVUd8doY5ZrmRrN2ODekSPd2LPnuIVj6S9Hi_PTpv2NB4KBLOkoEgsATCCdSiYXdrGZBQ5XBm6c-R2LELM3BdDDMHn2dVWu3OKRRBOHW2Q7ql3iWV1w3sqNpAaHTG7QO9vagKfa-3iFoZtQ51WTw*0!4993.e1'

in the below code, tik.code_verifier will be used to verify the code, ensure you stored it earlier as you will reinitialize Tiktok since your session may or instance may have been lost in the call back or continue if youre testing on terminal

tik = TikTok
tik = TikTok(client_key="ryjhrhrthrthr", client_secret="dfdbfbfbrtrbtbrtbrtbrt", redirect_uri="https://your-app-url.comp/callback", state={'user_id':'user1', 'name': 'hello'}, scopes=["video.publish", "user.info.basic"])
tik.code_verifier = code_verifier # if you reinitialzed the instance, fetch teh stored code_verifier

try:
    token_data = tik.exchange_code_for_token(code=authorization_code)
    print("Access Token:", token_data.get("access_token"))
    print("Refresh Token:", token_data.get("refresh_token"))
except Exception as e:
    print(f"Error exchanging code for token: {e}")
```

The token_data response is as below:
{'access_token': 'act.UD0znPSOyqFgRJVvF9Tr2Xc5bJYjOnRiGPpsvNxb1TX42nWnSY8J51FTdZxl!4964.e1',
 'expires_in': 86400,
 'open_id': '-000bMhnTFeW4SZCPZkPWZppArDnsFgvOa_f',
 'refresh_expires_in': 31536000,
 'refresh_token': 'rft.BDkTqoVTZZm9kLAtll3Rf2JQq5vwlvy9XR3KvbQEIMi6GgcDCtAWA9NJCP1h!5033.e1',
 'scope': 'user.info.basic,video.publish',
 'token_type': 'Bearer'}

this is stored in the tik object

store the access and refrsh token as it will be required for future authentication and refresh (use cron to refrsh hourly)

to refresh token
tik.refresh_access_token() or tik.refresh_access_token(refresh_token) #pass the token value if you reinitialized the instance, the response is same as token_data

### There are 2 methods for video and photo uploads
Direct Posting and Upload
- Direct will upload and publish for public view
- Upload save the video to draft

REQUIRED OPTIONS
title
source: FILE_UPLOAD, MEDIA_UPLOAD
upload_type: POST_VIDEO_FILE, 

## Direct Posting

```python
tik.init_post_video(title='hello', source='FILE_UPLOAD', upload_type="post_video_file", privacy_level="SELF_ONLY", video_path='/home/mymi14s/Desktop/development/v1.mp4')
# Optional parameters
# "disable_duet": False,
# "disable_comment": False,
# "disable_stitch": False,
# "video_cover_timestamp_ms": 1000

```

## Posting a Video from a URL

```python
access_token = "YOUR_ACCESS_TOKEN"  # Obtained from the authorization flow

payload = {
    "source_info": {
        "source": "PULL_FROM_URL",
        "video_url": "YOUR_VIDEO_URL"
    },
    "post_info": {
        "title": "My Awesome Video",
        "privacy_level": "PUBLIC",
        # Optional parameters
        # "disable_duet": False,
        # "disable_comment": False,
        # "disable_stitch": False,
        # "video_cover_timestamp_ms": 1000
    }
}

try:
    response = tiktok_client.post_video_url(payload)
    print("Video Post Response:", response)
except Exception as e:
    print(f"Error posting video: {e}")
```

## Posting a Photo

```python
access_token = "YOUR_ACCESS_TOKEN"

try:
    response = tiktok_client.create_photo(
        post_mode="DIRECT_POST",
        title="My Photo Post",
        privacy_level="PUBLIC",
        photo_images=["URL_TO_IMAGE_1", "URL_TO_IMAGE_2"],
        photo_cover_index=1,
        description="Check out my photos!",
        disable_comment=False,
        auto_add_music=False,
        access_token=access_token
    )
    print("Photo Post Response:", response)
except Exception as e:
    print(f"Error creating photo post: {e}")
```

## Class Overview

### `TikTok(client_key, client_secret, redirect_uri, state="", scopes=None)`

Initializes the TikTok API client.

- `client_key (str)`: Your TikTok application's client key.
- `client_secret (str)`: Your TikTok application's client secret.
- `redirect_uri (str)`: The redirect URI registered in your TikTok developer portal.
- `state (str, optional)`: Optional state parameter to prevent CSRF. Defaults to "".
- `scopes (list, optional)`: List of TikTok API scopes to request. Defaults to module-level SCOPES.

### Methods

- `get_authorization_url() -> str`
- `exchange_code_for_token(code: str, timeout: int = 10) -> dict`
- `refresh_access_token(refresh_token: str = None) -> dict`
- `revoke_access_token(access_token: str = None) -> dict`
- `get_creator_info(access_token: str = None) -> dict`
- `post_video_file(payload: dict) -> dict`
- `post_video_url(payload: dict) -> dict`
- `upload_video_file(payload: dict) -> dict`
- `create_photo(...) -> dict`
- `check_upload_status(...) -> dict`

## Available Scopes

```python
SCOPES = [
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats",
]
```

Pass a subset of these scopes to the `scopes` parameter when initializing the client.

## Error Handling

This library includes basic error handling. Expect the following:

- `TimeoutError` for request timeouts
- `Exception` for OAuth errors
- `HTTPError` (from utils.py) for HTTP issues

Always wrap operations in `try...except` blocks for reliability.

## Contributing

We welcome contributions! Please:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your fork.
5. Submit a pull request.

Ensure you follow coding style and include tests.

## License

MIT License. See `LICENSE` file for details.
