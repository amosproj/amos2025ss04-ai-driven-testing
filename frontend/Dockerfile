FROM node:20-alpine

WORKDIR /app

# Abhängigkeiten installieren
COPY frontend/package*.json ./
RUN npm install

# Quellcode kopieren und Build ausführen
COPY frontend/ .
RUN npm run build

# Statisches Serving-Tool installieren und bereitstellen
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"] 
