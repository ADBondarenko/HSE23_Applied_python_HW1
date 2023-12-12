import streamlit as st
import pandas as pd 
import numpy as np
import os

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM D_merged_processed limit 10;', ttl="10m")

# for row in df.itertuples():
#     st.write(f"{row.id} has a :{row.loan_id}:")
st.header('1. Просмотрим сам датафрейм')
st.subheader('''В наличии должны быть колонки     
    - AGREEMENT_RK — уникальный идентификатор объекта в выборке;
    - TARGET — целевая переменная: отклик на маркетинговую кампанию (1 — отклик был зарегистрирован, 0 — отклика не было);
    - AGE — возраст клиента;
    - SOCSTATUS_WORK_FL — социальный статус клиента относительно работы (1 — работает, 0 — не работает);
    - SOCSTATUS_PENS_FL — социальный статус клиента относительно пенсии (1 — пенсионер, 0 — не пенсионер);
    - GENDER — пол клиента (1 — мужчина, 0 — женщина);
    - CHILD_TOTAL — количество детей клиента;
    - DEPENDANTS — количество иждивенцев клиента;
    - PERSONAL_INCOME — личный доход клиента (в рублях);
    - LOAN_NUM_TOTAL — количество ссуд клиента;
    - LOAN_NUM_CLOSED — количество погашенных ссуд клиента.''')
st.dataframe(df, use_container_width=True)

st.header('2. Просмотрим на EDA')
st.subheader('''В наличии должны быть колонки     
* построение графиков распределений признаков
* построение матрицы корреляций
* построение графиков зависимостей целевой переменной и признаков
* вычисление числовых характеристик распределения числовых столбцов (среднее, min, max, медиана и так далее)''')

df_full = conn.query('SELECT * FROM D_merged_processed;', ttl="10m")

df_full_pd = pd.read_sql('SELECT * FROM D_merged_processed;', conn)
df_full_pd_test = pd.DataFrame(df_full)

