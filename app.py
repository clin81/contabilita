import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configurazione Pagina
st.set_page_config(page_title="Gestione Cassa 79€", layout="centered")

st.title("💰 Registro Vendite e Cassa")

# Connessione a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONE PER CARICARE I DATI ---
def get_data():
    return conn.read(ttl=0) # ttl=0 forza la lettura dei dati freschi, non salvati in cache

# --- CALCOLO DISPONIBILITÀ CASSA ---
try:
    df_attuali = get_data()
    if not df_attuali.empty:
        # Assicuriamoci che Importo sia un numero
        df_attuali['Importo'] = pd.to_numeric(df_attuali['Importo'], errors='coerce').fillna(0)
        # Somma solo se il metodo è Contanti
        totale_cassa = df_attuali[df_attuali['Metodo'] == 'Contanti']['Importo'].sum()
    else:
        totale_cassa = 0.0
except:
    totale_cassa = 0.0

# Mostra il totale in cassa in alto
st.metric("DISPONIBILITÀ IN CASSA (Contanti)", f"{totale_cassa:.2f} €")
st.divider()

# --- INPUT DATI ---
col1, col2 = st.columns(2)
with col1:
    tipo = st.selectbox("Tipo Documento", ["Ricevuta", "Fattura"])
    metodo = st.radio("Metodo di Pagamento", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)
with col2:
    numero_doc = st.text_input("Numero (Ricevuta/Fattura)", placeholder="es. 01, 02...")

# --- LOGICA DI REGISTRAZIONE ---
if st.button("REGISTRA 79.00 €", width='stretch'):
    if not numero_doc:
        st.error("⚠️ Inserisci il numero del documento prima di registrare!")
    else:
        try:
            # 1. Scarica i dati aggiornati dal foglio
            data = get_data()
            
            # 2. Crea la nuova riga
            nuova_riga = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Tipo": tipo,
                "Numero": numero_doc,
                "Metodo": metodo,
                "Importo": 79.00
            }])
            
            # 3. Attacca la nuova riga a quelle esistenti (Append)
            # Se il foglio era vuoto, il nuovo dataframe sarà solo la nuova riga
            if data.empty:
                updated_df = nuova_riga
            else:
                updated_df = pd.concat([data, nuova_riga], ignore_index=True)
            
            # 4. Carica tutto il blocco aggiornato su Google Sheets
            conn.update(data=updated_df)
            
            st.success(f"✅ {tipo} n. {numero_doc} registrata con successo!")
            st.balloons()
            
            # 5. Riavvia l'app per aggiornare il calcolo della cassa in alto
            st.rerun()
            
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")

st.divider()

# --- TABELLA STORICO ---
st.subheader("Storico Documenti Emessi")
try:
    # Rileggiamo i dati per mostrare lo storico aggiornato
    df_visualizza = get_data()
    if not df_visualizza.empty:
        # Mostriamo dalla più recente alla più vecchia
        st.dataframe(df_visualizza.iloc[::-1], width='stretch')
    else:
        st.info("Nessun documento registrato.")
except:
    st.warning("Impossibile caricare lo storico.")
