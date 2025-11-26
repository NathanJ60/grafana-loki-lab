# Grafana Loki Lab - Stack d'Observabilité

Projet de démonstration d'une stack d'observabilité complète avec Grafana, Loki, Promtail et un générateur de logs fake.

## Architecture

```
Fake Log Generator (Python/Faker)
└── Écrit dans /logs/app.log
    │
    ▼
Promtail (Log Shipper)
└── Lit les logs
└── Extrait les labels (level, scope)
└── Envoie à Loki
    │
    ▼
Loki (Log Store)
└── Stocke et indexe par labels
└── Expose une API de requêtes
    │
    ▼
Grafana (WebUI)
└── Visualisation
└── Requêtes LogQL
```

## Pré-requis

- Docker
- Docker Compose

## Installation

```bash
git clone https://github.com/NathanJ60/grafana-loki-lab.git
cd grafana-loki-lab
docker-compose up -d
```

## Utilisation

### Accéder à Grafana

1. Ouvrir http://localhost:3000 (ou http://IP_SERVEUR:3000)
2. Login : `admin` / `admin`
3. Aller dans **Connections** → **Data Sources** → **Add data source**
4. Sélectionner **Loki**
5. URL : `http://loki:3100`
6. Cliquer **Save & Test**

### Explorer les logs

Aller dans **Explore** et tester :

```logql
{job="fakeapp"}
```

Filtrer par level :
```logql
{job="fakeapp", level="ERROR"}
```

Filtrer par scope :
```logql
{job="fakeapp", scope="auth"}
{job="fakeapp", scope="database", level="ERROR"}
```

## Labels disponibles

Promtail extrait automatiquement ces labels de chaque ligne de log :

| Label | Valeurs | Description |
|-------|---------|-------------|
| `job` | fakeapp | Nom du job (statique) |
| `level` | DEBUG, INFO, WARNING, ERROR, CRITICAL | Niveau de log |
| `scope` | auth, database, api, storage, payment, system, other | Catégorie du log |

### Scope

Le scope est déterminé automatiquement selon le contenu du message :

- **auth** : login, session, authentication, token
- **database** : query, connection, database
- **api** : API call, request, endpoint, rate limit
- **storage** : file, cache, disk
- **payment** : payment, order
- **system** : memory, SSL, certificate, exception

## Format des logs

```
[2025-11-26 10:30:45] INFO - User john_doe logged in successfully
[2025-11-26 10:30:46] ERROR - Failed to connect to database: Connection refused
[2025-11-26 10:30:47] WARNING - High memory usage detected: 85%
```

Distribution des levels :
- DEBUG: 10%
- INFO: 50%
- WARNING: 20%
- ERROR: 15%
- CRITICAL: 5%

Toutes les ~100 logs, il y a 30% de chance d'un burst d'incident (20-50 ERROR/CRITICAL).

## Structure du projet

```
grafana-loki-lab/
├── docker-compose.yml
├── loki/
│   └── loki-config.yaml
├── promtail/
│   └── promtail-config.yaml
├── generator/
│   ├── Dockerfile
│   ├── generate_logs.py
│   └── requirements.txt
├── logs/
│   └── .gitkeep
└── README.md
```

## Commandes utiles

```bash
# Lancer la stack
docker-compose up -d

# Voir les logs de tous les services
docker-compose logs -f

# Arrêter la stack
docker-compose down

# Rebuild après modifs
docker-compose up -d --build

# Logs d'un service spécifique
docker-compose logs -f fakeapp
docker-compose logs -f promtail
docker-compose logs -f loki
```

## Configuration

### Loki

Modifier `loki/loki-config.yaml` pour :
- Changer la rétention
- Modifier les limites d'ingestion
- Configurer le stockage

### Promtail

Modifier `promtail/promtail-config.yaml` pour :
- Ajouter des chemins de logs
- Créer de nouveaux labels
- Modifier les pipeline stages

### Générateur de logs

Modifier `generator/generate_logs.py` pour :
- Ajouter des messages custom
- Changer la distribution des levels
- Modifier la fréquence des incidents

## Troubleshooting

### Loki ne démarre pas
Vérifier les permissions du volume :
```bash
docker-compose logs loki
```

### Les logs n'apparaissent pas dans Grafana
1. Vérifier que Promtail lit bien les logs :
```bash
docker-compose logs promtail
```

2. Vérifier que Loki reçoit les logs :
```bash
curl http://localhost:3100/loki/api/v1/labels
```

### Voir les labels disponibles
```bash
curl http://localhost:3100/loki/api/v1/labels
curl http://localhost:3100/loki/api/v1/label/scope/values
```
