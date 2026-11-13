from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import include, path, re_path
from core.yasg import urlpatterns_yasg
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlpatterns_yasg)),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    path('api/v1/auth/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/v1/', include('apps.testapp.urls')),
]


if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + 
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
else:
    urlpatterns += [
        re_path(r'^back_media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]