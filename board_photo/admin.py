from django.contrib import admin
from .models import PhotoBoard, Like


@admin.register(PhotoBoard)
class PhotoBoardAdmin(admin.ModelAdmin):
    list_display = ["title", "full_name", "email", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "first_name", "last_name", "email", "content"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    date_hierarchy = 'created_at'

    fieldsets = (
        ("기본 정보", {"fields": ("title", "first_name", "last_name", "email")}),
        ("내용", {"fields": ("content", "image")}),
        ("보안", {"fields": ("password",), "classes": ("collapse",)}),
        (
            "시간 정보",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'photo', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ip_address', 'photo__title')
    date_hierarchy = 'created_at'
