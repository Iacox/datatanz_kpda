from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from Config import settings

urlpatterns = [
                  # route панели администрации
                  path('admin/', admin.site.urls),
                  # подключение routes приложения api
                  path("api/", include("api.urls")),
                  # route медиа файлов проекта
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
