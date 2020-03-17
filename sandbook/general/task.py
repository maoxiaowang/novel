"""
Inherit this Task if you define a new Task class
"""
import traceback

from billiard.exceptions import SoftTimeLimitExceeded
from celery.task import Task
# from celery_once import QueueOnce
from general.core.logging import task_logger as logger

__all__ = [
    'CommonTask',
    # 'CommonTaskOnce'
]


class CommonTask(Task):
    silent_exceptions = (SoftTimeLimitExceeded,)

    def run(self, *args, **kwargs):
        # do something when task runs
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # do something when task raise any exception
        # catch billiard.exceptions.SoftTimeLimitExceeded here
        if exc in self.silent_exceptions:
            print('{0!r} aborted: {1!r}'.format(task_id, exc))
        else:
            print('{0!r} failed: {1!r}'.format(task_id, exc))
            logger.error('{0!r} failed: {1!r}'.format(task_id, exc))
            logger.error(traceback.format_exc())

    def on_success(self, retval, task_id, args, kwargs):
        # do something when task finished successfully
        # TODO:
        # LayerResource.objects.create()
        print('{0!r} success: {1!r}'.format(task_id, retval))
        logger.info('{0!r} success: {1!r}'.format(task_id, retval))


# class CommonTaskOnce(QueueOnce):
#     silent_exceptions = (SoftTimeLimitExceeded,)
#
#     def run(self, *args, **kwargs):
#         # do something when task runs
#         pass
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         # do something when task raise any exception
#         # catch billiard.exceptions.SoftTimeLimitExceeded here
#         if exc in self.silent_exceptions:
#             print('{0!r} aborted: {1!r}'.format(task_id, exc))
#         else:
#             print('{0!r} failed: {1!r}'.format(task_id, exc))
#             logger.error('{0!r} failed: {1!r}'.format(task_id, exc))
#             logger.error(traceback.format_exc())
#
#     def on_success(self, retval, task_id, args, kwargs):
#         # do something when task finished successfully
#         # TODO:
#         # LayerResource.objects.create()
#         print('{0!r} success: {1!r}'.format(task_id, retval))
#         logger.info('{0!r} success: {1!r}'.format(task_id, retval))
