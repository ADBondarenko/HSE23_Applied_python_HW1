import streamlit as st
import pandas as pd 
import numpy as np
import sqlalchemy
import seaborn as sns
from sqlalchemy import create_engine
import psycopg2
import os
import matplotlib.pyplot as plt

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
engine_pd = create_engine(f"postgresql://{st.secrets.connections.postgresql.username}:{st.secrets.connections.postgresql.password}@{st.secrets.connections.postgresql.host}/{st.secrets.connections.postgresql.database}")
df_full_pd = pd.read_sql('SELECT * FROM D_merged_processed;', engine_pd)
st.subheader('''Построение графиков распределений признаков''')

target_cols = ['age', 'gender', 'child_total',
       'dependants', 'socstatus_work_fl', 'socstatus_pens_fl', 'personal_income',
      'target', 'loan_num_total', 'loan_num_closed']

type_dict = {i : 'float64' for i in target_cols}
df_full_pd = df_full_pd.astype(type_dict)

for tab_col, col in zip(st.tabs(target_cols),target_cols):
    with tab_col:
        tab_col.subheader(f"Распределение признака {col}")
        fig, ax = plt.subplots()
        ax.set_title(f"Гистограмма распределения признака {col}")
        df_full_pd[[col]].hist(ax = ax, legend = True)
        tab_col.pyplot(fig)
        
st.subheader('''Построение матрицы корреляций''') 

corr_matrix = df_full_pd[list([target_cols])].corr()
corr_plot = sns.heatmap(corr_matrix)
st.pyplot(corr_plot)

st.subheader('''Попарное распределение фичей с таргетом''')
for tab_col, col in zip(st.tabs(target_cols.remove('target')),target_cols.remove('target')):
    with tab_col:
        tab_col.subheader(f"Распределение признака {col}")
        
        plot_ = sns.pairplot(df_full_pd[[col, "target"]],
                            diag_kind="kde",
                            x_vars = col, 
                            y_vars = 'target')
        plt.set_title(f"Попарное распределение признака {col} с таргетом")
        tab_col.pyplot(plot_)
        

        
#
# for i in target_cols:
# df_full = conn.query('SELECT * FROM D_merged_processed;', ttl="10m")
# all_widgets = sp.create_widgets(df_full, create_data)
# ignore_columns=["PassengerId"]



