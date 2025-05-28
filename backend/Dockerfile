FROM continuumio/miniconda3

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere zuerst nur die environment.yml
COPY backend/environment.yml /app/backend/

# Erstelle und aktiviere die Conda-Umgebung
RUN conda env create -f /app/backend/environment.yml
RUN echo "conda activate backend" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Kopiere den gesamten Backend-Code
COPY backend /app/backend/

# Setze Arbeitsverzeichnis auf das Backend-Verzeichnis
WORKDIR /app/backend

# Starte die FastAPI-Anwendung
CMD ["conda", "run", "--no-capture-output", "-n", "backend", "python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 
