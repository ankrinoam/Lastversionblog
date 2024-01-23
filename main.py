from openai import OpenAI
import gspread as gspread
import streamlit as st
import os

# Configuration de la clé API OpenAI
from oauth2client.service_account import ServiceAccountCredentials

# Initialisez le client OpenAI avec la nouvelle méthode
openai_client = OpenAI(api_key='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')

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('index.json', scope)
client = gspread.authorize(creds)
sheet = client.open("BlogPhilippe").sheet1
sheet.append_row(["Test", "Ceci est un test"])
st.write("Données testées écrites dans Google Sheets")

def generer_titre(theme):
    prompt_titre = f"Générer un titre captivant pour un article de blog sur le thème : {theme}."
    response_titre = openai_client.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt_titre,
        max_tokens=50
    )
    return response_titre.choices[0].text.strip()

def generer_corps(theme):
    prompt_corps = f"Écrire un corps détaillé pour un article de blog sur le thème : {theme}."
    response_corps = openai_client.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt_corps,
        max_tokens=2000
    )
    return response_corps.choices[0].text.strip()

def generer_conclusion(theme):
    prompt_conclusion = f"Formuler une conclusion concise et pertinente pour un article de blog sur le thème : {theme}."
    response_conclusion = openai_client.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt_conclusion,
        max_tokens=200
    )
    return response_conclusion.choices[0].text.strip()

def sauvegarder_contenu_google_sheet(theme, titre, corps, conclusion):
    data = [theme, titre, corps, conclusion]
    sheet.append_row(data)

st.title('Générateur de contenu de blog avec GPT-4')

theme = st.text_input("Entrez le thème du blog")

if st.button('Générer le titre'):
    st.session_state.titre_genere = generer_titre(theme)

titre_modifie = st.text_area("Modifier le titre ici", st.session_state.titre_genere if 'titre_genere' in st.session_state else '')

if st.button('Générer le corps'):
    st.session_state.corps_genere = generer_corps(theme)

corps_modifie = st.text_area("Modifier le corps du blog ici", st.session_state.corps_genere if 'corps_genere' in st.session_state else '')

if st.button('Générer la conclusion'):
    st.session_state.conclusion_genere = generer_conclusion(theme)

conclusion_modifie = st.text_area("Modifier la conclusion ici", st.session_state.conclusion_genere if 'conclusion_genere' in st.session_state else '')

if st.button('Sauvegarder les modifications'):
    sauvegarder_contenu_google_sheet(theme, titre_modifie, corps_modifie, conclusion_modifie)
    st.success("Le contenu modifié a été sauvegardé avec succès dans Google Sheets.")

