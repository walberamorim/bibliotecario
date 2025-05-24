from nltk import word_tokenize, corpus
from nltk.corpus import floresta, stopwords

from string import punctuation
from collections import Counter

import sqlite3
import os

CAMINHO_ARTIGOS = "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario\\artigos"
CAMINHO_BD = "C:\\Users\\WAA-HP\\Documents\\posweb\\bibliotecario"
BD_ARTIGOS = f"{CAMINHO_BD}\\artigos.sqlite3"

REMOVIVEIS_LATEX = [
    "\\textbf",
    "\\textit",
    "}",
    "{",
]

CLASSES_GRAMATICAIS_INDESEJADAS = [
    "adv",
    "v-inf",
    "v-fin",
    "v-pcp",
    "v-ger",
    "num",
    "adj"
]

FREQUENCIA_MINIMA = 2
PALAVRAS_CHAVE_POR_ARTIGO = 7

MAXIMO_ARTIGOS = 1000

def inicializar():
    palavras_de_parada = set(stopwords.words('portuguese'))

    classificacoes = {}
    for (palavra, classificacao) in floresta.tagged_words():
        classificacoes[palavra.lower()] = classificacao

    return palavras_de_parada, classificacoes

def ler_conteudo(artigo):
    sucesso, conteudo = False, None

    try:
        with open(artigo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        sucesso = True
    except Exception as e:
        print(f"Erro ao ler o artigo: {artigo}: {str(e)}")
    return sucesso, conteudo

def extrair_titulo(conteudo):
    marcador = "\\title{"
    marcador = conteudo.index(marcador) + len(marcador)

    titulo = conteudo[marcador:]
    titulo = titulo[:titulo.index("}")]

    return titulo


def extrair_resumo(conteudo):
    marcador_inicio, marcador_fim = "\\begin{resumo}", "\\end{resumo}"
    marcador_inicio = conteudo.index(marcador_inicio) + len(marcador_inicio)
    marcador_fim = conteudo.index(marcador_fim)
    resumo = conteudo[marcador_inicio:marcador_fim]
    return resumo

def eliminar_palavras_de_parada(tokens, palavras_de_parada):
    tokens_filtrados = []
    for token in tokens:
        if token.lower() not in palavras_de_parada:
            tokens_filtrados.append(token)
    return tokens_filtrados

def eliminar_removiveis_latex(tokens):
    tokens_filtrados = []
    for token in tokens:
        if token not in REMOVIVEIS_LATEX:
            tokens_filtrados.append(token)
    return tokens_filtrados

def eliminar_pontuacao(tokens):
    tokens_filtrados = []
    for token in tokens:
        if token not in punctuation:
            tokens_filtrados.append(token)
    return tokens_filtrados

def eliminar_classes_gramaticais_indesejadas(tokens, classificacoes):
    tokens_filtrados = []
    for token in tokens:
        if token in classificacoes.keys():
            classificacao = classificacoes[token]
            if not any (s in classificacao for s in CLASSES_GRAMATICAIS_INDESEJADAS):
                tokens_filtrados.append(token)
        else:
            tokens_filtrados.append(token)
    return tokens_filtrados

def eliminar_frequencias_baixas(tokens):
    frequencias = Counter(tokens)
    tokens_filtrados = []
    for token, frequencia in frequencias.most_common():
        if frequencia >= FREQUENCIA_MINIMA:
            tokens_filtrados.append(token)
    return tokens_filtrados

def iniciar_banco_artigos():
    if os.path.exists(BD_ARTIGOS):
        os.remove(BD_ARTIGOS)    

    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS artigos (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, artigo TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS chaves (id INTEGER PRIMARY KEY AUTOINCREMENT, id_artigo INTEGER, chave1 TEXT, chave2 TEXT, chave3 TEXT, chave4 TEXT, chave5 TEXT, chave6 TEXT, chave7 TEXT, FOREIGN KEY(id_artigo) REFERENCES artigos(id))")
    conexao.commit()
    conexao.close()

def gravar_artigo(id, titulo, chaves, artigo):
    conexao = sqlite3.connect(BD_ARTIGOS)
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO artigos (id, titulo, artigo) VALUES (?, ?, ?)", (id, titulo, artigo))

    # Garante que chaves tenha exatamente 7 elementos
    chaves = (chaves + [""] * PALAVRAS_CHAVE_POR_ARTIGO)[:PALAVRAS_CHAVE_POR_ARTIGO]

    cursor.execute("INSERT INTO chaves (id_artigo, chave1, chave2, chave3, chave4, chave5, chave6, chave7) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (id, *chaves))

    conexao.commit()
    conexao.close()

def get_artigos(como_linhas = False):
    conexao = sqlite3.connect(BD_ARTIGOS)
    print("como_linhas: ", como_linhas)
    if (como_linhas):
        conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute("SELECT id_artigo, titulo, artigo, chave1, chave2, chave3, chave4, chave5, chave6, chave7 FROM artigos, chaves WHERE chaves.id_artigo = artigos.id")
    artigos = cursor.fetchall()

    for artigo in artigos:
        print(f"ID: {artigo[0]}, Título: {artigo[1]}")
        cursor.execute("SELECT * FROM chaves WHERE id_artigo = ?", (artigo[0],))
        chaves = cursor.fetchone()
        print(f"Chaves: {chaves[1:] if chaves else None}")

    conexao.close()
    return artigos

if __name__ == "__main__":
    palavras_de_parada, classificacoes = inicializar()
    iniciar_banco_artigos()
    for contador in range(1, MAXIMO_ARTIGOS):
        artigo = f"{CAMINHO_ARTIGOS}\\{contador}.tex"
        if os.path.exists(artigo):
            sucesso, conteudo = ler_conteudo(artigo)

            if sucesso:
                titulo = extrair_titulo(conteudo)
                print(f"artigo: {artigo}")
                resumo = extrair_resumo(conteudo)
                print(f"resumo: {resumo}")
                tokens = word_tokenize(resumo, language='portuguese')
                tokens = eliminar_palavras_de_parada(tokens, palavras_de_parada)
                tokens = eliminar_removiveis_latex(tokens)
                tokens = eliminar_pontuacao(tokens)
                tokens = eliminar_classes_gramaticais_indesejadas(tokens, classificacoes)
                tokens = eliminar_frequencias_baixas(tokens)
                print(f"tokens: {tokens}")
                gravar_artigo(contador, titulo, tokens, conteudo)
        else:
            print(f"artigo: {artigo} não encontrado")
            break
    print("Artigos gravados no banco: ")
    get_artigos()