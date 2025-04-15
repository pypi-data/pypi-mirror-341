
import os
import json
import trimesh
import numpy as np
from tqdm import tqdm 
from langchain_openai import OpenAIEmbeddings
from sceneprogllm import LLM
from dotenv import load_dotenv
load_dotenv()

FUTURE_PATH_MODELS = os.getenv('FUTURE_PATH_MODELS')
HSSD_PATH_MODELS = os.getenv('HSSD_PATH_MODELS')
FUTURE_PATH_IMAGES = os.getenv('FUTURE_PATH_IMAGES')
HSSD_PATH_IMAGES = os.getenv('HSSD_PATH_IMAGES')

from pathlib import Path
BASE = str(Path(__file__).parent)
embd_location = os.path.join(BASE,'all_embeddings.npz')
metadata_location = os.path.join(BASE,'all_metadata.json')

def get_image_path(assetID):
    if assetID.startswith("future/"):
        assetID = assetID.split("/")[1]
        return os.path.join(FUTURE_PATH_IMAGES, assetID + ".png")
    elif assetID.startswith("hssd/"):
        assetID = assetID.split("/")[1]
        return os.path.join(HSSD_PATH_IMAGES, assetID + ".png")
    else:
        raise ValueError(f"Unknown assetID: {assetID}")
    
class AssetRetrieverFutureHSSD:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))
        data = np.load(embd_location, allow_pickle=True)
        self.all_embeddings = data['all_embeddings']
        self.all_models = data['all_models']

        with open(metadata_location, 'r') as f:
            self.metadata = json.load(f)
        
        self.llm = LLM(
            name="AssetRetrieverFutureHSSD",
            system_desc=f"""
Your task is to help me pick a 3D model by given a few images of candidate models based on the closeness to the query. 
Just responsd with the ID of the model.
""",
        response_format="json",
        json_keys=["name:str"],
        )

    def __call__(self, query, context="None"):
        # Step 1: Embed query and compute similarity
        emb = np.array(self.embeddings.embed_query(query))
        similarity = np.dot(self.all_embeddings, emb)

        # Get top 20 most similar models
        top_indices = np.argsort(similarity)[-20:][::-1]
        top_models = [self.all_models[i] for i in top_indices]
        top_similarities = similarity[top_indices]

        # Step 2: If similarity is too low, reject
        if np.max(top_similarities) < 0.5:
            return "No models found"

        # Normalize similarity to get probabilities (softmax over adjusted scores)
        adjusted_scores = 5 * (top_similarities - 0.4)
        probabilities = np.exp(adjusted_scores) / np.sum(np.exp(adjusted_scores))

        # Step 3: Sample 5 models from the 20, based on their probabilities
        sampled_indices = np.random.choice(len(top_models), size=5, replace=False, p=probabilities)
        sampled_models = [str(top_models[i]) for i in sampled_indices]

        image_paths = [get_image_path(model) for model in sampled_models]
        metadata = ""
        for model in sampled_models:
            metadata += f"""
Model ID: {model}
Description: {self.metadata[model]['description']}
Is there free space on top of the object?: {self.metadata[model]['freetop']}
Typical placement of the object: {self.metadata[model]['placement']}
Can this object be placed on top of or inside another object?: {self.metadata[model]['on_top_or_inside']}
Width of the object in meters: {self.metadata[model]['scale']}
"""
        prompt = f"""
Pick the most relevant model for the query: {query}
Following is some additional context provided by the user to help you make a decision: {context}
Pick from the following models:
{metadata }

Return the ID of the model you think is the best fit.
"""
        response = self.llm(prompt, image_paths=image_paths)
        return response["name"]