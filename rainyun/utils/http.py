"""HTTP helper utilities."""

import logging
import os
import time
from typing import Any

import requests

from rainyun.config import Config

logger = logging.getLogger(__name__)


def request_with_retry(
    method: str,
    url: str,
    *,
    max_retries: int = 3,
    retry_delay: int = 2,
    log: logging.Logger | None = None,
    **kwargs: Any,
) -> requests.Response:
    last_error = None
    log = log or logger
    for attempt in range(1, max_retries + 1):
        try:
            return requests.request(method=method, url=url, **kwargs)
        except requests.RequestException as e:
            last_error = e
            log.warning(f"HTTP 请求异常（第{attempt}次）：{url} - {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
    raise last_error


def post_with_retry(
    url: str,
    *,
    max_retries: int = 3,
    retry_delay: int = 2,
    log: logging.Logger | None = None,
    **kwargs: Any,
) -> requests.Response:
    return request_with_retry(
        "POST",
        url,
        max_retries=max_retries,
        retry_delay=retry_delay,
        log=log,
        **kwargs,
    )


def download_bytes(
    url: str,
    *,
    timeout: int,
    max_retries: int = 3,
    retry_delay: float = 2,
    log: logging.Logger | None = None,
) -> bytes:
    last_error: str | None = None
    log = log or logger
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200 and response.content:
                return response.content
            last_error = f"status_code={response.status_code}"
            log.warning(f"下载图片失败 (第 {attempt} 次): {last_error}, URL: {url}")
        except requests.RequestException as e:
            last_error = str(e)
            log.warning(f"下载图片失败 (第 {attempt} 次): {e}, URL: {url}")
        if attempt < max_retries:
            time.sleep(retry_delay)
    raise RuntimeError(f"下载图片失败，已重试 {max_retries} 次: {last_error}, URL: {url}")


def download_to_file(
    url: str,
    output_path: str,
    config: Config,
    *,
    log: logging.Logger | None = None,
) -> bool:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    last_error: str | None = None
    log = log or logger
    for attempt in range(1, config.download_max_retries + 1):
        try:
            response = requests.get(url, timeout=config.download_timeout)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return True
            last_error = f"status_code={response.status_code}"
            log.warning(f"下载图片失败 (第 {attempt} 次): {last_error}, URL: {url}")
        except requests.RequestException as e:
            last_error = str(e)
            log.warning(f"下载图片失败 (第 {attempt} 次): {e}, URL: {url}")
        if attempt < config.download_max_retries:
            time.sleep(config.download_retry_delay)
    log.error(f"下载图片失败，已重试 {config.download_max_retries} 次: {last_error}, URL: {url}")
    return False
