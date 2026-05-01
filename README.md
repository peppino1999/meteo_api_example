# Meteo API - Flask + Open-Meteo

REST API per il meteo basata su Flask e Open-Meteo API.

## 🚀 Quick Start

```powershell
# Build
docker build -t meteo-api .

# Run
docker run -p 5000:5000 meteo-api
```

## 📡 Endpoint

| Metodo | Rotta | Descrizione |
|--------|-------|-------------|
| GET | `/` | Info API |
| GET | `/weather/<city>` | Meteo per città |
| GET | `/weather?city=Rome&lat=41.9&lon=12.5` | Meteo con parametri |

## 🏙️ Città supportate

Rome, Milan, Naples, Turin, Palermo, Genoa, Bologna, Florence, Bari, Catania

## 🐳 Deployment Docker

### Build locale

```powershell
docker build -t meteo-api .
```

### Esecuzione

```powershell
# Modalità base
docker run -d -p 5000:5000 --name meteo meteo-api

# Con limiti memoria
docker run -d -p 5000:5000 --name meteo -m 512m meteo-api
```



### Produzione

```powershell
# Build e run con docker
docker run -d -p 5000:5000 --name meteo meteo-api

# Verifica status
docker ps

# Log
docker logs -f
```

## 🔧 Variabili d'ambiente

| Variabile | Default | Descrizione |
|-----------|---------|-------------|
| `PYTHONOPTIMIZE` | 2 | Ottimizzazione memoria |
| `PORT` | 5000 | Porta applicazione |

## 🧪 Test

```powershell
pip install pytest pytest-cov
pytest -v
```

## 📦 CI/CD

Workflow GitHub Actions in `.github/workflows/ci-cd.yml`:
- Build Docker image
- Linting (flake8)
- Test (pytest)
- Deploy a GitHub Container Registry
