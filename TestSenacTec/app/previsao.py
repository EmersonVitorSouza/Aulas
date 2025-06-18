import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
import sqlite3

def treinar_rede_neural():
    con = sqlite3.connect('banco.db')

    df = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', data) as mes,
            SUM(total) as faturamento
        FROM vendas
        GROUP BY mes
        ORDER BY mes
    """, con)

    con.close()

    df['mes_num'] = range(1, len(df) + 1)  # exemplo: Jan=1, Feb=2...
    X = df[['mes_num']].values
    y = df['faturamento'].values

    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mse')
    model.fit(X_scaled, y_scaled, epochs=500, verbose=0)

    # Previsão para os próximos 3 meses
    novos_meses = np.array([[len(X) + i] for i in range(1, 4)])
    novos_meses_scaled = scaler_x.transform(novos_meses)
    previsoes_scaled = model.predict(novos_meses_scaled)
    previsoes = scaler_y.inverse_transform(previsoes_scaled)

    for i, p in enumerate(previsoes, start=1):
        print(f"Previsão para Mês {len(X) + i}: R${p[0]:.2f}")
    
    return df, previsoes
