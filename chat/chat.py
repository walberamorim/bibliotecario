from flask import Flask, render_template, Response, request, session
import requests
import json

import secrets

URL_ROBO = "http://localhost:5000"
URL_ROBO_ALIVE = f"{URL_ROBO}/alive"
URL_ROBO_RESPONDER = f"{URL_ROBO}/responder"
URL_ROBO_PESQUISAR_ARTIGOS = f"{URL_ROBO}/artigos"

CONFIANCA_MINIMA = 0.65

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def acessar_robo(url, para_enviar = None):
    sucesso, resposta = False, None

    try:
        if para_enviar:
            resposta = requests.post(url, json=para_enviar)
        else:
            resposta = requests.get(url)
        resposta = resposta.json()

        sucesso = True
    except Exception as e:
        print(f"erro ao fazer requisição: {str(e)}")    

    return sucesso, resposta

def robo_alive():
    sucesso, resposta = acessar_robo(URL_ROBO_ALIVE)

    return sucesso and resposta["alive"] == "sim"

def perguntar_robo(pergunta):
    mensagem = "Ainda não sei responder esta pergunta. Por favor, tente de novo"

    sucesso, resposta = acessar_robo(URL_ROBO_RESPONDER, {"pergunta": pergunta})
    if sucesso and resposta["confianca"] >= CONFIANCA_MINIMA:
        mensagem = resposta["resposta"]
    return mensagem

    return mensagem, pesquisar_artigos

def pesquisar_artigos(chaves):
    artigos_selecionados = []

    sucesso, resposta = acessar_robo(URL_ROBO_PESQUISAR_ARTIGOS, {"chave1": chaves[0], "chave2": chaves[1], "chave3": chaves[2], "chave4": chaves[3], "chave5": chaves[4], "chave6": chaves[5], "chave7": chaves[6]})
    if sucesso:
        artigos = resposta["artigos"]
        if artigos:
            ordem = 1
            for artigo in artigos:
                artigos_selecionados.append({"id": artigo["id"], "titulo": f"{ordem} - {artigo["titulo"]}" , "artigo": artigo["artigo"]})
                ordem += 1
    
    return artigos_selecionados

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/responder")
def get_resposta():
    resposta = ''

    conteudo = request.json
    pergunta = conteudo['pergunta']

    resposta = perguntar_robo(pergunta)

    return Response(
        json.dumps({"resposta": resposta}),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5001,
        debug=True
    )
