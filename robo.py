from chatterbot import ChatBot
from processar_artigos import get_artigos

import sqlite3

NOME_ROBO = "Robô Bibliotecário Zezinho"
BD_ROBO = "chat.sqlite3"
CAMINHO_BD = "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario"
BD_ARTIGOS = f"{CAMINHO_BD}\\artigos.sqlite3"

CONFIANCA_MINIMA = 0.6

def inicializar():
    sucesso, robo, artigos = False, None, None

    try:
        robo = ChatBot(NOME_ROBO,
            read_only = True, 
            storage_adapter='chatterbot.storage.SQLStorageAdapter', 
            database_uri=f'sqlite:///{BD_ROBO}')
        
        artigos = get_artigos(True)
        
        sucesso = True
    except Exception as e:
        print(f"Erro inicializando o robô: {NOME_ROBO}: {str(e)}")

    return sucesso, robo, artigos

def executar(robo):
    while True:
        mensagem = input("👤: ")
        resposta = robo.get_response(mensagem.lower())

        if(resposta.confidence >= CONFIANCA_MINIMA):
            print(f"🤖: {resposta.text}. Confianca = {resposta.confidence}")
        else:
            print(f"🤖: Infelizmente, ainda não sei responder essa pergunta. Confiança = {resposta.confidence}")
            # registrar a pergunta em um log

def pesquisar_artigos_por_chaves(chaves, artigos):
    encontrou, artigos_selecionados = False, []
    ordem = 1
    for artigo in artigos:
        for chave in chaves:
            chave = chave.strip()
            print(f"artigoAAAAAAAAAAAAAAA: {artigo}")
            if chave and any(chave in c for c in [artigo['chave1'], artigo['chave2'], artigo['chave3'], artigo['chave4'], artigo['chave5'], artigo['chave6'], artigo['chave7']]):
                artigos_selecionados.append({'ordem': ordem, 'titulo': artigo['titulo'], 'artigo': artigo['artigo']})
                encontrou = True
                ordem += 1

    return encontrou, artigos_selecionados        

if __name__ == "__main__":
    sucesso, robo, artigos = inicializar()

    if sucesso:
        executar(robo)