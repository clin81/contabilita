import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gestione Cassa 79€", layout="centered")

st.title("💰 Registro Vendite e Cassa")

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl=0)

# --- CALCOLO DISPONIBILITÀ CASSA ---
try:
    df_attuali = get_data()
    if not df_attuali.empty:
        df_attuali['Importo'] = pd.to_numeric(df_attuali['Importo'], errors='coerce').fillna(0)
        totale_cassa = df_attuali[df_attuali['Metodo'] == 'Contanti']['Importo'].sum()
    else:
        totale_cassa = 0.0
except:
    totale_cassa = 0.0

st.metric("DISPONIBILITÀ IN CASSA (Contanti)", f"{totale_cassa:.2f} €")
st.divider()

# --- INPUT DATI ---
col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Tipo Documento", ["Ricevuta", "Fattura"])
    
    # LOGICA DISABILITAZIONE: Se è ricevuta, mostra solo Contanti e Bancomat
    if tipo == "Ricevuta":
        opzioni_pagamento = ["Contanti", "Bancomat"]
    else:
        opzioni_pagamento = ["Contanti", "Bancomat", "RiBa", "Bonifico"]
        
    metodo = st.radio("Metodo di Pagamento", opzioni_pagamento, horizontal=True)

with col2:
    # Mostra il campo numero solo se necessario (Fattura SEMPRE, Ricevuta solo se BANCOMAT)
    if tipo == "Fattura" or (tipo == "Ricevuta" and metodo == "Bancomat"):
        numero_doc = st.text_input("Numero Documento", placeholder="Inserisci numero...")
    else:
        numero_doc = ""
        st.write("📌 Per le ricevute in contanti il numero non è richiesto.")

# --- LOGICA DI REGISTRAZIONE ---
if st.button("REGISTRA 79.00 €", width='stretch'):
    # Controllo validità: se il campo è visibile, deve essere compilato
    if (tipo == "Fattura" or (tipo == "Ricevuta" and metodo == "Bancomat")) and not numero_doc:
        st.error("⚠️ Inserisci il numero del documento!")
    else:
        try:
            data = get_data()
            
            nuova_riga = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Tipo": tipo,
                "Numero": numero_doc, # Sarà vuoto se Ricevuta + Contanti
                "Metodo": metodo,
                "Importo": 79.00
            }])
            
            if data.empty:
                updated_df = nuova_riga
            else:
                updated_df = pd.concat([data, nuova_riga], ignore_index=True)
            
            conn.update(data=updated_df)
            
            st.success(f"✅ Registrazione effettuata!")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")

st.divider()

# --- TABELLA STORICO ---
st.subheader("Storico Documenti")
try:
    df_visualizza = get_data()
    if not df_visualizza.empty:
        st.dataframe(df_visualizza.iloc[::-1], width='stretch')
except:
    st.info("Nessun dato presente.")
