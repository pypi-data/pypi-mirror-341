from rest_framework import serializers

from .models import CounterVersionChoices, Platform, Report, SushiService


class CounterReleaseField(serializers.Field):
    def to_representation(self, value):
        return value.to_string()

    def to_internal_value(self, data):
        return CounterVersionChoices.from_string(data)


class SushiServiceSerializer(serializers.ModelSerializer):
    counter_release = CounterReleaseField()

    class Meta:
        model = SushiService
        fields = (
            "id",
            "counter_release",
            "url",
            "ip_address_authorization",
            "api_key_required",
            "platform_attr_required",
            "requestor_id_required",
        )


class ReportSerializer(serializers.ModelSerializer):
    counter_release = CounterReleaseField()

    class Meta:
        model = Report
        fields = ("counter_release", "report_id")


class PlatformSerializer(serializers.ModelSerializer):
    reports = SushiServiceSerializer(many=True, read_only=True)
    sushi_services = serializers.ListField(child=serializers.URLField(), read_only=True)

    class Meta:
        model = Platform
        fields = (
            "id",
            "name",
            "abbrev",
            "reports",
            "content_provider_name",
            "website",
            "sushi_services",
        )
