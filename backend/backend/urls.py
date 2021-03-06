from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from procrunner import views

from operations.views import ListOperations, CreateOperation, RunOperation, OperationStatus
from operations.views import MetaWorkflows, MetaWorkflow, CreateWorkflow, RunWorkflow, WorkflowStatus,ResetWorkflow
from operations.views import WorkflowViewSet, OperationViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'workflows', WorkflowViewSet)
#router.register(r'self', views.CurrentUserView)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/self/$', views.CurrentUserView.as_view(), name="self"),

    url(r'^api/ops/create/$', CreateOperation.as_view(), name="create_operation"),
    url(r'^api/ops/run/$', RunOperation.as_view(), name="run_operation"),
    url(r'^api/ops/status/(?P<pk>[0-9]+)/$', OperationStatus.as_view(), name="operation_status"),

    url(r'^api/metaoperations/', ListOperations.as_view(), name="operations"),


    url(r'^api/wf/create/$', CreateWorkflow.as_view(), name="create_workflow"),
    
    url(r'^api/wf/run/(?P<pk>[0-9]+)/$', RunWorkflow.as_view(), name="run_workflow_id"),
    url(r'^api/wf/run/$', RunWorkflow.as_view(), name="run_workflow"),
    
    url(r'^api/wf/reset/(?P<pk>[0-9]+)/$', ResetWorkflow.as_view(), name="reset_workflow"),
    url(r'^api/wf/reset/$', ResetWorkflow.as_view(), name="reset_workflow_id"),

    url(r'^api/wf/status/(?P<pk>[0-9]+)/$', WorkflowStatus.as_view(), name="workflow_status"),    
    
    url(r'^api/metaworkflows/(?P<name>\w+)/$', MetaWorkflow.as_view(), name="metaworkflow"),
    url(r'^api/metaworkflows/', MetaWorkflows.as_view(), name="metaworkflows"),



    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)


