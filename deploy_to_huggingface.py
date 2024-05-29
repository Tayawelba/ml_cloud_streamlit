import os
from huggingface_hub import HfApi, upload_folder

def deploy_to_huggingface():
    # Récupérer le token d'authentification de Hugging Face
    hf_token = os.getenv('HF_TOKEN')
    model_path = "model"
    repo_name = "tayawelba/ml_cloud_streamlit"

    # Authentifier
    api = HfApi()
    api.create_repo(repo_name, exist_ok=True, token=hf_token)

    # Upload du modèle en utilisant l'API HTTP
    upload_folder(
        folder_path=model_path,
        path_in_repo=".",
        repo_id=repo_name,
        token=hf_token,
        commit_message="Upload trained model"
    )

if __name__ == '__main__':
    deploy_to_huggingface()
