from rest_framework import serializers

from api.models import RawFile, ProcessedFile


class RawFileSerializer(serializers.ModelSerializer):
    """
    Необработанный файл (сериализатор)
    """

    class Meta:
        model = RawFile
        fields = '__all__'
        read_only_fields = ['id','status','processed_file']


class ProcessedFileSerializer(serializers.ModelSerializer):
    """
    Обработанный файл файл (сериализатор)
    """

    class Meta:
        model = ProcessedFile
        fields = '__all__'
        read_only_fields = fields