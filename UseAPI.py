import requests
import cv2

metodo = "GET"

# -----------------------------------------POST------------------------------------------
if metodo == "POST" :
    # -----------------------------------------POST------------------------------------------
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

# -----------------------------------------GET------------------------------------------
if metodo == "GET":
    # Define o ID do elemento que você deseja recuperar
    element_id = 28  # Substitua 1 pelo ID real do elemento que você deseja

    # Define a URL da sua API Django com o ID do elemento
    api_url = f'http://127.0.0.1:8000/applymodel/{element_id}/'

    # Faça uma solicitação GET para a API
    response = requests.get(api_url)

    # Verifique o código de status da resposta
    if response.status_code == 200:
        result = response.json()
        # Faça algo com os dados da resposta
        print(result)
    elif response.status_code == 201:
        # A solicitação POST foi bem-sucedida e um novo recurso foi criado
        # Recupere o URL do recurso criado na resposta
        resource_url = response.headers.get('Location')
        if resource_url:
            # Faça uma solicitação GET para o URL do recurso recém-criado
            resource_response = requests.get(resource_url)
            if resource_response.status_code == 200:
                resource_data = resource_response.json()
                # Faça algo com os dados do recurso recém-criado
                print(resource_data)
            else:
                print('Erro ao acessar o recurso:', resource_response.status_code)
        else:
            print('Não foi possível encontrar o URL do recurso criado.')
    else:
        print('Erro ao acessar a API:', response.status_code)
