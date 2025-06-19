# 🔊 Projeto Alexa + Flask – Automação e Monitoramento Climático

Este projeto integra a assistente virtual **Alexa** com um servidor Flask em Python, permitindo a interação por voz com funcionalidades como:
- Consulta ao **clima atual** usando a API OpenWeather
- Listagem de **dispositivos inteligentes** com consumo e prioridade
- Alteração de **prioridade de dispositivos** via comandos de voz

---

## 🚀 Funcionalidades

### 📍 Previsão do Tempo
> "Alexa, qual o clima hoje?"

- A Alexa responde com:
  - Temperatura
  - Sensação térmica
  - Umidade
  - Velocidade do vento

### 📋 Listar Dispositivos
> "Alexa, me mostre os dispositivos"

- Os dispositivos são lidos de arquivos `.json`
- A Alexa lista o nome, consumo (em watts) e prioridade de cada um

### 🛠️ Alterar Prioridade
> "Alexa, mude a prioridade da geladeira para 2"

- O valor da prioridade do dispositivo é alterado diretamente no arquivo JSON

---

## 🧱 Estrutura do Projeto

```
📁 alexa/
 ┣ 📁 dispositivos/             # Arquivos JSON com dados dos dispositivos
 ┃ ┗ 📄 geladeira.json
 ┣ 📄 app.py                    # Código principal com intents e endpoints
 ┣ 📄 services.py               # Funções auxiliares para manipular arquivos e API
 ┣ 📄 intents.json              # Modelo de interação da Alexa (intents)
 ┣ 📄 requirements.txt          # Dependências do projeto
 ┗ 📁 venv/                     # Ambiente virtual Python (isolado)
```

---

## 🔧 Pré-requisitos

- Python 3.6+
- Conta na [Amazon Developer Console](https://developer.amazon.com/)
- Conta na [OpenWeather](https://openweathermap.org/api) para obter uma API key
- [ngrok](https://ngrok.com/) instalado para expor o servidor local

---

## 📥 Instalação e Execução

1. Clone o repositório e entre na pasta:
```bash
git clone https://github.com/seu-usuario/alexa-flask-projeto.git
cd alexa-flask-projeto
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate   # No Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor Flask:
```bash
python app.py
```

5. Em outro terminal, inicie o ngrok:
```bash
ngrok http 5000
```

> Copie o link HTTPS gerado e use na configuração do endpoint HTTPS da Alexa no Developer Console.

---

## 🗣️ Como funciona com a Alexa?

1. Crie uma skill no [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
2. Configure o `invocationName` (ex: "weather app")
3. Importe o `intents.json` no modelo de interação
4. Aponte o endpoint HTTPS para o link do ngrok
5. Teste os comandos na aba “Test”

---

## 💾 Exemplo de JSON de Dispositivo

`dispositivos/geladeira.json`
```json
{
  "nome": "geladeira",
  "consumo": 150,
  "prioridade": 2
}
```

---

## 🤖 Tecnologias Utilizadas

- **Python 3**
- **Flask**
- **Flask-Ask**
- **ngrok**
- **OpenWeather API**
- **Alexa Developer Console**

---

## 📹 Sugestão de Demonstração em Vídeo

1. Explicar o uso do `venv` e `ngrok`
2. Mostrar o funcionamento do comando de clima
3. Mostrar a listagem dos dispositivos por voz
4. Alterar a prioridade de um dispositivo com comando
5. Mostrar o JSON sendo atualizado automaticamente

---

## 📜 Licença

Este projeto está licenciado sob a MIT License – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ✨ Autor

Desenvolvido por **Enzo Araújo**

Entre em contato para dúvidas ou sugestões!