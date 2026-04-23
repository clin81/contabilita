import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="Gestione 79€", layout="centered")
st.title("💰 Registrazione Incassi")

# Connessione a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Interfaccia Utente
tipo = st.selectbox("Documento", ["Ricevuta", "Fattura"])
metodo = st.radio("Metodo di Pagamento", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)

# NOTA: Cambiato use_container_width con width='stretch' come richiesto dai log 2026
if st.button("Registra Pagamento (79.00 €)", width='stretch'):
    # Creazione nuovo record
    nuova_riga = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Tipo": tipo,
        "Metodo": metodo,
        "Importo": 79.00
    }])
    
    # Caricamento dati esistenti e aggiunta
    data = conn.read()
    updated_df = pd.concat([data, nuova_riga], ignore_index=True)
    
    # Salvataggio su Google Sheets
    conn.update(data=updated_df)
    st.success(f"Registrata {tipo} via {metodo}!")
    st.balloons()

# Mostra gli ultimi inserimenti
st.divider()
st.subheader("Ultimi Movimenti")
# Anche qui aggiornato il parametro larghezza
st.dataframe(conn.read().tail(5), width='stretch')
