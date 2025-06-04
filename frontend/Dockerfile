FROM node:20-alpine

WORKDIR /app

# Kopiere package.json und package-lock.json
COPY frontend/package*.json ./

# Installiere Abhängigkeiten
RUN npm install

# Kopiere den restlichen Quellcode
COPY frontend/ .

# Build ausführen
RUN npm run build

# Statisches Serving-Tool installieren
RUN npm install -g serve

EXPOSE 3000

# Stelle sicher, dass der serve-Befehl auf das build-Verzeichnis zeigt
CMD ["serve", "-s", "build", "-l", "3000", "--single"] 
