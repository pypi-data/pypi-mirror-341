from setuptools import setup, find_packages

setup(
    name="hermes-ai",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "joblib",
        "nltk",
        "numpy",
        "pandas",
        "scikit-learn",
    ],    
    author="Jose Ruben Maldonado Herrera",
    author_email="rub.maler.22@gmail.com",
    description="A ML model to classify messages, reply and summarize conversations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Talos-IA-Lab/hermes",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)