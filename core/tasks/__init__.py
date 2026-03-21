"""
Background jobs — re-exported from ``fast_jobs``.

Prefer importing from the library directly in new code::

    from fast_jobs import enqueue, JobsConfiguration, cancel_job

The previous Redis ``TaskQueue`` / ``@task`` helpers were removed; use ``enqueue`` with
Celery / RQ / Dramatiq per ``config/jobs/config.json`` (see ``fast_jobs`` docs).
"""

from fast_jobs import (
    CancelJobResult,
    CronScheduleDTO,
    JobEnqueueResult,
    JobStatus,
    JobStatusSnapshot,
    JobsConfiguration,
    JobsConfigurationDTO,
    cancel_job,
    celery_crontab_schedule,
    dramatiq_periodiq_cron,
    enqueue,
    get_celery_app_if_enabled,
    get_job_status,
    get_queue_timeouts,
    make_celery_app,
    parse_cron_fields,
    resolve_job_timeout_seconds,
    rq_scheduler_cron,
)

__all__ = [
    "CancelJobResult",
    "CronScheduleDTO",
    "JobEnqueueResult",
    "JobStatus",
    "JobStatusSnapshot",
    "JobsConfiguration",
    "JobsConfigurationDTO",
    "cancel_job",
    "celery_crontab_schedule",
    "dramatiq_periodiq_cron",
    "enqueue",
    "get_celery_app_if_enabled",
    "get_job_status",
    "get_queue_timeouts",
    "make_celery_app",
    "parse_cron_fields",
    "resolve_job_timeout_seconds",
    "rq_scheduler_cron",
]
