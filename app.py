import streamlit as st
import requests
import time
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
from groq import Groq
from gtts import gTTS
from langdetect import detect
import speech_recognition as sr



#GROQ_API = os.environ.get("GROQ_API")

#changement du logo et du titre de mon application en anglais
st.set_page_config(page_title="Machine Learning Dans le Cloud", page_icon=":brain:", layout="centered", menu_items=None)



# Créer trois colonnes de largeur égale
col1, col2, col3 = st.columns(3)

# Laisser la première et la troisième colonne vides
with col1:
  st.write("")

# Afficher le logo dans la deuxième colonne
with col2:
  st.image("img/logo2.png", use_column_width=None)

with col3:
    st.write("")

selected = option_menu(
            menu_title=None,  # required
            options=["Accueil", "Chatbot : Groq", "Speech to Text", "Text to Speech"],  # required
            icons=["house","chat-dots", "mic","pen" ],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )

if selected == "Accueil":
    st.title(f"{selected}")

    # Display home page with app description and logo
    st.header('Bienvenue dans notre application polyvalente de conversation !')
    st.markdown("<h5 style='text-align: justify;'>Notre application combine trois fonctionnalités principales pour vous offrir une expérience interactive et fluide.</h5>", unsafe_allow_html=True)

    st.image('img/image1.jpeg', caption='Large Language Model')
    #st.title('Bienvenue sur l\'application de classification d\'images de radiographies pulmonaires')
    #st.markdown("<h1 style='text-align: center;'>Bienvenue sur l'application de classification d'images de radiographies pulmonaires</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify;'><b> Chatbot avec Groq : </b> Cette fonctionnalité permet aux utilisateurs d'interagir avec un chatbot alimenté par Groq. Les utilisateurs peuvent saisir des prompts dans une zone de texte et obtenir des réponses générées par le modèle Groq. L'interaction se fait de manière fluide et naturelle, simulant une conversation en langage naturel.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify;'><b> Speech to Text : </b> La fonction Speech to Text permet aux utilisateurs de convertir la parole en texte. En activant cette fonction, les utilisateurs peuvent parler dans leur microphone, et le texte correspondant sera automatiquement transcrit dans une zone de texte. Cela facilite la saisie de prompts ou de messages sans avoir à les taper manuellement.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify;'><b> Text to Speech : </b> La fonction Text to Speech permet aux utilisateurs de convertir du texte en parole. Les utilisateurs peuvent saisir du texte dans une zone dédiée, et en appuyant sur un bouton, le texte sera synthétisé en parole. Cela peut être utile pour écouter les réponses du chatbot ou d'autres messages générés par l\'application.</h5>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: justify;'>Avec ces trois volets, les utilisateurs peuvent interagir avec l'application de différentes manières, que ce soit en saisissant du texte, en parlant dans leur microphone, ou en écoutant les réponses générées par l'application. Cela offre une expérience utilisateur riche et flexible pour répondre à différents besoins et préférences.</h5>", unsafe_allow_html=True)


    components.html(
    """
        <div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; font-size: 15px; color: gray;">
        Tous droits réservés © Main 2024 Tayawelba Dawaï Hesed
        </div>
        """,
        height=50 
    )
