import logging
from logging import LogRecord, StreamHandler
from typing import List, Optional, Tuple
from datetime import datetime, timedelta, time
from pydantic import ValidationError, BaseModel
from models import LogDTO
from requests.session import ZebrunnerApi
import httpx

class loggerHandler(StreamHandler):

    def send_logs(self, test_run_id: int, logs: List[LogDTO]) -> None:

        URL = f"{ZebrunnerApi._BASE_URL}/api/reporting/v1/test-runs/{ZebrunnerApi.test_run_id}/logs"

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

    logs: List[LogDTO] = []

    def __init__(self) -> None:
        super().__init__()
        if ZebrunnerApi.test_id != None:
            self.api = ZebrunnerApi(ZebrunnerApi._BASE_URL, ZebrunnerApi.get_access_token())
        else:
            self.api = None
            self.last_push = datetime.utcnow()

    def emit(self, record: LogRecord) -> None:

        if datetime.utcnow() - self.last_push >= timedelta(seconds=1):
            self.push_logs()

        if ZebrunnerApi.test_run_id != None and ZebrunnerApi.test_id != None:

            self.logs.append(
                LogDTO(
                    test_id=str(ZebrunnerApi.test_id),
                    timestamp=str(round(time.time() * 1000)),
                    level=record.levelname,
                    message=str(record.msg),
                )
            )

    def push_logs(self)-> None:
        try:
            send_logs = True
            if ZebrunnerApi.test_run_id != None and send_logs:
                self.send_logs(ZebrunnerApi.test_run_id, self.logs)
        except Exception as e:
            logging.ERROR("Failed to send logs to Zebrunner", exc_info = e)
        finally:
            self.logs = []
            self.last_push = datetime.utcnow()
