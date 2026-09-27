# Cross-Platform Security Log Normalizer

A Python-based security log normalization system that converts **Linux authentication logs** and **Windows Security Event Logs** into a unified JSON schema.

The project is designed as the foundation of a lightweight **SIEM and security monitoring system**, where logs from different operating systems can be processed using a common structure before detection and analysis.

---

## Overview

Security logs from different operating systems use different formats.

For example, Linux SSH authentication may generate:

```text
Sep 27 08:15:32 server01 sshd[1234]: Failed password for admin from 10.10.10.25 port 52144 ssh2
```

While Windows records authentication failures using structured Security Events such as:

```text
Event ID: 4625
Account Name: administrator
Source Network Address: 10.10.10.25
```

Although both represent an authentication failure, their formats and field names are different.

This project converts both into a **common security event schema**.

```text
                    ┌───────────────────┐
                    │    Linux Logs     │
                    │    auth.log       │
                    └─────────┬─────────┘
                              │
                              ▼
                       Linux Parser
                              │
                              │
                              ▼
                    ┌───────────────────┐
                    │  Common Event     │
                    │      Schema       │
                    └───────────────────┘
                              ▲
                              │
                       Windows Parser
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │ Windows Security  │
                    │      Events       │
                    └───────────────────┘
```

---

## Features

* Linux SSH authentication log parsing
* Windows Security Event normalization
* Common JSON event schema
* Event ID mapping
* User and domain extraction
* Source IP and port extraction
* Process information support
* Authentication success/failure classification
* Original raw log preservation
* Pydantic-based schema validation
* Modular parser architecture
* Extensible detection-engine architecture

---

## Supported Log Sources

| Source                             | Status      |
| ---------------------------------- | ----------- |
| Linux `auth.log`                   | ✅ Supported |
| Windows Security Events            | ✅ Supported |
| Windows Event XML                  | 🔄 Planned  |
| Windows `.evtx`                    | 🔄 Planned  |
| Real-time Windows Event Collection | 🔄 Planned  |
| Detection Engine                   | 🔄 Planned  |
| Security Dashboard                 | 🔄 Planned  |

---

# Architecture

```text
                  RAW LOG SOURCES
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
        Linux auth.log       Windows Security Events
             │                       │
             ▼                       ▼
       Linux Parser           Windows Parser
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
                  Common Schema
                         │
                         ▼
                 Normalized JSON
                         │
                         ▼
                Detection Engine
                         │
                         ▼
                      Alerts
                         │
                         ▼
                    Dashboard
```

---

# Project Structure

```text
log-normalizer/
│
├── app.py
├── requirements.txt
│
├── schema/
│   ├── __init__.py
│   └── event.py
│
├── parsers/
│   ├── __init__.py
│   ├── linux.py
│   └── windows.py
│
├── pipeline/
│   ├── __init__.py
│   └── normalizer.py
│
├── samples/
│   ├── auth.log
│   └── windows_events.json
│
└── output/
    └── normalized.json
```

---

# Common Event Schema

All supported logs are converted into a common structure.

Example:

```json
{
    "timestamp": "2026-09-27T08:15:32+05:45",

    "source": {
        "type": "windows",
        "host": "WIN-SERVER01",
        "ip": null
    },

    "event": {
        "id": 4625,
        "type": "authentication",
        "action": "logon",
        "status": "failed",
        "category": "authentication"
    },

    "user": {
        "name": "administrator",
        "domain": "CORP"
    },

    "network": {
        "src_ip": "10.10.10.25",
        "src_port": 52144,
        "dst_ip": null,
        "dst_port": null,
        "protocol": "TCP"
    },

    "process": {
        "name": null,
        "pid": null,
        "command_line": null
    },

    "message": "An account failed to log on.",

    "raw_log": "..."
}
```

### Main fields

