from setuptools import setup, find_packages

setup(
    name="dd21006UNO",
    version="0.1.1",
    author="Steven Duran",
    author_email="dd21006@ues.edu.sv",  # Cambia esto por tu correo real
    description="Librería para resolver sistemas de ecuaciones lineales y no lineales con métodos clásicos.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stevenduran/dd21006UNO",  # Cambia esto por el link real de tu repo
    packages=find_packages(exclude=["tests*", "docs*"]),  # Excluye directorios que no son necesarios
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # O la que elijas
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
