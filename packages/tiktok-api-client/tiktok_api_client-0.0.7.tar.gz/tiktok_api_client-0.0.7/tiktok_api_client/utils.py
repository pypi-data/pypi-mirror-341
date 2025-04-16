import os
import math
from typing import List, Dict, Union, Iterator

class InvalidFileType(ValueError):
    """Custom exception for invalid file types."""
    pass

class HTTPError(Exception):
    """Base class for HTTP errors."""
    pass

class NotFoundError(HTTPError):
    """Exception raised for 404 Not Found errors."""
    def __init__(self, message="Resource not found"):
        super().__init__(f"404 Not Found: {message}")

class InternalServerError(HTTPError):
    """Exception raised for 500 Internal Server errors."""
    def __init__(self, message="Internal server error"):
        super().__init__(f"500 Internal Server Error: {message}")

class TimeoutError(HTTPError):
    """Exception raised when a request times out."""
    def __init__(self, message="The request timed out"):
        super().__init__(f"Timeout Error: {message}")


# Define common video and photo file extensions as sets for faster lookups
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm'}
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif'}

# A default target chunk size when chunking is required/chosen (e.g., 10 MiB).
DEFAULT_CHUNK_SIZE_BYTES = 10 * 1024 * 1024  # 10 MiB
# Maximum number of chunks allowed by the API.
MAX_CHUNKS_COUNT = 1000


def convert_bytes_to_readable(size_bytes: int) -> str:
    """Converts bytes to a human-readable format (e.g., KB, MB, GB)."""
    if size_bytes <= 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    i = min(i, len(size_name) - 1)
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def get_file(file_path: str) -> Dict[str, Union[int, str, List[Dict[str, Union[int, str, bytes]]]]]:
    """
    Retrieves information about a file, including its size and chunks.

    Args:
        file_path: The path to the file.

    Returns:
        A dictionary containing file metadata and a list of chunk data.

    Raises:
        FileNotFoundError: If the file does not exist.
        InvalidFileType: If the file is not a recognized video or photo type.
        ValueError: If the file size is negative or calculated chunk size is invalid.
        Exception: For other unexpected errors during file processing.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() not in VIDEO_EXTENSIONS and file_extension.lower() not in PHOTO_EXTENSIONS:
        raise InvalidFileType(f"File '{os.path.basename(file_path)}' is not a recognized video or photo type.")

    try:
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 0:
            raise ValueError("File size cannot be negative.")

        if file_size_bytes == 0:
            return {
                'file_size': 0,
                'chunk_size': 0,
                'total_chunks': 0,
                'file_size_bytes': 0,
                'file_size_readable': "0 B",
                'chunk_size_bytes': 0,
                'chunk_size_readable': "0 B",
                'file_path': file_path,
                'file_data': [],
            }

        if file_size_bytes <= DEFAULT_CHUNK_SIZE_BYTES:
            calculated_chunk_size_bytes = file_size_bytes
            total_chunks = 1
        else:
            target_chunk_size = DEFAULT_CHUNK_SIZE_BYTES
            provisional_chunks = math.ceil(file_size_bytes / target_chunk_size)

            if provisional_chunks <= MAX_CHUNKS_COUNT:
                calculated_chunk_size_bytes = target_chunk_size
                total_chunks = provisional_chunks
            else:
                required_chunk_size = math.ceil(file_size_bytes / MAX_CHUNKS_COUNT)
                calculated_chunk_size_bytes = max(required_chunk_size, DEFAULT_CHUNK_SIZE_BYTES)
                total_chunks = min(math.ceil(file_size_bytes / calculated_chunk_size_bytes), MAX_CHUNKS_COUNT)

        if calculated_chunk_size_bytes <= 0:
            raise ValueError("Calculated chunk size is invalid (must be > 0 for non-empty files).")

        file_size_readable = convert_bytes_to_readable(file_size_bytes)
        chunk_size_readable = convert_bytes_to_readable(calculated_chunk_size_bytes)

        chunks_info: List[Dict[str, Union[int, str, bytes]]] = []
        with open(file_path, "rb") as f:
            for i in range(total_chunks):
                start = i * calculated_chunk_size_bytes
                end = min((i + 1) * calculated_chunk_size_bytes, file_size_bytes) - 1
                chunk_data = f.read(end - start + 1)
                chunks_info.append({
                    'start': start,
                    'end': end,
                    'content_range': f"bytes {start}-{end}/{file_size_bytes}",
                    "chunk_data": chunk_data
                })

        file_info = {
            'file_size': file_size_bytes,
            'chunk_size': calculated_chunk_size_bytes,
            'total_chunks': total_chunks,
            'file_size_bytes': file_size_bytes,
            'file_size_readable': file_size_readable,
            'chunk_size_bytes': calculated_chunk_size_bytes,
            'chunk_size_readable': chunk_size_readable,
            'file_path': file_path,
            'file_data': chunks_info,
        }
        return file_info

    except (FileNotFoundError, InvalidFileType, ValueError) as e:
        raise
    except Exception as e:
        raise Exception(f"An unexpected error occurred while processing the file: {e}")


def handle_response(response: 'requests.Response') -> Dict:
    """
    Handles the HTTP response from an API.

    Args:
        response: The HTTP response object (e.g., from the 'requests' library).

    Returns:
        The JSON response from the API if the request was successful.

    Raises:
        NotFoundError: If the response status code is 404.
        InternalServerError: If the response status code is 500.
        TimeoutError: If the response status code is 408.
        HTTPError: For other non-200 status codes.
    """
    if response.status_code == 404:
        raise NotFoundError("The requested resource was not found.")
    elif response.status_code == 500:
        raise InternalServerError("The server encountered an error.")
    elif response.status_code == 408:
        raise TimeoutError("The request timed out.")
    elif response.status_code != 200:
        raise HTTPError(f"HTTP Error: {response.status_code} - {response.text}")
    else:
        response.raise_for_status()  # Raise an exception for bad status codes (e.g., 4xx, 5xx)
        return response.json()