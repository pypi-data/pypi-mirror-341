from jarvismode.services.base import Service
from jarvismode.services.factory import ServiceFactory
from jarvismode.services.job_queue.service import JobQueueService


class JobQueueServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(JobQueueService)

    def create(self) -> Service:
        return JobQueueService()
