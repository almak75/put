import streamlit as st
import pandas as pd
import numpy as np
import time
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


@st.cache_data
def load_data():
    df = pd.read_csv('putin_sp.csv', encoding='utf8', sep=';')
    df.fillna(0, inplace=True)
    return df

@st.cache_data
def kind_of_words():
    d = {
    'существительное':['NOUN'],
    'прилагательное':['ADJF','ADJS'],
    'компаратив':['COMP'],
    'глагол':['VERB','INFN'],
    'причастие':['PRTF', 'PRTS'],
    'деепричастие':['GRND'],
    'числительное':['NUMR'],
    'наречие':['ADVB'],
    'местоимение':['NPRO'],
    'предикатив':['PRED'],
    'предлог':['PREP'],
    'союз':['CONJ'],
    'частица':['PRCL'],
    'междометие':['INTJ']
    }
    #anti_d = { v:k for k,v in d.items()}
    return d

st.set_page_config(layout="wide")
df = load_data()
kind_of_words = kind_of_words()



st.header('В.В. Путин 2012-2023. Статистика слов в посланиях Федеральному Собранию.')

kw = st.multiselect('Выберите часть речи', kind_of_words.keys(),['существительное', 'прилагательное','глагол'])
years = st.multiselect('Укажите год:', ['2012','2013','2014','2015','2016','2018','2019','2020','2021','2023'],['2012','2013','2014','2015','2016','2018','2019','2020','2021','2023'])
txt = st.text_input(label='Фильтр по конкретному слову', ) 
unicum = st.checkbox('оставить только уникальные слова (сказанные единожды)')


if txt:
    norm_txt = morph.parse(txt)[0].normal_form
    st.text(f'Нормализованная форма слова {txt}: {norm_txt}')
    df=df[df['word']==norm_txt]

if kw:
    #st.write(kw)
    
    filter = []
    for item in kw:
        filter.extend(kind_of_words[item])
    #st.write(filter)
    df = df[df['kind_word'].isin(filter)] 
  
    
all_years = ['2012','2013','2014','2015','2016','2018','2019','2020','2021','2023']
if years:
    
    for_del = [y for y in all_years if y not in years]
    df.drop(for_del, inplace=True,axis=1)
    df['sum']=0
    for y in years:
        df['sum'] = df['sum'] +  df[y]
else:
    df['sum']=0
    for y in all_years:
        df['sum'] = df['sum'] +  df[y]

if unicum:
    df =df[df['sum']==1]


df.drop(['kind_word'], inplace=True,axis=1)
if df.shape[0]==0:
    st.header('ПУСТО. Проверьте не противоречат ли фильтры друг другу.')
else:
    df = df[df['sum']!=0]
    col = df.columns[1:-1]
 
    #st.write(df.style.highlight_max(axis=1, subset=col))
    st.write(df)
    st.text(f'Всего слов {df.shape[0]}')