if selected == "Chatbot : Groq":
    # Configuration de l'API Groq
    client = Groq(api_key=GROQ_API)

    def get_groq_completion(model, messages, temperature, max_tokens, top_p, stream):
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream
        )
        return completion

    # Fonction pour initialiser l'historique
    def init_chat_history():
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

    # Interface utilisateur
    st.title("Interface de Chat Groq API")

    # Initialiser l'historique des chats
    init_chat_history()

    # Sidebar pour les paramètres
    st.sidebar.header("Paramètres du Modèle")
    model = st.sidebar.selectbox(
        "Choisissez un modèle",
        ["llama3-8b-8192", "llama3-70b-8192", "gemma-7b-it", "mixtral-8x7b-32768"]
    )
    temperature = st.sidebar.slider("Température", 0.0, 1.0, 1.0)
    max_tokens = st.sidebar.slider("Nombre maximum de tokens", 1, 2048, 1024)
    top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0)
    stream = st.sidebar.checkbox("Stream", value=True)

    # Fonction pour envoyer le prompt et obtenir la réponse
    def submit_prompt():
        if st.session_state.prompt.strip() == "":
            st.error("Veuillez entrer un prompt")
        else:
            with st.spinner("Obtention de la réponse de Groq..."):
                messages = [{"role": "user", "content": st.session_state.prompt}]
                try:
                    completion = get_groq_completion(model, messages, temperature, max_tokens, top_p, stream)
                    response = ""
                    for chunk in completion:
                        response += chunk.choices[0].delta.content or ""

                    # Ajouter le prompt et la réponse à l'historique des chats
                    st.session_state['chat_history'].append({"prompt": st.session_state.prompt, "response": response})

                    # Réinitialiser le champ de saisie
                    st.session_state.prompt = ""

                except Exception as e:
                    st.error(f"Erreur: {e}")

    # Afficher l'historique des chats
    st.subheader("Historique des Chats")
    chat_history_container = st.container()
    for chat in st.session_state['chat_history']:
        chat_history_container.markdown(f"**Prompt :** {chat['prompt']}")
        chat_history_container.markdown(f"**Réponse :** {chat['response']}")
        chat_history_container.markdown("---")
    # Champ de texte pour le prompt
    prompt = st.text_area("Enter your prompt here:", key="prompt", on_change=submit_prompt)



if selected == "Speech to Text":
    # CODE SPEECH-TO-TEXT
    st.title(f"{selected}")

    st.markdown("Cette partie vous permet de convertir votre **parole** en **texte**.")

    # Record audio
    with st.spinner("Veuillez parler..."):
        # Initialize recognizer
        r = sr.Recognizer()

        # Use microphone as source
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source)
            st.info("Enregistrement en cours... Parlez maintenant !")
            audio_data = r.listen(source)

        # Speech recognition
        try:
            st.success("Enregistrement terminé ! Voici ce que j'ai compris :")
            recognized_text = r.recognize_google(audio_data, language='fr-FR')  # Language set to French
            st.write(recognized_text)
        except sr.UnknownValueError:
            st.warning("Désolé, je n'ai pas pu comprendre ce que vous avez dit.")
        except sr.RequestError as e:
            st.error(f"Erreur lors de la demande au service de reconnaissance vocale : {e}")

    # Clear button to reset input and result
    if st.button("Nettoyer"):
        st.success("Le champ est nettoyé.")
        st.empty()  # Clear previous results if any

    # Button to allow new speech-to-text conversion
    if st.button("Convertir en texte"):
        st.experimental_rerun()

    # END CODE SPEECH-TO-TEXT


if selected == "Text to Speech":
    # CODE TEXT-TO-SPEECH
    st.title(f"{selected}")

    st.markdown("Cette partie vous offre la possibilité de convertir vos **paragraphes** et vos **phrases** en **parole**.")

    headers = {"Authorization": TOKEN_API}

    # User input for text-to-speech
    tts_input = st.text_area("Entrer le texte à convertir en parole:", "")
    if st.button("Convertir en parole"):
        if tts_input:
            with st.spinner("Conversion en cours..."):
                # Détection de la langue
                language = detect(tts_input)
                # Conversion de texte en parole
                tts = gTTS(text=tts_input, lang=language)
                tts.save("output.mp3")
                st.success("Conversion terminée ! Cliquez ci-dessous pour écouter le résultat.")
                audio_file = open("output.mp3", "rb").read()
                st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Veuillez saisir le texte à convertir en parole.")
    
    # Clear button to reset input and result
    if st.button("Nettoyer"):
        tts_input = ""
        st.success("Le champ est nettoyé.")
        st.empty()  # Clear previous results if any

    # END CODE TEXT-TO-SPEECH

