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

# ... (parte iniziale uguale)

if st.button("Registra Pagamento (79.00 €)", width='stretch'):
    try:
        # Carichiamo i dati esistenti
        data = conn.read()
        
        nuova_riga = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Tipo": tipo,
            "Metodo": metodo,
            "Importo": 79.00
        }])
        
        # Unione dati
        updated_df = pd.concat([data, nuova_riga], ignore_index=True)
        
        # Salvataggio
        conn.update(data=updated_df)
        st.success(f"Registrata {tipo} via {metodo}!")
        st.balloons()
    except Exception as e:
        st.error(f"Errore durante il salvataggio: {e}")

st.divider()
st.subheader("Ultimi Movimenti")

# Visualizzazione sicura: se il foglio è vuoto non crasha
st.divider()
st.subheader("Debug Connessione")

try:
    df_visualizzazione = conn.read()
    st.write("Connessione riuscita!")
    st.dataframe(df_visualizzazione.tail(5), width='stretch')
except Exception as e:
    st.error("Errore Tecnico Rilevato:")
    st.code(str(e)) # Questo ci dirà l'errore esatto (es. 403 Forbidden o 404 Not Found)
