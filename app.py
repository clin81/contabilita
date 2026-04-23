import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURAZIONE ---
# INCOLLA QUI IL TUO LINK DI GOOGLE SHEETS
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/IL_TUO_ID_FOGLIO/edit?usp=sharing"
# ----------------------

st.set_page_config(page_title="Gestione 79€", layout="centered")
st.title("💰 Registrazione Incassi")

# Inizializziamo la connessione
conn = st.connection("gsheets", type=GSheetsConnection)

# Interfaccia
tipo = st.selectbox("Documento", ["Ricevuta", "Fattura"])
metodo = st.radio("Metodo", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)

if st.button("Registra Pagamento (79.00 €)", width='stretch'):
    try:
        # Leggiamo passando l'URL direttamente (risolve l'errore Spreadsheet must be specified)
        data = conn.read(spreadsheet=URL_FOGLIO)
        
        nuova_riga = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Tipo": tipo,
            "Metodo": metodo,
            "Importo": 79.00
        }])
        
        updated_df = pd.concat([data, nuova_riga], ignore_index=True)
        
        # Salviamo specificando l'URL
        conn.update(spreadsheet=URL_FOGLIO, data=updated_df)
        st.success(f"Registrata {tipo} via {metodo}!")
        st.balloons()
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")

st.divider()
st.subheader("Ultimi Movimenti")

try:
    # Anche qui leggiamo con l'URL diretto
    df_visualizzazione = conn.read(spreadsheet=URL_FOGLIO)
    if not df_visualizzazione.empty:
        st.dataframe(df_visualizzazione.tail(5), width='stretch')
    else:
        st.info("Il foglio è attualmente vuoto.")
except Exception as e:
    st.warning("Verifica che il link del foglio sia corretto e che sia impostato su 'Editor' per chiunque abbia il link.")
    st.code(str(e))