| Field                  | Description               |
| ---------------------- | ------------------------- |
| `timestamp`            | Time of the event         |
| `source.type`          | Log source                |
| `source.host`          | Hostname                  |
| `event.id`             | Original Windows Event ID |
| `event.type`           | General event type        |
| `event.action`         | Action performed          |
| `event.status`         | Success or failure        |
| `event.category`       | Security category         |
| `user.name`            | Username                  |
| `user.domain`          | Domain                    |
| `network.src_ip`       | Source IP                 |
| `network.src_port`     | Source port               |
| `network.dst_ip`       | Destination IP            |
| `network.dst_port`     | Destination port          |
| `network.protocol`     | Network protocol          |
| `process.name`         | Process name              |
| `process.pid`          | Process ID                |
| `process.command_line` | Command line              |
| `message`              | Event description         |
| `raw_log`              | Original event            |

---

# Linux Log Normalization

The Linux parser currently focuses on SSH authentication events from:

```text
/var/log/auth.log
```

Example:

```text
Sep 27 08:15:32 server01 sshd[1234]: Failed password for admin from 10.10.10.25 port 52144 ssh2
```

The parser extracts:

```text
Username
Source IP
Source port
Hostname
Process
Process ID
Timestamp
Authentication status
```

It then converts the event into the common schema.

### Example normalized Linux event

```json
{
    "timestamp": "2026-09-27T08:15:32",

    "source": {
        "type": "linux",
        "host": "server01"
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
        "src_ip": "10.10.10.25",
        "src_port": 52144,
        "protocol": "ssh"
    },

    "process": {
        "name": "sshd",
        "pid": 1234
    }
}
```

---

# Windows Event Normalization

The Windows parser maps important Security Event IDs to common event categories.

| Event ID | Event                       |
| -------: | --------------------------- |
|   `4624` | Successful logon            |
|   `4625` | Failed logon                |
|   `4634` | Logoff                      |
|   `4648` | Explicit credential logon   |
|   `4672` | Special privileges assigned |
|   `4688` | Process creation            |
|   `4720` | User account created        |
|   `4726` | User account deleted        |
|   `4740` | User account locked out     |

For example:

```text
4625
```

is mapped to:

```json
{
    "type": "authentication",
    "action": "logon",
    "status": "failed",
    "category": "authentication"
}
```

While:

```text
4688
```

is mapped to:

```json
{
    "type": "process",
    "action": "process_creation",
    "category": "process"
}
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/log-normalizer.git
cd log-normalizer
```

Replace `<your-username>` with your GitHub username.

## 2. Create a virtual environment

### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```text
Python 3.10+
Pydantic 2.x
```

---

# Usage

The application supports two input types:

```text
linux
windows
```

## Linux

```bash
python app.py linux samples/auth.log output/normalized.json
```

Example output:

```text
[+] Normalized events: 3
[+] Output: output/normalized.json
```

---

## Windows

```bash
python app.py windows samples/windows_events.json output/normalized.json
```

Example output:

```text
[+] Normalized events: 5
[+] Output: output/normalized.json
```

---

# Windows Event Collection

During the initial development stage, Windows events can be exported using PowerShell.

Example:

```powershell
Get-WinEvent -LogName Security -MaxEvents 100 |
ForEach-Object {
    [PSCustomObject]@{
        source = "windows"
        timestamp = $_.TimeCreated.ToString("o")
        event_id = $_.Id
        host = $_.MachineName
        message = $_.Message
    }
} |
ConvertTo-Json -Depth 5 |
Out-File windows_events.json
```

The resulting JSON file can then be passed to the normalizer.

```bash
python app.py windows windows_events.json output/normalized.json
```

> **Note:** The initial PowerShell collector stores the event description in `message`. Future versions will extract structured Windows Event XML fields such as `TargetUserName`, `IpAddress`, `IpPort`, `ProcessName`, and `ProcessId`.

---

# Why JSON/XML Before `.evtx`?

Windows Event Logs are commonly stored as `.evtx` files.

```text
C:\Windows\System32\winevt\Logs\Security.evtx
```

`.evtx` is a binary event-log format rather than a simple text format.

For the first version, the project uses structured event data:

```text
Windows Event
      │
      ▼
PowerShell / Windows API
      │
      ▼
Structured Event
      │
      ▼
JSON
      │
      ▼
Python Parser
      │
      ▼
Common Schema
```

This keeps the initial project focused on **parsing and normalization**.

Direct `.evtx` ingestion is planned as a future feature:

```text
Security.evtx
      │
      ▼
