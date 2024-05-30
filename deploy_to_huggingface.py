import os
from huggingface_hub import HfApi, HfFolder

def deploy_to_huggingface():
    # Récupérer le token d'authentification de Hugging Face
    hf_token = os.getenv('HF_TOKEN')
    space_name = "tayawelba/ml_cloud_streamlit"

    # Chemin du répertoire contenant les fichiers à télécharger (sauf upload_to_hf.py)
    folder_path = "."

    # Créer un objet HfFolder pour gérer le téléchargement des fichiers
    hf_folder = HfFolder()  # Corrected line

    # Upload de chaque fichier/dossier
    for file_name in os.listdir(folder_path):
        if file_name != "upload_to_hf.py":
            file_path = os.path.join(folder_path, file_name)
            hf_folder.upload(file_path, space_name, token=hf_token)

if __name__ == '__main__':
    deploy_to_huggingface()
