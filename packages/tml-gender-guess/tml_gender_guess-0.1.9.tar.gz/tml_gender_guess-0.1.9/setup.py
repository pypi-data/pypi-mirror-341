from setuptools import setup, find_packages

setup(
    name="tml_gender_guess",
    version="0.1.9",
    description="Gender classification pipeline based on names",
    author="José Ángel Morell",
    packages=find_packages(include=["gender_guess", "gender_guess.*"]),
    include_package_data=True,
    install_requires=[
        "pandas>=2.2.3",
        "tqdm>=4.67.1",
        "scikit-learn>=1.6.1",
        "torch>=2.6.0",
        "transformers>=4.51.1",
        "fastapi>=0.115.12",
        "uvicorn>=0.34.1",
        "nltk>=3.9.1",
        "requests>=2.32.3",
        "regex>=2024.11.6",
        "Unidecode>=1.3.2",
        "nameparser>=1.0.6",
       
        "typing-inspection>=0.4.0",
        "wordsegment>=1.3.1",
        "wordninja>=2.0.0",
    ],
    package_data={
        "gender_guess": ["nameLists/*.csv", "nameLists/*.dict"]
    },
)

