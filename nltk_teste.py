from nltk import word_tokenize, corpus
from nltk.corpus import floresta, stopwords

TEXTO = "A verdadeira generosidade para com o futuro consiste em dar tudo ao presente" # albert camus

palavras_de_parada = set(stopwords.words('portuguese'))

print(f"palavras de parada: {palavras_de_parada}")

tokens = word_tokenize(TEXTO, language='portuguese')
for token in tokens:
    print(f"token: {token}")

tokens_filtrados = []
for token in tokens:
    if token.lower() not in palavras_de_parada:
        tokens_filtrados.append(token)

print(f"tokens filtrados: {tokens_filtrados}")

classificacoes = {}

for (palavra, classificacao) in floresta.tagged_words():
    classificacoes[palavra.lower()] = classificacao

for token in tokens:
    classificacao = classificacoes.get(token.lower())
    print(f"token: {token} - classificação: {classificacao}")