"""
URL configuration for board_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from board_routine.views import like_routine

urlpatterns = [
    path("admin/", admin.site.urls),
    path("photo/", include("board_photo.urls")),
    path("routine/", include("board_routine.urls")),
    path("routine/<int:pk>/like/", like_routine, name="like_routine"),
    path("", views.home, name="home"),  # 홈페이지
]

# 미디어 파일 서빙 (개발환경에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
