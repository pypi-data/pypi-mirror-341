import requests, urllib.parse, base64, hashlib, secrets
from typing import Optional, List
from .utils import (
    TimeoutError, HTTPError, get_file, handle_response
)


SCOPES = [
    "user.info.basic",
    "video.list",
    "video.upload",
    "video.publish",
    "user.info.profile",
    "user.info.stats",
]

class TikTok:
    """
    A class for interacting with the TikTok Open API for authorization and video/photo publishing.
    """
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
    TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
    TOKEN_REVOKE_URL = "https://open.tiktokapis.com/v2/oauth/revoke/"
    AUTH_SCOPE = ["video.publish"]
    VIDEO_POST_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    PHOTO_POST_URL = "https://open.tiktokapis.com/v2/post/publish/content/init/"

    def __init__(self, client_key: str, client_secret: str, redirect_uri: str, state: str = "", scopes: Optional[List[str]] = None):
        """
        Initializes the TikTok API client with necessary credentials and configurations.

        Args:
            client_key (str): The client key obtained from your TikTok developer portal.
            client_secret (str): The client secret obtained from your TikTok developer portal.
            redirect_uri (str): The redirect URI registered in your TikTok developer portal.
            state (str, optional): An optional state parameter to prevent cross-site request forgery. Defaults to "".
            scopes (Optional[List[str]], optional): A list of TikTok API scopes to request. Defaults to the module-level SCOPES.
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code_verifier = self._generate_code_verifier()
        self.state = state
        if scopes:
            for i in scopes:
                if i not in SCOPES:
                    raise ValueError(f"Invalid scope: {i}. Available scopes are: {SCOPES}")
            self.AUTH_SCOPE = scopes

    def _generate_code_verifier(self) -> str:
        """
        Generates a random code verifier string for the PKCE authorization flow.

        Returns:
            str: The generated code verifier.
        """
        return secrets.token_urlsafe(64)

    def _generate_code_challenge(self, verifier: str) -> str:
        """
        Generates a code challenge from the code verifier for the PKCE authorization flow.

        Args:
            verifier (str): The code verifier string.

        Returns:
            str: The generated code challenge.
        """
        digest = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip("=")

    def get_authorization_url(self) -> str:
        """
        Constructs the authorization URL for the TikTok OAuth flow.

        Returns:
            str: The authorization URL that the user should be redirected to.
        """
        code_challenge = self._generate_code_challenge(self.code_verifier)
        params = {
            "client_key": self.client_key,
            "response_type": "code",
            "scope": " ".join(self.AUTH_SCOPE),
            "redirect_uri": self.redirect_uri,
            "code_challenge": code_challenge,
            "state": self.state,
            "code_challenge_method": "S256"
        }
        return f"{self.AUTH_URL}?{urllib.parse.urlencode(params)}"

    def _make_oauth_request(self, url: str, data: dict, timeout: int = 10) -> dict:
        """
        Internal helper method to make POST requests for OAuth-related endpoints.

        Args:
            url (str): The URL to make the request to.
            data (dict): The data to send in the request body.
            timeout (int, optional): The request timeout in seconds. Defaults to 10.

        Returns:
            dict: The JSON response from the API.

        Raises:
            Exception: If the HTTP request fails.
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache"
        }
        try:
            response = requests.post(url, headers=headers, data=data, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"OAuth request failed: {e}")

    def exchange_code_for_token(self, code: str, timeout: int = 10) -> dict:
        """
        Exchanges the authorization code received from TikTok for an access token and refresh token.

        Args:
            code (str): The authorization code received in the redirect URI.
            timeout (int, optional): The request timeout in seconds. Defaults to 10.

        Returns:
            dict: A dictionary containing the access token, refresh token, and other token-related information.

        Raises:
            TimeoutError: If the request to the TikTok API times out.
            Exception: If the HTTP request fails for other reasons.
        """
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier,
        }
        try:
            response_data = self._make_oauth_request(self.TOKEN_URL, data, timeout=timeout)
            self.token_data = response_data
            return self.token_data
        except Exception as e:
            raise TimeoutError("TikTok OAuth request timed out") if "timed out" in str(e) else Exception(f"OAuth error: {e}")

    def refresh_access_token(self, refresh_token: str = None) -> dict:
        """
        Refreshes an expired access token using the refresh token.

        Args:
            refresh_token (str, optional): The refresh token. If not provided, it will try to use the refresh token stored in `self.token_data`. Defaults to None.

        Returns:
            dict: A dictionary containing the new access token, refresh token, and other token-related information.

        Raises:
            Exception: If no refresh token is available or if the refresh request fails.
        """
        if not refresh_token and not self.token_data.get("refresh_token"):
            raise Exception("No refresh token available")

        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token if refresh_token else self.token_data.get("refresh_token"),
        }
        self.token_data = self._make_oauth_request(self.TOKEN_URL, data)
        return self.token_data

    def revoke_access_token(self, access_token: str = None) -> dict:
        """
        Revokes an access token, making it invalid.

        Args:
            access_token (str, optional): The access token to revoke. If not provided, it will try to use the access token stored in `self.token_data`. Defaults to None.

        Returns:
            dict: The JSON response from the API indicating the success or failure of the revocation.

        Raises:
            Exception: If no access token is available or if the revocation request fails.
        """
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No access token available")

        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "token": access_token if access_token else self.token_data.get("access_token")
        }
        return self._make_oauth_request(self.TOKEN_REVOKE_URL, data)

    def get_creator_info(self, access_token: str = None) -> dict:
        """
        Retrieves information about the authenticated TikTok creator.

        Args:
            access_token (str, optional): The access token to use for the request. If not provided, it will try to use the access token stored in `self.token_data`. Defaults to None.

        Returns:
            dict: A dictionary containing the creator's information.

        Raises:
            Exception: If no access token is available or if the API request fails.
        """
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No access token available")
        url = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
        headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get("access_token")}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        try:
            response = requests.post(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"Request failed: {req_err}")

    def _upload_video_chunks(self, upload_url: str, video_data: list):
        """
        Internal helper method to upload video file chunks to the provided URL.

        Args:
            upload_url (str): The URL provided by the TikTok API to upload the video chunks.
            video_data (list): A list of dictionaries, where each dictionary contains 'content_range' and 'chunk_data'.
        """
        for chunk in video_data:
            response = requests.put(
                upload_url,
                headers={
                    "Content-Range": chunk['content_range'],
                    "Content-Type": "video/mp4"
                },
                data=chunk['chunk_data'],
                timeout=300
            )
            response.raise_for_status()

    def post_video_file(self, payload: dict) -> dict:
        """
        Initializes and uploads a video file to TikTok.

        Args:
            payload (dict): A dictionary containing the video post information and file data.
                             Expected keys include:
                               - 'file_data' (list): A list of dictionaries containing video chunks.
                               - 'title' (str): The title of the video.
                               - 'privacy_level' (str): The privacy level of the video ('PUBLIC', 'PRIVATE', 'FRIENDS').
                               - 'disable_duet' (bool, optional): Whether to disable duet for the video. Defaults to False.
                               - 'disable_comment' (bool, optional): Whether to disable comments for the video. Defaults to False.
                               - 'disable_stitch' (bool, optional): Whether to disable stitch for the video. Defaults to False.
                               - 'video_cover_timestamp_ms' (int, optional): The timestamp for the video cover in milliseconds. Defaults to 1000.

        Returns:
            dict: A dictionary containing the initial and final upload responses from the TikTok API.

        Raises:
            TimeoutError: If the request to the TikTok API times out.
            HTTPError: If the HTTP request fails.
        """
        try:
            video_data = payload.pop("file_data")
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload, timeout=10))
            initial_data = response
            self.initial_video_upload_response = initial_data

            self._upload_video_chunks(initial_data['data']['upload_url'], video_data)

            # Assuming a complete URL is provided in the initial response
            complete_url = initial_data['data'].get('complete_url')
            if complete_url:
                response = requests.get(complete_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                final_data = response.json()
                self.final_video_upload_response = final_data
            else:
                final_data = {"message": "Finalization URL not found, check initial response."} # Handle case where complete_url is missing

            self.video_response = {
                "initial_video_upload_response": initial_data,
                "final_video_upload_response": final_data
            }
            return self.video_response

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def post_video_url(self, payload: dict) -> dict:
        """
        Posts a video to TikTok by providing a video URL.

        Args:
            payload (dict): A dictionary containing the video post information and URL.
                             Expected keys include:
                               - 'source_info' (dict): Contains the source information, including 'source': 'PULL_FROM_URL' and 'video_url' (str).
                               - 'post_info' (dict): Contains the post details:
                                   - 'title' (str): The title of the video.
                                   - 'privacy_level' (str): The privacy level of the video ('PUBLIC', 'PRIVATE', 'FRIENDS').
                                   - 'disable_duet' (bool, optional): Whether to disable duet. Defaults to False.
                                   - 'disable_comment' (bool, optional): Whether to disable comments. Defaults to False.
                                   - 'disable_stitch' (bool, optional): Whether to disable stitch. Defaults to False.
                                   - 'video_cover_timestamp_ms' (int, optional): The timestamp for the cover. Defaults to 1000.

        Returns:
            dict: The response from the TikTok API after initiating the video post.

        Raises:
            TimeoutError: If the request to the TikTok API times out.
            HTTPError: If the HTTP request fails.
        """
        try:
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload, timeout=10))
            self.video_url_upload_response = response
            return response
        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def upload_video_file(self, payload: dict) -> dict:
        """
        Initializes a video upload to TikTok, providing upload details without immediately posting.

        Args:
            payload (dict): A dictionary containing the video upload information.
                             Expected keys include:
                               - 'source_info' (dict): Contains the source information, including:
                                   - 'source': 'FILE_UPLOAD'
                                   - 'video_size' (int): The size of the video file in bytes.
                                   - 'chunk_size' (int): The size of each chunk.
                                   - 'total_chunk_count' (int): The total number of chunks.
                               - 'file_data' (list): A list of dictionaries containing video chunks.

        Returns:
            dict: A dictionary containing the initial and final upload data from the TikTok API.

        Raises:
            TimeoutError: If the request to the TikTok API times out.
            HTTPError: If the HTTP request fails.
        """
        try:
            video_data = payload.pop("file_data")
            response = handle_response(requests.post(self.VIDEO_POST_URL, headers=self.headers, json=payload['source_info'], timeout=10))
            initial_data = response
            self.initial_video_upload_data = initial_data

            self._upload_video_chunks(initial_data['data']['upload_url'], video_data)

            complete_url = initial_data['data'].get('complete_url')
            if complete_url:
                response = requests.get(complete_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                final_data = response.json()
                self.final_video_upload_data = final_data
            else:
                final_data = {"message": "Finalization URL not found, check initial response."}

            return {
                "initial_data": initial_data,
                "final_data": final_data
            }

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def create_photo(
            self,
            post_mode: str,
            title: str,
            privacy_level: str,
            description: str = "",
            disable_comment: bool = False,
            auto_add_music: bool = False,
            photo_cover_index: int = 1,
            photo_images: Optional[List[str]] = None,
            access_token: Optional[str] = None,
    ) -> dict:
        """
        Creates and publishes a photo post to TikTok.

        Args:
            post_mode (str): The posting mode ('DIRECT_POST', 'MEDIA_UPLOAD').
            title (str): The title of the photo post.
            privacy_level (str): The privacy level of the photo post ('PUBLIC', 'PRIVATE', 'FRIENDS').
            description (str, optional): The description of the photo post. Defaults to "".
            disable_comment (bool, optional): Whether to disable comments for the photo post. Defaults to False.
            auto_add_music (bool, optional): Whether to automatically add music to the photo post (if supported). Defaults to False.
            photo_cover_index (int, optional): The index of the image to use as the cover (1-based). Defaults to 1.
            photo_images (Optional[List[str]], optional): A list of URLs for the photos to include in the post. Defaults to None.
            access_token (Optional[str], optional): The access token to use for the request. If not provided, it will try to use the access token stored in `self.token_data`. Defaults to None.

        Returns:
            dict: The response from the TikTok API after attempting to create the photo post.

        Raises:
            ValueError: If `post_mode` is invalid, `photo_images` is not provided or empty, or `photo_cover_index` is out of range.
            Exception: If no access token is available or if the API request fails.
            TimeoutError: If the request to the TikTok API times out.
            HTTPError: If the HTTP request fails.
        """
        if not post_mode in ["DIRECT_POST", "MEDIA_UPLOAD"]:
            raise ValueError("post_mode must be one of ['DIRECT_POST', 'MEDIA_UPLOAD']")

        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No access token available")

        if not photo_images or not isinstance(photo_images, list) or not len(photo_images):
            raise ValueError("photo_images must be a non-empty list of URLs")

        if (photo_cover_index < 1 or photo_cover_index > len(photo_images)):
            raise ValueError("photo_cover_index must be between 1 and the number of images provided")

        # fetch lates user info
        self.get_creator_info()

        headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get("access_token")}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        post_info = {
            "title": title,
            "description": description,
        }
        source_info = {
            "source": "PULL_FROM_URL",
            "photo_cover_index": photo_cover_index,
            "photo_images": photo_images
        }

        if post_mode == "DIRECT_POST":
            post_info.update({
                "disable_comment": disable_comment,
                "privacy_level": privacy_level,
                "auto_add_music": auto_add_music
            })

        payload = {
            "post_info": post_info,
            "source_info": source_info,
            "media_type": "PHOTO",
            "post_mode": post_mode
        }

        try:
            # initial posting
            response = handle_response(requests.post(self.PHOTO_POST_URL, headers=headers, json=payload, timeout=10))

            # Handle response
            self.photo_upload_response = response
            return {
                "photo_upload_response": self.photo_upload_response
            }

        except requests.exceptions.Timeout:
            raise TimeoutError ("The request to TikTok timed out.")
        except requests.exceptions.RequestException as e:
            raise HTTPError(f"Request failed: {e}")

    def check_upload_status(self, access_token: Optional[str] = None, publish_id: Optional[str] = None) -> dict:
        """
        Checks the upload status of a video on TikTok.

        Args:
            access_token (Optional[str], optional): The access token to use for the request. If not provided, it will try to use the access token stored in `self.token_data`. Defaults to None.
            publish_id (Optional[str], optional): The publish ID of the video to check. If not provided, it will try to use the publish ID from the `initial_video_upload_data`. Defaults to None.

        Returns:
            dict: The JSON response from the TikTok API containing the upload status.

        Raises:
            ValueError: If `publish_id` is not provided and not available in `initial_video_upload_data`.
            Exception: If no access token is available or if the API request fails.
        """
        if not access_token and not self.token_data.get("access_token"):
            raise Exception("No access token available")
        if not publish_id and not getattr(self, 'initial_video_upload_data', {}).get('data', {}).get("publish_id"):
            raise ValueError("publish_id must be provided to check upload status")

        url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

        headers = {
            "Authorization": f"Bearer {access_token if access_token else self.token_data.get("access_token")}",
            "Content-Type": "application/json; charset=UTF-8"
        }

        data = {
            "publish_id": publish_id if publish_id else self.initial_video_upload_data['data'].get("publish_id"),
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check upload status: {e}")