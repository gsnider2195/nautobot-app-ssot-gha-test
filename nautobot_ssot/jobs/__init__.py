"""Plugin provision of Nautobot Job subclasses."""

from django.conf import settings

from nautobot.extras.models import Job
from nautobot_ssot.jobs.base import DataSource, DataTarget
from nautobot_ssot.jobs.examples import ExampleDataSource, ExampleDataTarget

if settings.PLUGINS_CONFIG["nautobot_ssot"]["hide_example_jobs"]:
    jobs = []
else:
    jobs = [ExampleDataSource, ExampleDataTarget]


def _add_integrations():
    for module in each_enabled_integration_module("jobs"):
        for job in module.jobs:
            if job in jobs:
                raise Exception(f"Job {job} already exists in jobs list for integration {module.__file__}.")
            logger.debug("Registering job %s from %s", job, module.__file__)
            jobs.append(job)


_add_integrations()


def get_data_jobs():
    """Get all data-source and data-target jobs available."""
    sync_jobs = Job.objects.all()
    data_sources = []
    data_targets = []
    for job in sync_jobs:
        if issubclass(job.job_class, DataSource):
            data_sources.append(job.job_class)
        if issubclass(job.job_class, DataTarget):
            data_targets.append(job.job_class)

    return (data_sources, data_targets)
