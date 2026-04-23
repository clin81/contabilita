import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Contabilità 79€", layout="centered")

st.title("💰 Registro Incassi 79.00€")

# Connessione automatica tramite Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Form di inserimento
with st.container():
    tipo = st.selectbox("Tipo Documento", ["Ricevuta", "Fattura"])
    metodo = st.radio("Metodo di Pagamento", ["Contanti", "Bancomat", "RiBa", "Bonifico"], horizontal=True)
    
    # Pulsante con stile 2026
    if st.button("REGISTRA PAGAMENTO", width='stretch'):
        try:
            # Lettura dati attuali
            df = conn.read()
            
            # Creazione nuova riga
            nuova_riga = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Tipo": tipo,
                "Metodo": metodo,
                "Importo": 79.00
            }])
            
            # Aggiornamento
            updated_df = pd.concat([df, nuova_riga], ignore_index=True)
            conn.update(data=updated_df)
            
            st.success(f"Salvato con successo: {tipo} - {metodo}")
            st.balloons()
        except Exception as e:
            st.error(f"Errore durante il salvataggio: {e}")

st.divider()

# Visualizzazione dati
st.subheader("Ultimi 10 inserimenti")
try:
    dati_totali = conn.read()
    if not dati_totali.empty:
        st.dataframe(dati_totali.tail(10), width='stretch')
        
        # Un piccolo extra: Totale del giorno
        oggi = datetime.now().strftime("%d/%m/%Y")
        totale_oggi = dati_totali[dati_totali['Data'].str.contains(oggi)]['Importo'].sum()
        st.metric("Totale registrato oggi", f"{totale_oggi:.2f} €")
    else:
        st.info("Il foglio è vuoto. Registra il primo pagamento!")
except:
    st.warning("Configurazione in corso...")
