import os
from huggingface_hub import HfApi

def deploy_to_huggingface():
    # Récupérer le token d'authentification de Hugging Face
    hf_token = os.getenv('HF_TOKEN')
    space_name = "tayawelba/ml_cloud_streamlit"

    # Chemin du répertoire contenant les fichiers à télécharger (sauf upload_to_hf.py)
    folder_path = "."

    # Créer une instance de HfApi
    hf_api = HfApi()

    # Upload de chaque fichier/dossier
    for file_name in os.listdir(folder_path):
        if file_name != "upload_to_hf.py":
            file_path = os.path.join(folder_path, file_name)
            # Vérifier si c'est un dossier
            if os.path.isdir(file_path):
                hf_api.upload_folder(
                    folder_path=file_path,
                    path_in_repo=".",
                    repo_id=space_name,
                    token=hf_token,
                    commit_message="Upload folder: " + file_name
                )
            else:
                # Si c'est un fichier, télécharger directement
                with open(file_path, "rb") as f:
                    hf_api.upload_file(
                        repo_id=space_name,
                        filename=file_name,
                        file_obj=f,
                        token=hf_token,
                        commit_message="Upload file: " + file_name
                    )

if __name__ == '__main__':
    deploy_to_huggingface()
