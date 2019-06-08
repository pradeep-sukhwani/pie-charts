from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from core.models import IdMapping, Report


class IdMappingSerializer(ModelSerializer):

    class Meta:
        model = IdMapping
        fields = ('id', 'name',)


class ReportSerializer(ModelSerializer):
    students = IdMappingSerializer()

    class Meta:
        model = Report
        fields = '__all__'
