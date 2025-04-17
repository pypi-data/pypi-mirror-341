from django.contrib import admin
from django.utils.html import format_html

from .models import Platform, SushiService


class ReportsInline(admin.TabularInline):
    model = Platform.reports.through

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


class SushiServiceInline(admin.TabularInline):
    show_change_link = True
    model = SushiService

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ("name", "abbrev", "id")
    inlines = (SushiServiceInline, ReportsInline)
    list_display = ("id", "abbrev", "name", "registry")
    readonly_fields = ("id", "abbrev", "name")

    def registry(self, obj: Platform):
        return format_html(f'<a href="{obj.registry_url}">Registry</a>')

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False


@admin.register(SushiService)
class SushiServicemAdmin(admin.ModelAdmin):
    search_fields = ("url", "id")
    list_display = (
        "id",
        "url",
        "linked",
        "ip_address_authorization",
        "api_key_required",
        "platform_attr_required",
        "requestor_id_required",
    )

    readonly_fields = ("id", "url", "counter_release", "platform")

    @admin.display(boolean=True, ordering="linked")
    def linked(self, obj):
        return obj.linked

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def get_actions(self, *args, **kwargs):
        return []
