import streamlit as st
from data_loader import loadData, loadSelect
import plotly.graph_objects as go
import pandas as pd
from prophet import Prophet
import pandas as pd

st.set_page_config(
    page_title="dashboard", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded" 
)

selctBase = loadSelect()

left_column, right_column = st.columns([3,3])

sector = left_column.selectbox('Setor', selctBase)

if sector:
    base = loadData(sector, '1') 
    baseiRF = base

    left_column, right_column = st.columns([2,2])
    container = left_column.container(border=True)
    df = base[['Close']]

    with container:

        print(df)
        mm = df.rolling(window=20).mean()
        dpm = df.rolling(window=20).std()
        sup_band = mm + 2 * dpm
        inf_band = mm - 2 * dpm
        sup_band = sup_band.rename(columns={'Close' : 'superior'})
        inf_band = inf_band.rename(columns={'Close' : 'inferior'})
        bandas_bollinger = df.join(sup_band).join(inf_band)
        bandas_bollinger.dropna(inplace=True)
        compra = bandas_bollinger[bandas_bollinger['Close'] <= bandas_bollinger['inferior']]
        venda = bandas_bollinger[bandas_bollinger['Close'] >= bandas_bollinger['superior']]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=inf_band.index,
                                y=inf_band['inferior'],
                                name='Banda Inferior',
                                line_color='rgba(173,204,255,0.2)'
                                ))

        fig.add_trace(go.Scatter(x=sup_band.index,
                                y=sup_band['superior'],
                                name='Banda Superior',
                                fill='tonexty',
                                fillcolor='rgba(173,204,255,0.2)',
                                line_color='rgba(173,204,255,0.2)'
                                ))

        fig.add_trace(go.Scatter(x=df.index,
                                y=df['Close'],
                                name='Preço Fechamento',
                                line_color='#636EFA'
                                ))

        fig.add_trace(go.Scatter(x=mm.index,
                                y=mm['Close'],
                                name='Media Movel',
                                line_color='#FECB52'
                                ))

        fig.add_trace(go.Scatter(x=compra.index,
                                y=compra['Close'],
                                name='compra',
                                mode='markers',
                                marker=dict(
                                    color='#00CC96',
                                    size=8,
                                )
                                ))

        fig.add_trace(go.Scatter(x=venda.index,
                                y=venda['Close'],
                                name='venda',
                                mode='markers',
                                marker=dict(
                                    color='#EF553B',
                                    size=8,
                                )
                                ))
        st.plotly_chart(fig)
        
       
    container = right_column.container(border=True)
    
    with container:
        baseiRF.index = pd.to_datetime(baseiRF.index) 
        baseiRF['Date'] = baseiRF.index.date

        baseiRF['Posição'] = baseiRF.index.to_series().reset_index(drop=True)

        baseiRF.set_index('Posição', inplace=True)
        baseiRF = baseiRF[['Date', 'Close']]
        df_acao_fec = baseiRF.set_index(pd.DatetimeIndex(baseiRF['Date'].values))
        df_acao_fec.drop('Date', axis=1, inplace=True)
        df_acao_fec['dif'] = df_acao_fec.diff(1)
        df_acao_fec['ganho'] = df_acao_fec['dif'].clip(lower=0).round(2)
        df_acao_fec['perda'] = df_acao_fec['dif'].clip(upper=0).abs().round(2)
        df_acao_fec['mm_ganho'] = df_acao_fec['ganho'].rolling(window=14, min_periods=14).mean()[:14+1]
        df_acao_fec['mm_perda'] = df_acao_fec['perda'].rolling(window=14, min_periods=14).mean()[:14+1]
        for i in range(15, len(df_acao_fec)):
            df_acao_fec['mm_ganho'].iloc[i] = (df_acao_fec['mm_ganho'].iloc[i-1] * (14 - 1) + df_acao_fec['ganho'].iloc[i])/ 14
            df_acao_fec['mm_perda'].iloc[i] = (df_acao_fec['mm_perda'].iloc[i-1] * (14 - 1) + df_acao_fec['perda'].iloc[i])/ 14
            
        df_acao_fec['ifr'] = 100 - (100 / (1 + (df_acao_fec['mm_ganho'] / df_acao_fec['mm_perda'])))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_acao_fec.index, y=df_acao_fec['Close'], mode='lines', name='Close'))

        fig.add_trace(go.Scatter(x=df_acao_fec.index, y=df_acao_fec['ifr'], mode='lines', name='Índice de Força Relativa', line=dict(color='orange')))

        fig.add_shape(type='line', x0=df_acao_fec.index.min(), x1=df_acao_fec.index.max(), y0=30, y1=30, line=dict(color='red', dash='dash'))
        fig.add_shape(type='line', x0=df_acao_fec.index.min(), x1=df_acao_fec.index.max(), y0=70, y1=70, line=dict(color='red', dash='dash'))

        fig.update_layout(title='Close e Índice de Força Relativa', xaxis_title='Data', yaxis_title='Valor')

        st.plotly_chart(fig, use_container_width=True, key='grafico_unique')
    
    if len(base) != 0:
        container = st.container(border=True)
        
        with container:
            new_date = df[['Close']]
            new_date.index = new_date.index.date            

            new_date = new_date.reset_index()

            new_date.rename(columns={'index': 'ds', 'Close': 'y'}, inplace=True)
            
            model = Prophet()
            model.fit(new_date)
            
            future = pd.date_range(start=new_date['ds'].max(), periods=60, freq='D')
            future =  pd.Series(future.strftime('%Y-%m-%d'))
            df_future = pd.DataFrame({'ds': future})
            
            prever = model.predict(df_future)        
            fig = model.plot(prever)
            plotly_fig = go.Figure()

            plotly_fig.add_trace(go.Scatter(
                x=prever['ds'],
                y=prever['yhat'],
                mode='lines',
                name='Previsão',
                line=dict(color='cyan', width=2) 
            ))

            plotly_fig.add_trace(go.Scatter(
                x=prever['ds'],
                y=prever['yhat_lower'],
                mode='lines',
                name='Limite Inferior',
                line=dict(color='red', dash='dash', width=2)
            ))

            plotly_fig.add_trace(go.Scatter(
                x=prever['ds'],
                y=prever['yhat_upper'],
                mode='lines',
                name='Limite Superior',
                line=dict(color='red', dash='dash', width=2)
            ))

            plotly_fig.update_layout(
                template="plotly_dark",  
                plot_bgcolor="rgb(28, 28, 28)",  
                paper_bgcolor="rgb(28, 28, 28)",
                font=dict(color="white"), 
                title="Previsão de Fechamento", 
                title_x=0.5, 
                title_font=dict(size=16, family="Arial, sans-serif", color='white'),  
                xaxis=dict(
                    title="Data", 
                    showgrid=True, 
                    gridcolor="rgb(50, 50, 50)", 
                ),
                yaxis=dict(
                    title="Fechamento",
                    showgrid=True, 
                    gridcolor="rgb(50, 50, 50)",
                ),
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.1, 
                    xanchor="center", 
                    x=0.5, 
                    font=dict(size=12, color="white") 
                ),
            )
                        
            st.plotly_chart(plotly_fig)
            st.plotly_chart(fig)

        

else:
     st.write('Selecione uma ação')