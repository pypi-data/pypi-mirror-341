import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from pydantic import BaseModel, validate_call
from requests import HTTPError, Response, post

from .exceptions import (
    ApiError,
    InvalidResponseError,
    MissingApiKeyError,
    RpcError,
    SessionError,
    WetrafficError,
)
from .logging_config import setup_logger


class RpcRequest(BaseModel):
    action: str
    params: Dict[str, Any]


logger = setup_logger()


class ApiClient:
    DEFAULT_ENDPOINT = "https://api.wetraffic.eu/main"
    SESSION_EXPIRATION_BUFFER = timedelta(minutes=5)

    @validate_call
    def __init__(self, *, area: str, endpoint: str = DEFAULT_ENDPOINT):
        api_key = os.environ.get("WETRAFFIC_API_KEY")
        if not api_key:
            log_extra = {"area": area, "reason": "WETRAFFIC_API_KEY not set"}
            logger.critical("SDK Initialization failed", extra=log_extra)
            raise MissingApiKeyError("WETRAFFIC_API_KEY not set.")

        self.api_key: str = api_key
        self.area = area
        self.session_token: Optional[str] = None
        self.session_expiration_date = datetime.min
        self.endpoint = endpoint
        logger.info(
            "WetrafficSdk initialized",
            extra={"area": self.area, "endpoint": self.endpoint},
        )

    def _is_session_valid(self) -> bool:
        if self.session_token is None:
            return False
        is_valid = self.session_expiration_date > (
            datetime.now() + self.SESSION_EXPIRATION_BUFFER
        )
        logger.debug(
            "Session validity check",
            extra={
                "area": self.area,
                "session_valid": is_valid,
                "session_expires": (
                    self.session_expiration_date.isoformat()
                    if self.session_expiration_date != datetime.min
                    else None
                ),
            },
        )
        return is_valid

    def _format_error_response(self, response: Response) -> dict:
        error_data = {
            "status_code": response.status_code,
            "reason": response.reason,
            "text": response.text,
        }
        return error_data

    def _upsert_session_token(self):
        logger.info("Requesting new session token", extra={"area": self.area})
        payload = RpcRequest(
            action="get_session_token",
            params={
                "area": self.area,
                "api_key": self.api_key,
            },
        )

        try:
            response = post(self.endpoint, json=payload.model_dump())
            response.raise_for_status()

            data = response.json()
            new_token = data.get("token")
            new_iso_date = data.get("token_expiration")

            if not new_token or not new_iso_date:
                logger.error("Incomplete session data received")
                raise InvalidResponseError("Incomplete session data", response)

            self.session_token = new_token
            self.session_expiration_date = datetime.fromisoformat(new_iso_date)
            logger.info(
                "Obtained new session token", extra={"new_iso_date": new_iso_date}
            )

        except HTTPError as http_err:
            logger.error(
                "HTTP error getting session token",
                exc_info=logger.getEffectiveLevel() <= logging.DEBUG,
            )
            raise ApiError(
                "Failed to get session token", http_err.response
            ) from http_err

        except InvalidResponseError as e:
            logger.error(
                "Invalid response data",
                exc_info=logger.getEffectiveLevel() <= logging.DEBUG,
            )
            raise SessionError("Invalid session data received", e.response) from e

        except Exception as e:
            logger.error(
                "Unexpected error getting session token",
                extra={"error": str(e)},
                exc_info=logger.getEffectiveLevel() <= logging.DEBUG,
            )
            raise WetrafficError(f"Unexpected error: {str(e)}") from e

    @validate_call
    def invoke_rpc(self, action: str, params: dict) -> Any:
        log_extra: dict = {
            "action": action,
        }
        logger.debug("Invoking RPC action", extra=log_extra)

        if not self._is_session_valid():
            logger.info(
                "Session invalid or expired, refreshing token.", extra=log_extra
            )
            self._upsert_session_token()

        if not self.session_token:
            logger.error(
                "Cannot invoke RPC, session token is missing after refresh attempt.",
                extra=log_extra,
            )
            raise SessionError("Session token unavailable for RPC call")

        headers = {"Authorization": f"Bearer {self.session_token}"}
        logger.debug("Sending RPC request", extra=log_extra)

        rpc_data = RpcRequest(action=action, params=params)
        try:
            response = post(self.endpoint, headers=headers, json=rpc_data.model_dump())
            response.raise_for_status()

            log_extra["status_code"] = response.status_code
            logger.debug("RPC successful", extra=log_extra)
            return response.json()

        except HTTPError as http_err:
            log_extra["error_details"] = self._format_error_response(http_err.response)
            logger.error(
                "HTTP error during RPC",
                extra=log_extra,
                exc_info=logger.getEffectiveLevel() <= logging.DEBUG,
            )
            raise RpcError(action, "RPC call failed", http_err.response) from http_err

        except Exception as e:
            log_extra["error"] = str(e)
            logger.error(
                "Unexpected error during RPC",
                extra=log_extra,
                exc_info=logger.getEffectiveLevel() <= logging.DEBUG,
            )
            raise WetrafficError(f"Unexpected error during RPC: {str(e)}") from e