EVTX Parser
      │
      ▼
Windows Event Parser
      │
      ▼
Common Schema
      │
      ▼
Normalized JSON
```

---

# Example: Cross-Platform Normalization

### Linux

```text
Failed password for admin from 10.10.10.25
```

### Windows

```text
Event ID: 4625
User: administrator
Source IP: 10.10.10.25
```

Both can be represented as:

```json
{
    "event": {
        "type": "authentication",
        "action": "login",
        "status": "failed"
    },
    "network": {
        "src_ip": "10.10.10.25"
    }
}
```

This is the main purpose of the project.

Instead of creating separate detection logic for every log format, future detection rules can work against the normalized schema.

---

# Future Detection Engine

The normalized data will eventually feed a detection engine.

Example:

```text
Linux SSH Failed Login
          │
          │
Windows 4625
          │
          ▼
   Common Schema
          │
          ▼
 Authentication Detector
          │
          ▼
 Multiple Failed Attempts
          │
          ▼
      Alert
```

Planned detections include:

* SSH brute-force attempts
* Windows failed-logon bursts
* Account lockouts
* Suspicious process creation
* Privilege-related events
* New account creation
* Suspicious PowerShell execution
* Repeated authentication failures
* Cross-platform authentication attacks

---

# Roadmap

## Phase 1 — Schema

* [x] Design common event schema
* [x] Define event categories
* [x] Define user fields
* [x] Define network fields
* [x] Define process fields
* [x] Add Pydantic validation

## Phase 2 — Linux Parser

* [x] Parse SSH authentication
* [x] Detect successful SSH login
* [x] Detect failed SSH login
* [ ] Add sudo events
* [ ] Add user-management events

## Phase 3 — Windows Parser

* [x] Event ID `4624`
* [x] Event ID `4625`
* [x] Event ID `4634`
* [x] Event ID `4648`
* [x] Event ID `4672`
* [x] Event ID `4688`
* [x] Event ID `4720`
* [x] Event ID `4726`
* [x] Event ID `4740`
* [ ] Extract structured Event XML fields

## Phase 4 — Log Collection

* [x] JSON input
* [ ] Windows Event API
* [ ] Real-time Linux log monitoring
* [ ] Real-time Windows event monitoring
* [ ] `.evtx` ingestion

## Phase 5 — Detection

* [ ] Brute-force detection
* [ ] Authentication anomaly detection
* [ ] Account-lockout detection
* [ ] Suspicious process detection
* [ ] Privilege escalation indicators
* [ ] Alert generation

## Phase 6 — Dashboard

* [ ] Event statistics
* [ ] Event timeline
* [ ] Source IP analysis
* [ ] Authentication monitoring
* [ ] Alert dashboard
* [ ] Search and filtering

---

# Security Considerations

This project is intended for **authorized defensive security monitoring and research**.

Do not commit real production logs to a public repository.

Logs may contain:

* Usernames
* IP addresses
* Hostnames
* Commands
* Authentication information
* Internal infrastructure information

Use sanitized logs for demonstrations.

Recommended `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc

output/*
*.evtx

.env
```

---

# Learning Outcomes

This project provides practical experience with:

* Security log analysis
* Linux authentication logs
* Windows Security Events
* Windows Event IDs
* Log parsing
* Regular expressions
* JSON processing
* Schema design
* Data normalization
* Pydantic
* Python
* PowerShell
* SIEM architecture
* Security detection engineering

---

# Future Architecture

The final goal is to evolve the project into a lightweight security monitoring platform:

```text
                 LOG COLLECTION
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
          Linux              Windows
             │                   │
             └─────────┬─────────┘
                       ▼
                PARSING LAYER
                       │
                       ▼
                 NORMALIZATION
                       │
                       ▼
                 COMMON SCHEMA
                       │
                       ▼
                DETECTION ENGINE
                       │
                 ┌─────┴─────┐
                 ▼           ▼
               ALERTS      EVENTS
                 │           │
                 └─────┬─────┘
                       ▼
                   DASHBOARD
```

---

## License

This project is intended for educational, research, and authorized defensive-security purposes.
