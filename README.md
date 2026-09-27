# Cross-Platform Security Log Normalizer

A lightweight, cross-platform security log normalization platform that collects **Linux and Windows security events in real time**, converts them into a common JSON schema, and provides a foundation for future detection and SIEM capabilities.

---

## Architecture

```text
Linux / Windows
      │
      ▼
Real-Time Agents
      │
      │ HTTP / JSON
      ▼
   Flask API
      │
      ▼
Authentication
      │
      ▼
Platform Parsers
      │
      ▼
Common Event Schema
      │
      ▼
Normalized JSON Storage
      │
      ▼
Future Detection / SIEM
```

---

## Current Work

The current implementation focuses on **real-time collection, parsing, normalization, and storage**.

### Implemented

* Linux real-time log collection from `/var/log/auth.log`
* SSH authentication monitoring
* Windows Security Event Log collection
* Windows Event XML parsing
* Central Flask REST API
* API-key authentication
* Linux and Windows platform-specific parsers
* Common normalized event schema
* JSON-based event storage
* Modular agent/server architecture

### Supported Windows Events

| Event ID | Activity                |
| -------: | ----------------------- |
|     4624 | Successful logon        |
|     4625 | Failed logon            |
|     4634 | Logoff                  |
|     4648 | Explicit credential use |
|     4672 | Special privileges      |
|     4688 | Process creation        |
|     4720 | User account created    |
|     4726 | User account deleted    |
|     4740 | Account locked out      |

### Common Event Format

Events from different operating systems are converted into a consistent structure:

```json
{
  "timestamp": "...",
  "source": {
    "type": "linux",
    "host": "...",
    "ip": "..."
  },
  "event": {
    "type": "authentication",
    "action": "login",
    "status": "failed",
    "category": "authentication"
  },
  "user": {
    "name": "admin"
  },
  "network": {
    "src_ip": "192.168.1.10",
    "src_port": 54321,
    "protocol": "ssh"
  },
  "process": {
    "name": "sshd"
  },
  "message": "...",
  "raw_log": "..."
}
```

---

## Project Structure

```text
cross-platform-log-normalizer/
│
├── server/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── parsers/
│   │   ├── linux.py
│   │   └── windows.py
│   ├── normalization/
│   │   ├── schema.py
│   │   └── normalizer.py
│   └── storage/
│       └── json_store.py
│
├── agents/
│   ├── linux/
│   │   ├── collector.py
│   │   ├── config.py
│   │   └── requirements.txt
│   └── windows/
│       ├── collector.py
│       ├── config.py
│       └── requirements.txt
│
├── output/
│   └── normalized_events.json
│
├── samples/
│   └── auth.log
│
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd cross-platform-log-normalizer
```

### 2. Install Server Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 3. Start the Central Server

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

Health check:

```text
GET /api/health
```

---

## Linux Agent

Install dependencies:

```bash
cd agents/linux
pip install -r requirements.txt
```

Configure the server:

```bash
export NORMALIZER_SERVER="http://127.0.0.1:5000"
export NORMALIZER_API_KEY="change-this-key"
```

Start the collector:

```bash
python collector.py
```

The agent monitors:

```text
/var/log/auth.log
```

and forwards new SSH authentication events to the central server.

---

## Windows Agent

Install dependencies:

```powershell
cd agents\windows
pip install -r requirements.txt
```

Configure the server:

```powershell
$env:NORMALIZER_SERVER="http://127.0.0.1:5000"
$env:NORMALIZER_API_KEY="change-this-key"
```

Run:

```powershell
python collector.py
```

The agent collects events from:

```text
Windows Security Event Log
```

and sends them to the central API.

---

## Environment Configuration

The system supports environment-based configuration.

Common variables:

```text
NORMALIZER_SERVER
NORMALIZER_API_KEY
NORMALIZER_REQUEST_TIMEOUT
```

Linux-specific:

```text
LINUX_LOG_FILE
LINUX_POLL_INTERVAL
LINUX_MONITORED_SERVICE
LINUX_AGENT_NAME
```

Windows-specific:

```text
WINDOWS_LOG_NAME
WINDOWS_POLL_INTERVAL
WINDOWS_AGENT_NAME
```

---

## Event Flow

Example Linux event:

```text
SSH Failed Login
      ↓
Linux Agent
      ↓
HTTP POST /api/events
      ↓
Flask API
      ↓
Linux Parser
      ↓
Common Schema
      ↓
JSON Storage
```

Windows follows the same pipeline:

```text
Windows Security Event
      ↓
Windows Agent
      ↓
Flask API
      ↓
Windows Parser
      ↓
Common Schema
      ↓
JSON Storage
```

---

## Current Status

| Component                 | Status        |
| ------------------------- | ------------- |
| Linux real-time collector | ✅ Implemented |
| Windows event collector   | ✅ Implemented |
| Central Flask API         | ✅ Implemented |
| API authentication        | ✅ Implemented |
| Linux parser              | ✅ Implemented |
| Windows parser            | ✅ Implemented |
| Common event schema       | ✅ Implemented |
| JSON storage              | ✅ Implemented |
| Detection engine          | 🔄 Future     |
| Database                  | 🔄 Future     |
| Dashboard                 | 🔄 Future     |
| Alerting                  | 🔄 Future     |
| Threat intelligence       | 🔄 Future     |
| MITRE ATT&CK mapping      | 🔄 Future     |
| Event correlation         | 🔄 Future     |
| Full SIEM functionality   | 🔄 Future     |

---

## Future Work

The project is planned to evolve into a lightweight SIEM platform.

### Detection & Correlation

* Brute-force detection
* Password spraying detection
* Suspicious process detection
* Privilege escalation detection
* Multi-event correlation
* Risk scoring

### Storage & Analytics

* SQLite/PostgreSQL
* Elasticsearch/OpenSearch
* Advanced event search
* Historical analysis

### Security Dashboard

A web dashboard will provide:

* Real-time events
* Security alerts
* Event filtering
* Source IP analysis
* User activity
* Host monitoring
* Risk visualization

### Alerting & Threat Intelligence

Planned integrations include:

* Discord
* Email
* Webhooks
* IOC reputation lookup
* IP/domain enrichment
* MITRE ATT&CK mapping

### Reliability & Security

Future improvements:

* HTTPS/TLS
* Secure agent registration
* Event buffering and retry
* Persistent Windows Event Record IDs
* Agent heartbeat monitoring
* Duplicate-event prevention
* EVTX offline analysis

---

## Long-Term Goal

The long-term goal is to transform the project from a **cross-platform log normalizer** into a lightweight security monitoring platform:

```text
Log Collection
      ↓
Normalization
      ↓
Detection
      ↓
Correlation
      ↓
Risk Scoring
      ↓
Threat Intelligence
      ↓
Alerting
      ↓
Security Dashboard
```

---

## Technologies

* Python
* Flask
* Pydantic
* Requests
* Linux
* Windows Event Log
* REST API
* JSON
* PowerShell
* Git

---

## Security Note

This project is intended for **security monitoring, learning, research, and authorized environments**. Production deployment should additionally use TLS, secure secret management, proper authentication, access controls, persistent storage, and event integrity protections.

## License

This project is intended for educational and security research purposes.
