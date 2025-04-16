# **SceneProgDatasets**

**SceneProgDatasets** is a easy to use retriver that sources assets from popular datasets based on a simple textual description. 

---

## **Features**
1. **Supported Datasets**
    - 3D-FUTURE
    - HSSD

## **Installation**
To install the package and its dependencies, use the following command:
```bash
pip install sceneprogdatasets
```
Note: Remember to setup .env file (ask from admin) to use the package.

## **Getting Started**
Importing the Package
```python
from sceneprogdatasets import SceneProgAssetRetriever
```

## **Usage Examples**
```python
retriever = SceneProgAssetRetriever()
path = retriever("A simple dining table")
path = retriever("A sandwitch maker")
```
