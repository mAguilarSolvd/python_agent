import logging
from logging import LogRecord, StreamHandler
from typing import List
from datetime import datetime, timedelta, time
from models import LogDTO
from session import ZebrunnerApi
import httpx

api = ZebrunnerApi()
log = logging.getLogger(__name__)


class loggerHandler(StreamHandler):
    logs: List[LogDTO] = []

    def __init__(self) -> None:
        super().__init__()
        if api.test_run_id is not None:
            self.api = ZebrunnerApi(api.getUrl(), api.get_access_token())
        else:
            self.api = None
            self.last_push = datetime.utcnow()

    def send_logs(self, test_run_id: int, logs: List[LogDTO]) -> None:

        BASE_URL = api.getUrl()

        URL = f"{BASE_URL}/api/reporting/v1/test-runs/{test_run_id}/logs"

        body = [x.dict(exclude_none=True, by_alias=True) for x in logs]
        try:
            response = self._client.post(URL, json=body)
        except httpx.RequestError as e:
            raise Exception("Failed to send logs", e)

        if not response.is_success:
            raise Exception(
                "Failed to send logs. Non successful status code",
                {"status_code": response.status_code, "body": response.json()},
            )

    def emit(self, record: LogRecord) -> None:

        if datetime.utcnow() - self.last_push >= timedelta(seconds=1):
            self.push_logs()

        if api.test_run_id is not None and api.test_id is not None:
            self.logs.append(
                LogDTO(
                    test_id=str(api.test_id),
                    message=str(record.msg),
                    level=record.levelname,
                    timestamp=str(round(time.time() * 1000))
                )
            )

    def push_logs(self) -> None:
        try:
            send_logs = True
            if api.test_run_id is not None and send_logs:
                self.send_logs(api.test_run_id, self.logs)
        except Exception as e:
            log.error("Failed to send logs to Zebrunner", exc_info=e)
        finally:
            self.logs = []
            self.last_push = datetime.utcnow()
