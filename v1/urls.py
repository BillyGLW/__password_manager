from django.urls import include, path, re_path
from rest_framework import routers
from . import views

from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# router.register(r'custom', views.RWeb_ManagerView, basename='Custom')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='obtain_new_token'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
    re_path(r'^user/$', views.RWeb_ManagerView.as_view(), name='create_new_password'),
    re_path(r'^user/(?P<pk>[0-9]+)$', views.RWeb_get_delete_update_ManagerView.as_view(), name='create_new_password'),
    # re_path(r'^user/(?P<pk>[0-9]+)$', views.RWeb_ManagerView.as_view(), name='create_new_password'),
]


