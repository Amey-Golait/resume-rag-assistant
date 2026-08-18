from typing import Any

import httpx

from config import API_BASE_URL


class APIError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.is_success:
            return response.json()

        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except Exception:
            pass
        raise APIError(str(detail), response.status_code)

    def health(self) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(f"{self.base_url}/health")
            return self._handle_response(response)

    def upload_resume(self, file_bytes: bytes, filename: str) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/upload/resume",
                files={"file": (filename, file_bytes, "application/pdf")},
            )
            return self._handle_response(response)

    def upload_job(self, file_bytes: bytes, filename: str) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/upload/job",
                files={"file": (filename, file_bytes, "application/pdf")},
            )
            return self._handle_response(response)

    def analyze(self, resume_filename: str, job_description: str) -> dict:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/analyze",
                json={
                    "resume_filename": resume_filename,
                    "job_description": job_description,
                },
            )
            return self._handle_response(response)

    def ask(self, question: str, job_description: str | None = None) -> dict:
        payload: dict[str, Any] = {"question": question}
        if job_description:
            payload["job_description"] = job_description

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.base_url}/ask", json=payload)
            return self._handle_response(response)
