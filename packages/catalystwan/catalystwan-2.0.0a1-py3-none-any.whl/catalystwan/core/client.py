from __future__ import annotations

import logging
from contextlib import contextmanager
from copy import copy
from typing import TYPE_CHECKING, Generator, Optional, Union

from catalystwan.core.apigw_auth import ApiGwAuth
from catalystwan.core.loader import load_client
from catalystwan.core.request_adapter import RequestAdapter
from catalystwan.core.request_limiter import RequestLimiter
from catalystwan.core.session import ManagerSession, create_base_url, create_manager_session
from catalystwan.core.vmanage_auth import vManageAuth

if TYPE_CHECKING:
    from catalystwan.core.loader import ApiClient


@contextmanager
def create_thread_client(
    url: str,
    auth: Union[vManageAuth, ApiGwAuth],
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
    request_limiter: Optional[RequestLimiter] = None,
) -> Generator[ApiClient, None, None]:
    if logger is None:
        logger = logging.getLogger(__name__)
    session = ManagerSession(
        base_url=create_base_url(url, port),
        auth=auth,
        subdomain=subdomain,
        logger=logger,
        request_limiter=request_limiter,
    )
    with session.login():
        version = session.api_version.base_version
        logger.debug(f"Choosing client for version {version}...")
        client = load_client(session.api_version.base_version)
        logger.debug(f"Client for version {version} loaded")
        yield client(RequestAdapter(session=session, logger=logger))


@contextmanager
def create_client(
    url: str,
    username: str,
    password: str,
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> Generator[ApiClient, None, None]:
    if logger is None:
        logger = logging.getLogger(__name__)
    with create_manager_session(url, username, password, port, subdomain, logger) as session:
        version = session.api_version.base_version
        logger.debug(f"Choosing client for version {version}...")
        client = load_client(session.api_version.base_version)
        logger.debug(f"Client for version {version} loaded")
        yield client(RequestAdapter(session=session, logger=logger))


@contextmanager
def copy_client(client: ApiClient) -> Generator[ApiClient, None, None]:
    request_adapter = copy(client._request_adapter)
    session = request_adapter.session
    with session.login():
        new_client = load_client(session.api_version.base_version)(request_adapter)
        assert new_client.api_version == client.api_version
        yield new_client
