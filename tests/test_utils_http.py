import importlib.util
import unittest
from unittest.mock import patch

REQUESTS_AVAILABLE = importlib.util.find_spec("requests") is not None

if REQUESTS_AVAILABLE:
    import requests

    from rainyun.utils.http import download_bytes, request_with_retry


class DummyResponse:
    def __init__(self, status_code: int, content: bytes) -> None:
        self.status_code = status_code
        self.content = content


@unittest.skipUnless(REQUESTS_AVAILABLE, "requests 未安装，跳过 HTTP 工具测试")
class HttpUtilsTests(unittest.TestCase):
    def test_request_with_retry_success(self):
        response = DummyResponse(200, b"ok")
        with patch("rainyun.utils.http.requests.request", return_value=response) as mock_request:
            result = request_with_retry("GET", "http://example.com", max_retries=1)

        self.assertEqual(result, response)
        mock_request.assert_called_once()

    def test_download_bytes_success(self):
        response = DummyResponse(200, b"data")
        with patch("rainyun.utils.http.requests.get", return_value=response):
            result = download_bytes(
                "http://example.com/img",
                timeout=1,
                max_retries=1,
                retry_delay=0,
            )

        self.assertEqual(result, b"data")


if __name__ == "__main__":
    unittest.main()
