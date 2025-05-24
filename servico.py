from flask import Flask, Response, request
from robo import *

import json

sucesso, robo = inicializar()
servico = Flask(NOME_ROBO)

INFO = {
    'descricao': 'Robô Bibliotecário Zezinho. Atendimento a usuários de uma biblioteca.',
    'versao': '1.0',
}

@servico.get('/')
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype='application/json')

@servico.get('/alive')
def is_alive():
    return Response(json.dumps({'alive': 'sim' if sucesso else 'não'}), status=200, mimetype='application/json')

@servico.post('/responder')
def get_resposta():
    if sucesso:
        conteudo = request.json
        resposta = robo.get_response(conteudo['pergunta'])

        return Response(json.dumps({'resposta': resposta.text, 'confianca': resposta.confidence}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({'resposta': 'Robô não inicializado', 'confianca': 0}), status=503, mimetype='application/json')

if __name__ == "__main__":
    servico.run(host='0.0.0.0', port=5000, debug=True)