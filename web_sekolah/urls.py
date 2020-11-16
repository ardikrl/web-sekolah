from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from blog.views import HelloView


urlpatterns = [
    path('', include('blog.urls')),
    path('', include('sekolah.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hello/', HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
