from rest_framework.viewsets import ModelViewSet
from core.models import ApplyModel
from .serializers import ApplyModelSerializer
from .code import apply_model
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from base64 import b64decode
import numpy as np
import os
import cv2


save_directory_image = os.getcwd() + "\\core\\detect\\image\\"

class ApplyModelViewSet(ModelViewSet):
    queryset = ApplyModel.objects.all()
    serializer_class = ApplyModelSerializer

    def create(self, request, format=None):
        uploaded_file = request.FILES['imagem_input']
        
        (datahora, detected_class_, confclass, principal_cor, principal_confcor, conf_claro, conf_escuro, conf_padrao, classify_rgb,) = apply_model(uploaded_file)

        image_pil = Image.fromarray(classify_rgb)
        image_io = BytesIO()
        image_pil.save(image_io, format='JPEG')  # Você pode ajustar o formato conforme necessário
        image_file = InMemoryUploadedFile(
                        image_io,  # Arquivo de origem
                        None,  # Campo de arquivo (use None para criar manualmente)
                        'image.jpg',  # Nome do arquivo
                        'image/jpeg',  # Tipo de conteúdo MIME
                        image_io.tell,  # Tamanho do arquivo em bytes
                        None  # Codificação de caracteres (use None para binário)
                    )

        # Corrija a criação do objeto Soma, passando o valor de resultado como argumento nomeado.
        applymodel_post = ApplyModel(imagem_input = uploaded_file, datahora = datahora,detect_class = detected_class_,conf_class = confclass,principal_cor = principal_cor,principal_cor_conf = principal_confcor,conf_claro = conf_claro,conf_escuro = conf_escuro,conf_padrao = conf_padrao,imagem_output = image_file)
        applymodel_post.save()

        serializer = ApplyModelSerializer(applymodel_post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)