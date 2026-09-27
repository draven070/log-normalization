# Cross-Platform Security Log Normalizer 🚧

> **Status: Under Construction 🚧**

A cross-platform security log collection and normalization project currently under active development.

The goal is to build a lightweight security monitoring foundation capable of collecting **Windows and Linux security events in real time**, converting them into a common format, and eventually providing detection, alerting, and visualization capabilities.

---

## 🚧 Current Development

The project is currently focused on building the core log collection and normalization pipeline.

### Currently Working On

* Real-time Windows Security Event collection
* Real-time Linux authentication log collection
* Windows Event XML parsing
* Linux authentication log parsing
* Central Flask API
* API-key based agent authentication
* Common normalized event schema
* JSON-based event storage
* Shared `.env` configuration
* Windows EventRecordID tracking

Current pipeline:

```text
Windows / Linux
      ↓
Real-Time Agent
      ↓
HTTP / JSON
      ↓
Central Flask API
      ↓
Platform Parser
      ↓
Common Event Schema
      ↓
JSON Storage
```

---

## 🏗️ Project Structure

```text
cross-platform-log-normalizer/
│
├── .env
├── .env.example
├── .gitignore
│
├── server/
│   ├── app.py
│   ├── config.py
│   │
│   ├── parsers/
│   │   ├── linux.py
│   │   └── windows.py
│   │
│   ├── normalization/
│   │   ├── schema.py
│   │   └── normalizer.py
│   │
│   └── storage/
│       └── json_store.py
│
├── agents/
│   ├── windows/
│   │   ├── collectors.py
│   │   └── config.py
│   │
│   └── linux/
│       ├── collector.py
│       └── config.py
│
├── output/
│   └── normalized_events.json
│
└── README.md
```

---

## 🔧 Technologies

* Python
* Flask
* Pydantic
* Requests
* Python Dotenv
* Windows Event Log / `wevtutil`
* Linux authentication logs
* XML parsing
* JSON

---

## 🎯 Planned Features

The following features are planned and **not yet fully implemented**:

* [ ] Advanced detection engine
* [ ] Brute-force detection
* [ ] Suspicious authentication detection
* [ ] Event correlation
* [ ] Database storage
* [ ] Security dashboard
* [ ] Real-time alerts
* [ ] Email/Discord notifications
* [ ] IOC extraction and enrichment
* [ ] Threat intelligence integration
* [ ] MITRE ATT&CK mapping
* [ ] Agent health monitoring
* [ ] HTTPS communication
* [ ] Message queue for large-scale ingestion
* [ ] Role-based access control
* [ ] SIEM-style investigation interface

---

## 🧪 Development Status

| Component                    | Status         |
| ---------------------------- | -------------- |
| Project architecture         | 🟡 In Progress |
| Windows real-time collection | 🟢 Working     |
| Linux real-time collection   | 🟡 In Progress |
| Windows event parsing        | 🟢 Working     |
| Linux event parsing          | 🟡 In Progress |
| Central API                  | 🟢 Working     |
| Common schema                | 🟢 Working     |
| JSON storage                 | 🟢 Working     |
| Detection engine             | ⚪ Planned      |
| Database                     | ⚪ Planned      |
| Dashboard                    | ⚪ Planned      |
| Alerting                     | ⚪ Planned      |
| SIEM functionality           | ⚪ Future       |

---

## 🚧 Project Status

This repository is **under active development**.

The architecture, APIs, schemas, configuration, and implementation may change as development progresses.

Features shown in the **Planned Features** section should not be considered implemented.

---

## 🔭 Long-Term Goal

The long-term objective is to evolve this project into a lightweight cross-platform security monitoring/SIEM platform:

```text
Collect
   ↓
Normalize
   ↓
Detect
   ↓
Correlate
   ↓
Enrich
   ↓
Alert
   ↓
Visualize
```

For now, the primary focus is getting the **real-time collection and normalization layer** reliable before moving on to detection and visualization.

---

> **⚠️ Work in Progress**
>
> This project is being developed for learning, research, and authorized security-monitoring environments.
