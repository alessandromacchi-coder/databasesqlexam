import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("f1.db", check_same_thread=False)


st.title("visualizzatore e modificatore data f1!")
#st.write("c'è da divertirsi")
st.sidebar.title("menù di scelta per operazioni")
sidebar=st.sidebar.radio("scegli tra le ozpioni", ["ricerca circuiti per nazione", "inserimento di dati"])

def form_nuovo_pilota(conn):
    st.write("inserisci i dati del pilota")
    with st.form("form_pilota"):
        nome = st.text_input("nome*")
        cognome = st.text_input("cognome*")
        codice = st.text_input("codice del pilota (tipo LEC)")
        
        inviato = st.form_submit_button("aggiungiaml")
        
        if inviato:
            if nome and cognome:
                query = "INSERT INTO drivers (name, surname, code) VALUES (?, ?, ?)"
                with conn:
                    conn.execute(query, (nome, cognome, codice))
                    st.success(f"pilota {nome} {cognome} inserito con successo!")
            else:
                st.warning("i parametri con scritto dentro * sono obbligatori!")

def pagina_inserimento(conn):
    st.subheader("aggiungamo nuovi dati")
    tipoinserimento=st.selectbox("che tabella vuoi inserire?",["piloti"])

    match tipoinserimento:
        case "piloti":
            form_nuovo_pilota(conn)

def circuitscountry():
    query = """
        select * from circuits 
        where country = ?
    """
    return query

def ricercacircuiti(conn):
    nazione = st.text_input("inserisci la nazione")
    df = pd.read_sql(circuitscountry(), conn, params=(nazione,))
    if nazione:
        st.dataframe(df)

match sidebar:
    case "ricerca circuiti per nazione":
        ricercacircuiti(conn)
    case "inserimento di dati":
        pagina_inserimento(conn)