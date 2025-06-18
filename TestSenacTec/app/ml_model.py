import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def prever_faturamento():
    # Conexão com o banco
    con = sqlite3.connect('vendas.db')
    
    # Coletar faturamento por mês
    df = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', data) as mes,
            SUM(total) as faturamento
        FROM vendas
        GROUP BY mes
        ORDER BY mes
    """, con)
    
    con.close()
    
    # Converter meses em números para regressão
    df['mes_num'] = np.arange(len(df))

    # Separar dados
    X = df[['mes_num']]
    y = df['faturamento']

    # Treinar modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Prever próximo mês
    proximo_mes = [[len(df)]]
    previsao = modelo.predict(proximo_mes)[0]

    return {
        'proximo_mes': df['mes'].iloc[-1],
        'previsao': round(previsao, 2),
        'historico': df.to_dict(orient='records')
    }
