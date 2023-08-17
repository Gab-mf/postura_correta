# postura_correta
Este é um script em Python que utiliza a biblioteca MediaPipe juntamente com o OpenCV para estimar a postura humana a partir do feed da webcam e visualizar pontos de referência-chave no corpo. Ele também calcula o ângulo do tronco como uma aproximação da postura.

![Demo](demo.gif)

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- mediapipe
- opencv-python

Você pode instalá-las usando os seguintes comandos:

```bash
pip install mediapipe
pip install opencv-python

Clone o repositório:

git clone https://github.com/your-username/pose-estimation.git
Navegue até o diretório do projeto:

cd pose-estimation

Execute o script:

python pose_estimation.py
Uma janela aparecerá exibindo o feed da webcam com os pontos de referência da pose estimada e o ângulo do tronco calculado exibido na tela.

Você pode modificar o código para rastrear e visualizar diferentes pontos de referência.
Ajuste as especificações de desenho para alterar a aparência dos pontos de referência e linhas.
Para mais informações sobre os módulos mp_pose e mp_drawing, consulte a documentação oficial do MediaPipe.
Licença

Este projeto está licenciado sob a Licença MIT.

Agradecimentos
Este projeto utiliza a biblioteca MediaPipe do Google.
Sinta-se à vontade para personalizar e melhorar este código conforme necessário. Se você tiver alguma dúvida ou sugestão, fique à vontade para abrir uma issue ou pull request. Feliz codificação!
