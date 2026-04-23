import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Contabilità 79€", layout="centered")
st.title("💰 Registrazione Incassi")

# Connessione ufficiale tramite Service Account (configurato nei Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

tipo = st.selectbox("Documento", ["Ricevuta", "Fattura"])
metodo = st.radio("Metodo", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)

if st.button("Registra Pagamento (79.00 €)", width='stretch'):
    try:
        # Legge i dati
        df = conn.read()
        
        # Aggiunge la riga
        nuova_riga = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Tipo": tipo,
            "Metodo": metodo,
            "Importo": 79.00
        }])
        
        df = pd.concat([df, nuova_riga], ignore_index=True)
        
        # Scrive i dati (ora funzionerà!)
        conn.update(data=df)
        st.success(f"Registrata {tipo} via {metodo}!")
        st.balloons()
    except Exception as e:
        st.error(f"Errore: {e}")

st.divider()
st.subheader("Ultimi 5 Movimenti")
try:
    st.dataframe(conn.read().tail(5), width='stretch')
except:
    st.info("In attesa di dati...")
