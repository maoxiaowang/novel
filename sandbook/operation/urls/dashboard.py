from django.urls import path
from operation.views.dashboard import Index, task, novel, application

dashboard_urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),

    # Task
    path('tasks/', task.TaskIndex.as_view(), name='dashboard_task_index'),
    path('tasks/<int:category_id>/', task.TaskList.as_view(), name='dashboard_task_list'),

    # Novel
    path('novels/<int:category_id>/', novel.NovelList.as_view(), name='dashboard_novel_list'),
    path('novel/<int:novel_id>/update-status/', novel.UpdateStatus.as_view(), name='dashboard_novel_approve'),

    # Author
    path('user/applications/', application.ApplicationList.as_view(), name='dashboard_application_list'),
    path('user/application/<int:pk>/approve/', application.ApplicationApprove.as_view(),
         name='dashboard_application_approve'),
]
