from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from procrunner import views
from operations.views import ListOperations, CreateOperation, RunOperation, OperationStatus


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'self', views.CurrentUserView)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/self/', views.CurrentUserView.as_view(), name="self"),

    url(r'^api/ops/create', CreateOperation.as_view(), name="create_operation"),
    url(r'^api/ops/run', RunOperation.as_view(), name="run_operation"),
    url(r'^api/ops/status/(?P<pk>\d)/$', OperationStatus.as_view(), name="operation_status"),

    url(r'^api/operations/', ListOperations.as_view(), name="operations"),



    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)


