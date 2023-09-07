from rest_framework import serializers
from .models import DiagramText

class DiagramTextSerialiazer(serializers.ModelSerializer):
    json_user_histories = serializers.JSONField()

    class Meta:
        model = DiagramText
        fields = ["id", "name", "json_user_stories", "id_project", "creation_date"]
