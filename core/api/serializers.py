from rest_framework import serializers
from core.models import ApplyModel

class ApplyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyModel
        fields = ('id', 'imagem_input', 'datahora', 'detect_class', 'conf_class', 'principal_cor', 'principal_cor_conf', 'imagem_output')