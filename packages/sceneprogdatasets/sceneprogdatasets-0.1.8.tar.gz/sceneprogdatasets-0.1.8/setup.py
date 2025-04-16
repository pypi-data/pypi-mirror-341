from setuptools import setup, find_packages
setup(
    name="sceneprogdatasets",  # Package name
    version="0.1.8",            # Version number
    author="Kunal Gupta",
    author_email="k5gupta@ucsd.edu",
    description="A dataset retriever for SceneProg project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KunalMGupta/sceneprogdatasets.git",  # Update with actual URL
    packages=find_packages(include=["sceneprogdatasets", "sceneprogdatasets.*"]),
    include_package_data=True,  # Ensures compiled.json is included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Define minimum Python version
    install_requires=[
        'sceneprogllm',
        'scipy',
        'trimesh'
    ],
)