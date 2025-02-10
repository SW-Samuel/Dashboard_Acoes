import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data
def loadData(data, time):
    acao = yf.Ticker(f"{data}")
    data = acao.history(period=f'{time}y')
    return data

def loadSelect():
    table = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(table["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers