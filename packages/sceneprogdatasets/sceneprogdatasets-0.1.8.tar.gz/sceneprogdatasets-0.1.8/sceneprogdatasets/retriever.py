from dotenv import load_dotenv
load_dotenv()

class SceneProgAssetRetriever:
    def __init__(self):
       
        import os
        from pathlib import Path
        path = Path(__file__).parent
        
        if not os.path.exists(os.path.join(path, '.env')):
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to create a .env file first!
cp .env {os.path.join(path, '.env')}
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)

        if not os.path.exists(os.path.join(path,'futurehssd/all_metadata.json')) or not os.path.exists(os.path.join(path,'objaverse/compiled.json')):
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to download the assets first!

Run the following commands to download the assets:

aws s3 cp s3://{os.getenv("DATASET_METADATA_REPO")}/futurehssd/ {os.path.join(path,'futurehssd/')} --recursive
aws s3 cp s3://{os.getenv("DATASET_METADATA_REPO")}/objaverse/ {os.path.join(path,'objaverse/')} --recursive
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)
       
        from .futurehssd.futurehssd import AssetRetrieverFutureHSSD 
        from .objaverse.objaverse import AssetRetrieverObjaverse

        self.future_hssd = AssetRetrieverFutureHSSD()
        self.objaverse = AssetRetrieverObjaverse()
    
    def __call__(self, description, context="None"):
        ## first search in Future
        future_hssd_results = self.future_hssd(description, context=context)
        if not future_hssd_results == 'No models found':
            return future_hssd_results
        
        ## then search in OBJAVERSE
        objaverse_results = self.objaverse(description)
        if not objaverse_results == 'No models found':
            return ("OBJAVERSE",objaverse_results)
        
        ## Lastly create the model!
        create_model_results = create_model(description)
        return create_model_results

def create_model(description):
    import os
    import requests
    from scipy.spatial.transform import Rotation as R
    import numpy as np
    import trimesh
    response = requests.post(os.getenv("GENERATE_GLB"), json={"text": description})
    cwd = os.getcwd()
    os.makedirs(f"{cwd}/tmp", exist_ok=True)
    random_name = os.urandom(16).hex()
    path = f"{cwd}/tmp/{random_name}.glb"
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception("Failed to generate 3D model")

    mesh = trimesh.load(path, force="mesh")
    rotation = R.from_euler('y', 30, degrees=True)
    rotation = np.hstack((rotation.as_matrix(), np.array([[0], [0], [0]])))
    rotation = np.vstack((rotation, np.array([0, 0, 0, 1])))
    mesh.apply_transform(rotation)
    mesh.export(path)
    return path