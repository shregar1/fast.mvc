"""
Scheduled job abstraction.

Supports cron-like or interval jobs via APScheduler and leaves room
for Temporal/Prefect style workflows in the future.
"""

from __future__ import annotations

from typing import Any, Callable

from loguru import logger

from fastmvc_core import JobsConfiguration

try:  # Optional
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except Exception:  # pragma: no cover - optional
    AsyncIOScheduler = None  # type: ignore


class Scheduler:
    """
    Minimal scheduler facade.

    Currently wires APScheduler when configured; Temporal/Prefect
    can be integrated later by applications using the same config.
    """

    def __init__(self) -> None:
        cfg = JobsConfiguration.instance().get_config()
        self._backend = cfg.scheduler.backend
        self._scheduler = None

        if cfg.scheduler.enabled and cfg.scheduler.backend == "apscheduler":
            if AsyncIOScheduler is None:  # pragma: no cover - optional
                logger.warning(
                    "APScheduler is configured but not installed; "
                    "scheduled jobs will not run.",
                )
            else:
                self._scheduler = AsyncIOScheduler(timezone=cfg.scheduler.timezone)
                self._scheduler.start()
                logger.info("APScheduler started for cron/interval jobs.")
        elif cfg.scheduler.enabled and cfg.scheduler.backend in {"temporal", "prefect"}:
            logger.info(
                "Scheduler backend %s is configured. "
                "Integrate Temporal/Prefect client in your app code.",
                cfg.scheduler.backend,
            )

    def add_cron_job(
        self,
        func: Callable[..., Any],
        *,
        cron: str,
        job_id: str | None = None,
    ) -> None:
        """
        Register a cron-style job using APScheduler's CronTrigger syntax.
        """

        if not self._scheduler:
            logger.warning("No active scheduler; cannot register cron job %s", job_id or func.__name__)
            return

        # Cron string like "0 * * * *" (minute hour day month day_of_week)
        parts = cron.split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have 5 fields: 'm h dom mon dow'")

        minute, hour, day, month, day_of_week = parts
        self._scheduler.add_job(
            func,
            "cron",
            id=job_id,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
        )


__all__ = [
    "Scheduler",
]

