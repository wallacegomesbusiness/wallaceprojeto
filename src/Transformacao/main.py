#Vamos importas o que precisamos
import pandas as pd
import sqlite3
from datetime import datetime

# Definir o caminh para o arquivo JSONL
df = pd.read_json('../data/data.jsonl', lines=True)

# Setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

# Adicionar a coluna _source com um valor fixo
df['source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Adicionar a coluna _data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()

# Tratar os valores nulos para colunas numéricas e de texto
df['old_prices_reais'] = df['old_prices_reais'].fillna(0).astype(float)
df['old_prices_centavos'] = df['old_prices_centavos'].fillna(0).astype(float)
df['new_prices_reais'] = df['new_prices_reais'].fillna(0).astype(float)
df['new_prices_centavos'] = df['new_prices_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parênteses das colunas 'reviews_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços como floats e calcular os valores totais
df['old_price'] = df['old_prices_reais'] + df['old_prices_centavos'] / 100
df['new_price'] = df['new_prices_reais'] + df['new_prices_centavos'] / 100

# Remover as colunas antigas de preços

df.drop(columns=['old_prices_reais', 'old_prices_centavos', 'new_prices_reais', 'new_prices_centavos'],axis = 1, inplace=True)

# Conectar ao banco de dados SQLite (ou Criar um novo)
conn = sqlite3.connect('../data/quotes.db')

# Salvar o Dataframe no banco de dados SQLite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

print(df.head())


