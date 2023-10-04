import requests
import cv2

# Define a URL da sua API Django
api_url = 'http://127.0.0.1:8000/applymodel/'

# Define o caminho para o arquivo da imagem que você deseja enviar
image_path = r"C:\Users\ekt92712\ProjPython\TestesReCor\Input\Claro 3.jpg"
image = cv2.imread(image_path)

# Verifica se a imagem foi lida com sucesso
if image is not None:
    # Codificar a imagem em bytes
    _, encoded_image = cv2.imencode('.jpg', image)

    # Crie um dicionário com os dados que você deseja enviar, neste caso, a imagem codificada
    data = {'imagem_input': ('image.jpg', encoded_image.tobytes())}

    # Faça uma solicitação POST para a API com os dados da imagem
    response = requests.post(api_url, files=data)

    # Verifique o código de status da resposta
    if response.status_code == 200:
        result = response.json()
        # Faça algo com os dados da resposta
        print(result)
    else:
        print('Erro ao acessar a API:', response.status_code)
else:
    print('Erro ao ler a imagem.')
