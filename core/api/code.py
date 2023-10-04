import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import albumentations as A
from albumentations.pytorch import ToTensorV2
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np
from PIL import Image
import os
from PIL import Image
from io import BytesIO


def apply_model(classify_rgb):
    datahora = 0
    detected_class_ = str("Nenhuma")
    confclass = 1
    principal_cor = str("Nenhuma")
    principal_confcor = 1
    conf_claro = 1
    conf_escuro = 1
    conf_padrao = 1

    #Converter a imagem de entrada em numpy.array
    image_data = BytesIO(classify_rgb.read())
    frame = Image.open(image_data)

    save_directory_image = os.getcwd() + "\\core\\detect\\image\\"
    save_directory_csv = os.getcwd() + "\\core\\detect\\files_csv\\"
    model_detect = YOLO("core/api/best_detect.pt")
    model_classify = YOLO("core/api/best_classify.pt")
    escala = 6
    espessura = 6
    cor_texto = (255, 255, 255)  # Cor do texto em branco (BGR)

    #O Post da API recebe em "<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>", convertendo:"
    #frame = Image.open(frame)
    #frame = np.array(frame)
    #frame = frame[...,:3][...,::-1]

    results = model_detect(frame)  # Execute o modelo

    if len(results[0]) > 0: #Caso queira pegar mais de um biscoito por vez usar for det in results[0]:
        det = results[0][0]
        bbox = det.boxes.xyxy[:4].cpu().numpy()  # Coordenadas da caixa delimitadora (xmin, ymin, xmax, ymax)
        conf = float(det.boxes.conf.cpu().numpy())   # Confiança da detecção
        class_id = "Biscoito"
        #class_id = det.names[int(det.boxes.cls)]  # ID da classe

        if conf > 0.2:  # Considerar apenas detecções com confiança acima de 0.# Desenhar a caixa delimitadora na imagem
            xmin, ymin, xmax, ymax = map(int,(bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3]))
            imagem_print = frame.copy()
            cropped_image = np.array(imagem_print)[int(ymin):int(ymax), int(xmin):int(xmax)] #np.array para converter

            #Aplicar transformações usando o Albumentations
            transform = A.Compose([
                A.Resize(416, 416),  # Redimensionar para o tamanho do modelo YOLO
                ToTensorV2(),
            ])

            imagem_transformed = transform(image=cropped_image)
            imagem_transformed = imagem_transformed["image"].numpy().transpose(1, 2, 0)

            classify = model_classify.predict(imagem_transformed, show = False)
            classify_imagem_convert = cv2.cvtColor(classify[0].orig_img, cv2.COLOR_BGRA2RGBA)

            conf = float(det[0].boxes.conf.cpu().numpy())   # Confiança da detecção
            class_id = det[0].names[int(det[0].boxes.cls)]  # ID da classe
            detected_class = "Biscoito"  #O modelo foi treinado com o nome trocado, por isso não vamos usar class_id
            label = f"{detected_class} - {conf*100:.2f}%"
            classif = classify[0].names[classify[0].probs.top5[0]]
            conf_classify = classify[0].probs.top5conf[0].item()
            label_classify = f"{classif} - {conf_classify*100:.2f}%"

            cv2.putText(classify_imagem_convert, label, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(classify_imagem_convert, label_classify, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            classify_rgb = classify_imagem_convert[...,:3][...,::-1]

            detected_class_ = str(detected_class)
            confclass = float(conf)
            principal_cor = str(classif)
            principal_confcor = float(conf_classify)
            conf_claro = float(classify[0].probs.data[0].item())
            conf_escuro = float(classify[0].probs.data[1].item())
            conf_padrao = float(classify[0].probs.data[2].item())

    dt_time = ' '.join([datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S')])
    name_file = dt_time.replace(' ', '').replace('-', '').replace(':', '')
    save_path = os.path.join(save_directory_image, f'{name_file}.jpg')
    #cv2.imwrite(save_path, frame)

    return(int(name_file), detected_class_, confclass, principal_cor, principal_confcor, conf_claro, conf_escuro, conf_padrao, classify_rgb)
