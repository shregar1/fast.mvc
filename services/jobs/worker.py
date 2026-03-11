"""
Background job worker abstraction.

Provides a thin facade over Celery, RQ, and Dramatiq. These are
intentionally minimal so that applications can plug in their own
task definitions while FastMVC handles configuration wiring.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from loguru import logger

from configurations.jobs import JobsConfiguration

try:  # Optional
    from celery import Celery
except Exception:  # pragma: no cover - optional
    Celery = None  # type: ignore

try:
    import rq
    from redis import Redis
except Exception:  # pragma: no cover - optional
    rq = None  # type: ignore
    Redis = None  # type: ignore

try:
    import dramatiq
except Exception:  # pragma: no cover - optional
    dramatiq = None  # type: ignore


class JobWorker:
    """
    High-level entry point to enqueue background jobs.

    Depending on configuration, this will use Celery, RQ, or Dramatiq.
    """

    def __init__(self) -> None:
        cfg = JobsConfiguration.instance().get_config()
        self._celery_app: Optional[Celery] = None
        self._rq_queue: Optional["rq.Queue"] = None  # type: ignore[name-defined]
        self._dramatiq_broker = None

        if cfg.celery.enabled and Celery is not None:
            self._celery_app = Celery(
                cfg.celery.namespace,
                broker=cfg.celery.broker_url,
                backend=cfg.celery.result_backend,
            )
            logger.info("Celery worker configured.")

        if cfg.rq.enabled and rq is not None and Redis is not None:
            redis_conn = Redis.from_url(cfg.rq.redis_url)
            self._rq_queue = rq.Queue(cfg.rq.queue_name, connection=redis_conn)
            logger.info("RQ worker configured.")

        if cfg.dramatiq.enabled and dramatiq is not None:
            self._dramatiq_broker = dramatiq.get_broker()
            logger.info("Dramatiq worker configured.")

        if not any([self._celery_app, self._rq_queue, self._dramatiq_broker]):
            logger.info(
                "No background job worker is enabled. "
                "Update config/jobs/config.json to enable Celery/RQ/Dramatiq.",
            )

    def enqueue(
        self,
        task_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Enqueue a job by task/function name.

        The concrete registration of tasks is left to the application;
        this facade just delegates to the configured backend.
        """

        if self._celery_app is not None:
            self._celery_app.send_task(task_name, args=args, kwargs=kwargs)
            return

        if self._rq_queue is not None:
            self._rq_queue.enqueue(task_name, *args, **kwargs)
            return

        if self._dramatiq_broker is not None and dramatiq is not None:
            actor = self._dramatiq_broker.get_actor(task_name)
            if actor is not None:
                actor.send(*args, **kwargs)
                return

        logger.warning(
            "No job backend configured; dropping job %s", task_name,
        )


__all__ = [
    "JobWorker",
]

