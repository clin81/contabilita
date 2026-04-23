import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Contabilità 79€", layout="centered")

st.title("💰 Registro Incassi & Cassa")

# Connessione automatica tramite Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOGICA DI CALCOLO CASSA ---
try:
    df_storico = conn.read()
    if not df_storico.empty:
        # Calcoliamo il totale dei contanti (Fatture + Ricevute)
        totale_cassa = df_storico[df_storico['Metodo'] == 'Contanti']['Importo'].sum()
    else:
        totale_cassa = 0.0
except:
    totale_cassa = 0.0

# Visualizzazione Cassa in evidenza
st.metric("DISPONIBILITÀ IN CASSA (Contanti)", f"{totale_cassa:.2f} €")
st.divider()

# --- FORM DI INSERIMENTO ---
col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Tipo Documento", ["Ricevuta", "Fattura"])
    metodo = st.radio("Metodo di Pagamento", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)

with col2:
    # Campo per il numero fattura o ricevuta
    numero_doc = st.text_input("Numero Documento", placeholder="Es. 12/A o 45")

# Pulsante di registrazione
if st.button("REGISTRA 79.00 €", width='stretch'):
    if not numero_doc:
        st.warning("Per favore, inserisci il numero del documento prima di salvare.")
    else:
        try:
            df = conn.read()
            
            nuova_riga = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Tipo": tipo,
                "Numero": numero_doc, # Nuovo campo
                "Metodo": metodo,
                "Importo": 79.00
            }])
            
            updated_df = pd.concat([df, nuova_riga], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success(f"Registrata {tipo} n. {numero_doc} via {metodo}")
            st.balloons()
            # Forza il refresh per aggiornare la cassa
            st.rerun()
        except Exception as e:
            st.error(f"Errore: {e}")

st.divider()

# --- VISUALIZZAZIONE DATI ---
st.subheader("Ultimi inserimenti")
try:
    dati_mostra = conn.read()
    if not dati_mostra.empty:
        # Mostriamo le ultime 10 righe ordinate per la più recente
        st.dataframe(dati_mostra.tail(10), width='stretch')
    else:
        st.info("Nessun dato presente.")
except:
    st.info("Configurazione in corso...")
