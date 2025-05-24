from chatterbot import ChatBot

NOME_ROBO = "Robô Bibliotecário Zezinho"
BD_ROBO = "chat.sqlite3"

CONFIANCA_MINIMA = 0.6

def inicializar():
    sucesso, robo = False, None

    try:
        robo = ChatBot(NOME_ROBO,
            read_only = True, 
            storage_adapter='chatterbot.storage.SQLStorageAdapter', 
            database_uri=f'sqlite:///{BD_ROBO}')
        
        sucesso = True
    except Exception as e:
        print(f"Erro inicializando o robô: {NOME_ROBO}: {str(e)}")

    return sucesso, robo

def executar(robo):
    while True:
        mensagem = input("👤: ")
        resposta = robo.get_response(mensagem.lower())

        if(resposta.confidence >= CONFIANCA_MINIMA):
            print(f"🤖: {resposta.text}. Confiança = {resposta.confidence}")
        else:
            print(f"🤖: Infelizmente, ainda não sei responder essa pergunta. Confiança = {resposta.confidence}")
            # registrar a pergunta em um log

        

if __name__ == "__main__":
    sucesso, robo = inicializar()

    if sucesso:
        executar(robo)