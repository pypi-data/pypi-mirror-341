import threading
from typing import Optional

import httpx

from tracedy import Tracedy
from tracedy.types import MaskFunction


class TracedySingleton:
    _instance = None
    _lock = threading.Lock()
    _tracedy: Optional[Tracedy] = None

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(TracedySingleton, cls).__new__(cls)
        return cls._instance

    def get(
        self,
        *,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
        release: Optional[str] = None,
        debug: Optional[bool] = None,
        threads: Optional[int] = None,
        flush_at: Optional[int] = None,
        flush_interval: Optional[int] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[int] = None,
        httpx_client: Optional[httpx.Client] = None,
        sdk_integration: Optional[str] = None,
        enabled: Optional[bool] = None,
        sample_rate: Optional[float] = None,
        mask: Optional[MaskFunction] = None,
        environment: Optional[str] = None,
    ) -> Tracedy:
        if self._tracedy:
            return self._tracedy

        with self._lock:
            if self._tracedy:
                return self._tracedy

            tracedy_init_args = {
                "public_key": public_key,
                "secret_key": secret_key,
                "host": host,
                "release": release,
                "debug": debug,
                "threads": threads,
                "flush_at": flush_at,
                "flush_interval": flush_interval,
                "max_retries": max_retries,
                "timeout": timeout,
                "httpx_client": httpx_client,
                "sdk_integration": sdk_integration,
                "enabled": enabled,
                "sample_rate": sample_rate,
                "mask": mask,
                "environment": environment,
            }

            self._tracedy = Tracedy(
                **{k: v for k, v in tracedy_init_args.items() if v is not None}
            )

            return self._tracedy

    def reset(self) -> None:
        with self._lock:
            if self._tracedy:
                self._tracedy.shutdown()

            self._tracedy = None
