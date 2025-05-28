FROM continuumio/miniconda3

WORKDIR /app

# Environment-Datei kopieren
COPY backend/environment.yml ./environment.yml

# Erstelle die Conda-Umgebung
RUN conda env create -f environment.yml

# Aktiviere die Conda-Umgebung
RUN echo "conda activate backend" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Kopiere den Anwendungscode in das Package-Verzeichnis
COPY backend ./backend

# Starte die Anwendung
CMD ["conda", "run", "--no-capture-output", "-n", "backend", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 
