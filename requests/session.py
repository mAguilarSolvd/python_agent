from typing import Dict

import requests as rq
from datetime import datetime


class ZebrunnerApi:
    response = ["response", rq.Response]

    def __init__(self):
        self.project_name = "ALPHA"
        self.access_token = None
        self.media_type = {"content-type": "application/json"}
        self.authorization = None
        self.test_run_id = None
        self._BASE_URL = "https://solvdinternal.zebrunner.com"
        self.test_id = None

    def get_access_token(self):
        URL = f"{self._BASE_URL}/api/iam/v1/auth/refresh"

        data: Dict[str, str] = {"refreshToken": "HP4v6PasVpPt6RG5Dm4ufeyBVRJPi6T3gaKyKrRCXvFxjI9ytN"}

        response = rq.post(URL, json=data)

        json_response = response.json()

        self.access_token = json_response["authToken"]

        self.authorization = {"Authorization": f"Bearer {self.access_token}"}

    def req_test_run_start(self) -> None:
        URL: str = f"{self._BASE_URL}/api/reporting/v1/test-runs?projectKey={self.project_name}"

        data: Dict[str: str] = {
            "name": "Pytest practice",
            "startedAt": datetime.now().astimezone().isoformat(),
            "framework": "Pytest"
        }

        json_response = self.__perform_request(data, "post", URL).json()

        self.test_run_id = json_response["id"]

    def req_test_execution_start(self):
        URL: str = f"{self._BASE_URL}/api/reporting/v1/test-runs/{self.test_run_id}/tests"

        data: Dict[str: str] = {
            "name": "Test execution python",
            "className": "login_test",
            "methodName": "login_credentials",
            "startedAt": datetime.now().astimezone().isoformat()
        }

        json_response = self.__perform_request(data, "post", URL).json()

        self.test_id = json_response["id"]

    def req_test_execution_finish(self):
        URL: str = f"{self._BASE_URL}/api/reporting/v1/test-runs/{self.test_run_id}/tests/{self.test_id}"

        data: Dict[str: str] = {
            "result": "PASSED",
            "endedAt": datetime.now().astimezone().isoformat()
        }

        self.__perform_request(data, "put", URL)

    def req_test_run_execution_finish(self):
        URL: str = f"{self._BASE_URL}/api/reporting/v1/test-runs/{self.test_run_id}"

        data: Dict[str: str] = {
            "endedAt": datetime.now().isoformat()
        }

        self.__perform_request(data, "put", URL).json()

    def get_header(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def __perform_request(self, data: Dict[str, str], verb: str, url: str) -> response:

        if verb == "post":
            response_endpoint = rq.post(url, json=data, headers=self.get_header())
            return response_endpoint
        else:
            response_endpoint = rq.put(url, json=data, headers=self.get_header())
            return response_endpoint


if __name__ == "__main__":
    zebrunner = ZebrunnerApi()
    zebrunner.get_access_token()
    zebrunner.req_test_run_start()
    zebrunner.req_test_execution_start()
    zebrunner.req_test_execution_finish()
    zebrunner.req_test_run_execution_finish()
