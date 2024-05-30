import os
from huggingface_hub import HfApi, upload_folder

def deploy_to_huggingface():
    # Récupérer le token d'authentification de Hugging Face
    hf_token = os.getenv('HF_TOKEN')
    repo_name = "tayawelba/ml_cloud_streamlit"

    # Authentifier
    api = HfApi()
    api.create_repo(repo_name, exist_ok=True, token=hf_token)

    # Chemin du répertoire contenant les fichiers à télécharger (sauf upload_to_hf.py)
    folder_path = "."
    # Liste des fichiers à exclure
    exclude_files = ["upload_to_hf.py"]

    # Créer une liste de tous les fichiers et dossiers dans le répertoire (sauf ceux à exclure)
    files_to_upload = [file for file in os.listdir(folder_path) if file not in exclude_files]

    # Upload de chaque fichier/dossier
    for file_name in files_to_upload:
        file_path = os.path.join(folder_path, file_name)
        # Vérifier si c'est un dossier
        if os.path.isdir(file_path):
            upload_folder(
                folder_path=file_path,
                path_in_repo=file_name,
                repo_id=repo_name,
                token=hf_token,
                commit_message="Upload folder: " + file_name
            )
        else:
            # Si c'est un fichier, télécharger directement
            with open(file_path, "rb") as f:
                api.upload_file(repo_name, file_name, f, token=hf_token, commit_message="Upload file: " + file_name)

if __name__ == '__main__':
    deploy_to_huggingface()
