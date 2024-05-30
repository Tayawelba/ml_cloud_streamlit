import os
from huggingface_hub import HfApi, HfFolder

def deploy_to_huggingface():
    # Récupérer le token d'authentification de Hugging Face
    hf_token = os.getenv('HF_TOKEN')
    space_name = "tayawelba/ml_cloud_streamlit"

    # Chemin du répertoire contenant les fichiers à télécharger (sauf upload_to_hf.py)
    folder_path = "."
    # Liste des fichiers à exclure
    exclude_files = ["upload_to_hf.py"]

    # Créer un objet HfFolder pour gérer le téléchargement des fichiers
    hf_folder = HfFolder(folder_path)

    # Upload de chaque fichier/dossier
    for file_name in hf_folder.files():
        if file_name not in exclude_files:
            file_path = hf_folder.full_file_path(file_name)
            hf_folder.push_to_hub(path=file_name, repo_id=space_name, token=hf_token)

if __name__ == '__main__':
    deploy_to_huggingface()
