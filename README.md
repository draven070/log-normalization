# Cross-Platform Security Log Normalizer

A lightweight, cross-platform security log collection and normalization system designed as a foundation for a Security Information and Event Management (SIEM) platform.

The project collects security-related logs from **Windows and Linux systems**, sends them to a centralized Flask server, normalizes different log formats into a **common structured schema**, and stores the resulting events as JSON for further security analysis.

The current implementation focuses on:

* Windows Security Event Log collection
* Linux systemd journal collection
* Linux authentication log collection
* Centralized log ingestion
* API-key authentication
* Cross-platform log parsing
* Common event normalization
* JSON-based event storage
* Environment-based configuration

The project is designed to be extended with detection rules, correlation, alerting, threat intelligence, dashboards, and automated security analysis.

---

## 1. Project Overview

Security logs are generated in different formats depending on the operating system and service.

For example, Windows Security Event Logs contain structured XML events:

```text
EventRecordID
Provider
EventID
Level
TimeCreated
Computer
EventData
```

Linux authentication logs are generally text-based:

```text
Sep 28 10:32:15 kali sshd[1234]: Failed password for root from 192.168.1.10 port 51234 ssh2
```

Analyzing these logs directly becomes difficult when multiple operating systems are involved.

This project solves the first part of that problem by converting heterogeneous security logs into a common structure.

### Basic concept

```text
                  ┌──────────────────────┐
                  │      Windows Host    │
                  │                      │
                  │ Windows Security Log │
                  └──────────┬───────────┘
                             │
                             │ Windows Agent
                             ▼
                     ┌───────────────┐
                     │               │
                     │  Flask API    │
                     │               │
                     │ Authentication│
                     │      +        │
                     │  Ingestion    │
                     └───────┬───────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Log Normalizer   │
                    │                  │
                    │ Windows Parser   │
                    │ Linux Parser     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Common Schema    │
                    │                  │
                    │ timestamp        │
                    │ source           │
                    │ event             │
                    │ user              │
                    │ network          │
                    │ process           │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ JSON Event Store │
                    └──────────────────┘


                  ┌──────────────────────┐
                  │      Linux Host      │
                  │                      │
                  │ systemd journal     │
                  │ /var/log/auth.log   │
                  │ /var/log/secure     │
                  └──────────┬───────────┘
                             │
                             │ Linux Agent
                             └──────────────► Flask API
```

---

# 2. Goals

The main goals of this project are:

1. Collect security logs from different operating systems.
2. Provide a centralized ingestion point.
3. Authenticate agents before accepting events.
4. Parse operating-system-specific log formats.
5. Convert different logs into a common schema.
6. Store normalized events in a structured format.
7. Provide a foundation for future SIEM functionality.

---

# 3. Current Features

## Windows Log Collection

The Windows agent collects events from the Windows Security Event Log using:

```powershell
wevtutil
```

The agent queries the Security log and retrieves events in XML format.

The XML event is then converted into JSON and sent to the Flask server.

---

## Linux Log Collection

The Linux agent currently supports two major sources.

### systemd Journal

The agent follows the systemd journal using:

```bash
journalctl -f
```

This allows the agent to receive new log entries as they occur.

### Authentication Log Files

The agent can monitor:

```text
/var/log/auth.log
/var/log/secure
```

depending on the Linux distribution.

The file collector behaves similarly to:

```bash
tail -f
```

It waits for new log lines and sends them to the server.

---

# 4. Supported Linux Security Events

The Linux parser currently recognizes events such as:

### Failed SSH Login

Example:

```text
Failed password for root from 192.168.1.50 port 43210 ssh2
```

Normalized as:

```json
{
  "event": {
    "type": "authentication",
    "action": "login",
    "status": "failed",
    "category": "authentication"
  }
}
```

### Successful SSH Login

Example:

```text
Accepted password for kali from 192.168.1.50 port 43210 ssh2
```

### Successful Public Key Login

Example:

```text
Accepted publickey for kali from 192.168.1.50 port 43210 ssh2
```

### Invalid User Login

Example:

```text
Failed password for invalid user admin from 192.168.1.50 port 43210 ssh2
```

### Local Password Authentication Failure

Example:

```text
unix_chkpwd: password check failed for user kali
```

### Sudo Authentication Failure

Example:

```text
pam_unix(sudo:auth): authentication failure; user=kali
```

---

# 5. Windows Security Events

The Windows agent collects events from:

```text
Windows Security Event Log
```

The collected Windows event is passed to the Windows parser and converted into the common normalized schema.

The architecture allows additional Windows Event IDs and security events to be mapped later.

---

# 6. Common Normalized Schema

One of the most important parts of the project is the common schema.

Instead of storing Windows and Linux events in completely different formats, the system converts them into a consistent structure.

A normalized event conceptually looks like:

```json
{
  "timestamp": "2026-09-28T10:32:15",
  "source": {
    "type": "linux"
  },
  "event": {
    "type": "authentication",
    "action": "login",
    "status": "failed",
    "category": "authentication"
  },
  "user": {
    "name": "root"
  },
  "network": {
    "src_ip": "192.168.1.50",
    "src_port": 43210,
    "protocol": "ssh"
  },
  "process": {
    "name": "sshd"
  },
  "message": "Failed password for root from 192.168.1.50 port 43210 ssh2",
  "raw_log": "..."
}
```

This makes it easier to build detection and correlation logic later.

---

# 7. Project Architecture

The project is divided into three major layers.

## Layer 1 — Agents

Agents run on monitored systems.

```text
agents/
├── linux/
└── windows/
```

Their responsibilities are:

* Collect logs
* Track new events
* Package events
* Authenticate with the server
* Send events to the API

---

## Layer 2 — Central Server

The Flask server provides the centralized ingestion layer.

```text
server/
├── app.py
├── config.py
├── parsers/
├── normalization/
└── storage/
```

Its responsibilities are:

* Receive events
* Authenticate agents
* Identify the log source
* Parse logs
* Normalize events
* Store normalized events

---

## Layer 3 — Storage

The current storage implementation uses JSON.

```text
output/
└── normalized_events.json
```

This is intentionally simple at the current stage.

A database such as PostgreSQL, Elasticsearch, OpenSearch, or ClickHouse can be introduced later.

---

# 8. Project Structure

```text
log_normalizer/
│
├── agents/
│   │
│   ├── linux/
│   │   ├── collectors.py
│   │   ├── config.py
│   │   ├── journal.py
│   │   ├── file_collector.py
│   │   └── requirements.txt
│   │
│   └── windows/
│       ├── collectors.py
│       └── config.py
│
├── server/
│   ├── app.py
│   ├── config.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── linux.py
│   │   └── windows.py
│   │
│   ├── normalization/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   └── normalizer.py
│   │
│   └── storage/
│       ├── __init__.py
│       └── json_store.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── output/
│   └── normalized_events.json
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── ...
```

### Important

The real `.env` file is intentionally excluded from Git.

The repository only contains:

```text
.env.example
```

with placeholder values.

---

# 9. Technology Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python                 |
| API Server           | Flask                  |
| Data Validation      | Pydantic               |
| Windows Collection   | wevtutil               |
| Linux Collection     | journalctl / log files |
| Communication        | HTTP/JSON              |
| Authentication       | API Key                |
| Storage              | JSON                   |
| Configuration        | python-dotenv          |
| HTTP Client          | requests               |
| Operating Systems    | Windows + Linux        |
| Version Control      | Git                    |

---

# 10. Setup From Scratch

## 10.1 Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd log_normalizer
```

---

# 11. Python Environment

It is recommended to use a virtual environment.

## Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## Linux

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

---

# 12. Install Server Dependencies

Install the required Python packages.

For example:

```bash
pip install flask pydantic python-dotenv requests
```

If a `requirements.txt` is added for the server in the future, install using:

```bash
pip install -r requirements.txt
```

---

# 13. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`.

Example:

```env
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

NORMALIZER_SERVER=http://127.0.0.1:5000
NORMALIZER_API_KEY=change-this-to-a-long-random-secret
NORMALIZER_REQUEST_TIMEOUT=5

OUTPUT_FILE=output/normalized_events.json

WINDOWS_LOG_NAME=Security
WINDOWS_POLL_INTERVAL=1.0
WINDOWS_AGENT_NAME=windows-agent-01

LINUX_AGENT_NAME=linux-agent-01
LINUX_POLL_INTERVAL=0.5

LINUX_ENABLE_JOURNAL=true
LINUX_ENABLE_AUTH_LOG=true

LINUX_AUTH_LOG_PATH=/var/log/auth.log
LINUX_SECURE_LOG_PATH=/var/log/secure
```

---

# 14. API Key

The server and agents use the same API key.

For example:

```env
NORMALIZER_API_KEY=your-long-random-secret
```

The Linux and Windows agents must use the same key when communicating with the server.

The key is transmitted using:

```http
X-API-Key: your-secret
```

Never commit the real `.env` file to GitHub.

---

# 15. Start the Central Server

From the project root:

```bash
python server/app.py
```

The server should start on:

```text
http://0.0.0.0:5000
```

The server listens on all interfaces so remote agents can connect.

---

# 16. Test Server Health

From the server machine:

```bash
curl http://127.0.0.1:5000/api/health
```

Expected response:

```json
{
  "service": "cross-platform-log-normalizer",
  "status": "online"
}
```

---

# 17. Windows Agent Setup

The Windows agent runs on the Windows machine whose security logs need to be collected.

Make sure Python is installed.

Navigate to:

```powershell
cd agents\windows
```

Install dependencies if required:

```powershell
pip install requests python-dotenv
```

Configure the Windows environment variables.

The Windows agent needs:

```env
NORMALIZER_SERVER=http://127.0.0.1:5000
NORMALIZER_API_KEY=your-secret
WINDOWS_LOG_NAME=Security
WINDOWS_POLL_INTERVAL=1.0
WINDOWS_AGENT_NAME=windows-agent-01
```

If the server is running on another machine, replace `127.0.0.1` with the server's IP address.

For example:

```env
NORMALIZER_SERVER=http://192.168.127.1:5000
```

Run the collector:

```powershell
python collectors.py
```

The agent will continuously monitor Windows Security events.

---

# 18. Linux Agent Setup

The Linux agent can run on a Linux VM or physical Linux machine.

Example:

```bash
cd agents/linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The requirements include:

```text
requests
python-dotenv
```

Configure the Linux agent:

```env
NORMALIZER_SERVER=http://192.168.127.1:5000
NORMALIZER_API_KEY=your-secret

LINUX_AGENT_NAME=linux-agent-01
LINUX_POLL_INTERVAL=0.5

LINUX_ENABLE_JOURNAL=true
LINUX_ENABLE_AUTH_LOG=true

LINUX_AUTH_LOG_PATH=/var/log/auth.log
LINUX_SECURE_LOG_PATH=/var/log/secure
```

Replace:

```text
192.168.127.1
```

with the IP address of the machine running the Flask server.

Run:

```bash
python3 collectors.py
```

---

# 19. Linux Permissions

Some Linux log sources require elevated privileges.

If the agent cannot access:

```text
/var/log/auth.log
```

or:

```text
journalctl
```

run it with appropriate permissions:

```bash
sudo python3 collectors.py
```

The exact permissions required depend on the Linux distribution and its journal configuration.

---

# 20. Network Connectivity

The architecture requires the agents to communicate with the central server over TCP port:

```text
5000
```

For example:

```text
Linux VM
192.168.127.X
      │
      │ HTTP :5000
      ▼
Windows Server
192.168.127.1
      │
      ▼
Flask API
```

Test connectivity from Linux:

```bash
curl http://192.168.127.1:5000/api/health
```

If this works, the Linux machine can reach the server.

---

# 21. How the Project Works

The complete processing pipeline is:

```text
                    LOG SOURCE
                        │
          ┌─────────────┴─────────────┐
          │                           │
       Windows                       Linux
          │                           │
    Security Log              journalctl/auth.log
          │                           │
          ▼                           ▼
    Windows Agent                Linux Agent
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
                  HTTP POST /api/events
                        │
                        ▼
                 API Key Validation
                        │
                        ▼
                  Source Detection
                        │
             ┌──────────┴──────────┐
             │                     │
       Windows Parser        Linux Parser
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                 Common Schema
                        │
                        ▼
                 JSON Event Store
                        │
                        ▼
              normalized_events.json
```

---

# 22. Step-by-Step Processing

## Step 1 — Log Generation

An operating system generates a security event.

Example Linux event:

```text
Failed password for root from 192.168.1.50 port 43210 ssh2
```

---

## Step 2 — Agent Collection

The Linux agent receives the new log line.

The source is identified as:

```text
systemd-journal
```

or:

```text
/var/log/auth.log
```

---

## Step 3 — Event Transmission

The agent creates a JSON payload:

```json
{
  "agent": "linux-agent-01",
  "source": "systemd-journal",
  "message": "Failed password for root from 192.168.1.50 port 43210 ssh2"
}
```

It sends the event to:

```text
POST /api/events
```

---

# 23. API Authentication

The server checks:

```http
X-API-Key
```

against:

```env
NORMALIZER_API_KEY
```

If the key is incorrect:

```http
401 Unauthorized
```

is returned.

This prevents unauthorized clients from sending events to the ingestion API.

---

# 24. Log Normalization

The server identifies the source:

```python
source = data.get("source")
```

For Linux sources, the raw message is passed to:

```text
LinuxAuthParser
```

For Windows events, the event is passed to:

```text
WindowsEventParser
```

The parser extracts useful information such as:

```text
Timestamp
Username
Source IP
Source Port
Protocol
Process
Event Type
Action
Status
```

---

# 25. Common Event Model

After parsing, both Windows and Linux events are converted into the common:

```text
NormalizedLog
```

structure.

This is important because future detection rules can work against the normalized event rather than needing separate detection logic for every operating system.

For example, a future detection rule could simply check:

```text
event.type == authentication
event.status == failed
```

without caring whether the original event came from Windows or Linux.

---

# 26. Event Storage

The normalized event is stored in:

```text
output/normalized_events.json
```

The JSON storage implementation is handled by:

```text
server/storage/json_store.py
```

The current JSON storage is intended for development and prototyping.

For production-scale deployment, a proper event database should eventually replace it.

---

# 27. API Endpoints

## Health Check

```http
GET /api/health
```

Example:

```bash
curl http://127.0.0.1:5000/api/health
```

---

## Event Ingestion

```http
POST /api/events
```

Required header:

```http
X-API-Key: your-secret
```

Example request:

```json
{
  "agent": "linux-agent-01",
  "source": "systemd-journal",
  "message": "Failed password for root from 192.168.1.50 port 43210 ssh2"
}
```

---

# 28. Error Handling

The server currently handles several common conditions.

### Invalid API Key

```http
401 Unauthorized
```

### Invalid JSON

```http
400 Bad Request
```

### Unsupported Source

The server returns an error for unsupported log sources.

### Parsing Failure

Events that do not match currently supported patterns can be ignored rather than being incorrectly normalized.

---

# 29. Configuration Design

Configuration is separated from the source code using environment variables.

This provides several benefits:

* Secrets are not hardcoded.
* Server addresses can change without modifying code.
* Different environments can use different settings.
* Agent names can be configured independently.
* Polling intervals can be adjusted.

The project uses:

```text
python-dotenv
```

to load `.env` values.

---

# 30. Security Considerations

The current implementation includes basic security controls.

### API Authentication

Agents must provide:

```text
X-API-Key
```

### Secrets Outside Git

Real credentials are stored in:

```text
.env
```

and excluded through:

```text
.gitignore
```

### Raw Event Preservation

The normalized event retains the original log message through:

```text
raw_log
```

This is useful for later forensic analysis and parser debugging.

---

# 31. Testing the System

A simple end-to-end test can be performed by generating an SSH authentication event on Linux.

For example, attempt an SSH login with an incorrect password.

The Linux system should generate an event similar to:

```text
Failed password for ...
```

The Linux agent should display:

```text
[SENT] systemd-journal: Failed password ...
```

The Flask server should display a normalized event such as:

```text
[+] SYSTEMD-JOURNAL | authentication | login | failed
```

The resulting event should then appear in:

```text
output/normalized_events.json
```

---

# 32. Troubleshooting

## Server Cannot Be Reached

Check:

```bash
curl http://SERVER_IP:5000/api/health
```

Verify:

* Flask is running.
* Server is listening on `0.0.0.0`.
* Port `5000` is accessible.
* Firewall rules allow the connection.
* The agent is using the correct server IP.

---

## Unauthorized Error

Check that both server and agent use the same:

```env
NORMALIZER_API_KEY
```

---

## Linux Logs Are Not Being Collected

Check:

```bash
journalctl -f
```

and:

```bash
ls -l /var/log/auth.log
```

Also verify the Linux configuration:

```env
LINUX_ENABLE_JOURNAL=true
LINUX_ENABLE_AUTH_LOG=true
```

---

## Events Are Received But Not Stored

Check the Flask server output for parser or storage errors.

Also verify that:

```text
output/
```

exists and is writable.

---

## No Windows Events

Verify that the Windows Security log is available:

```powershell
wevtutil qe Security /c:5 /f:xml
```

If this command returns events, the Windows agent should be able to collect them.

---

# 33. Current Limitations

The current version is intentionally a foundation rather than a complete SIEM.

Current limitations include:

* JSON storage is not suitable for large-scale production workloads.
* Detection rules are not yet implemented.
* No event correlation engine.
* No alert management system.
* No web dashboard.
* No threat intelligence integration.
* No MITRE ATT&CK mapping.
* Limited Windows Event ID coverage.
* Limited Linux event coverage.
* API key authentication is basic.
* HTTP communication is not yet protected with TLS.
* No agent registration mechanism.
* No agent health monitoring.
* No centralized configuration management.
* No high-availability architecture.

---

# 34. Future Development Roadmap

The project is designed to gradually evolve from a log normalizer into a lightweight SIEM/security monitoring platform.

## Phase 1 — Detection Engine

Implement rule-based detection.

Initial rules could include:

```text
Multiple failed SSH logins
Multiple failed Windows logins
Successful login after repeated failures
Repeated sudo authentication failures
Suspicious privileged account activity
```

Example:

```text
5 failed SSH logins
        │
        ▼
Same source IP
        │
        ▼
Within 60 seconds
        │
        ▼
Generate security alert
```

---

## Phase 2 — Event Correlation

Instead of analyzing individual events, correlate multiple events.

Example:

```text
10 failed SSH attempts
        ↓
Successful login
        ↓
sudo authentication
        ↓
sudo command execution
```

This can represent a much more meaningful security sequence than any individual event.

---

## Phase 3 — Risk Scoring

Introduce a risk score based on event characteristics.

Potential factors:

```text
Event severity
Frequency
Source IP
Username
Privilege level
Previous activity
Event sequence
Known malicious indicators
```

Example conceptual model:

```text
Event
  │
  ├── Frequency
  ├── Severity
  ├── Reputation
  └── Context
        │
        ▼
   Risk Assessment
        │
        ▼
      Alert
```

---

## Phase 4 — Threat Intelligence

Integrate external threat intelligence sources.

Potential functionality:

```text
Source IP
     │
     ▼
IOC extraction
     │
     ▼
Threat Intelligence Lookup
     │
     ├── Known malicious
     ├── Suspicious
     └── Unknown
```

Potential integrations could include IP/domain reputation services and IOC feeds.

---

## Phase 5 — MITRE ATT&CK Mapping

Map detected behaviors to MITRE ATT&CK techniques.

For example:

```text
Repeated SSH Authentication Attempts
             │
             ▼
Credential Access
             │
             ▼
MITRE ATT&CK Mapping
```

This would make alerts more useful for SOC-style analysis.

---

## Phase 6 — Database Storage

Replace JSON storage with a proper database.

Potential technologies:

```text
PostgreSQL
OpenSearch
Elasticsearch
ClickHouse
```

The choice would depend on expected event volume and query requirements.

---

## Phase 7 — Security Dashboard

Build a web-based analyst dashboard.

Potential components:

```text
┌─────────────────────────────────────────────┐
│ Security Monitoring Dashboard               │
├───────────────┬───────────────┬─────────────┤
│ Events        │ Alerts        │ Agents      │
│ 12,542        │ 37            │ 4           │
├───────────────┴───────────────┴─────────────┤
│ Event Timeline                              │
├─────────────────────────────────────────────┤
│ Top Source IPs                              │
├─────────────────────────────────────────────┤
│ Authentication Failures                     │
├─────────────────────────────────────────────┤
│ Recent Security Alerts                      │
└─────────────────────────────────────────────┘
```

---

## Phase 8 — Real-Time Alerting

Add notification channels such as:

```text
Discord
Email
Telegram
Slack
Webhook
```

An example workflow:

```text
Suspicious Event
      │
      ▼
Detection Engine
      │
      ▼
Risk Evaluation
      │
      ▼
Alert
      │
      ├── Dashboard
      ├── Email
      └── Discord/Telegram
```

---

## Phase 9 — Agent Management

Introduce centralized agent management.

Possible features:

* Agent registration
* Agent authentication
* Agent status
* Last-seen timestamp
* Version tracking
* Configuration management
* Agent enable/disable
* Health monitoring

---

## Phase 10 — Secure Production Architecture

For production deployment, the system should eventually support:

```text
TLS/HTTPS
        │
        ▼
Reverse Proxy
        │
        ▼
API Server
        │
        ▼
Message Queue
        │
        ▼
Processing Workers
        │
        ▼
Event Database
        │
        ▼
Detection Engine
        │
        ▼
Alerting
```

Possible technologies:

```text
Nginx
Redis
RabbitMQ
Kafka
PostgreSQL
OpenSearch
Docker
Kubernetes
```

depending on deployment requirements.

---

# 35. Long-Term Architecture

The intended evolution of the project is:

```text
             Windows Agent
                   │
                   │
             Linux Agent
                   │
                   │
             Other Agents
                   │
                   ▼
          ┌─────────────────┐
          │ Ingestion API   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Normalization   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Event Pipeline  │
          └────────┬────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Detection Engine    Threat Intel
          │                 │
          └────────┬────────┘
                   ▼
          ┌─────────────────┐
          │ Correlation     │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Risk Assessment │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Alerting        │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ SOC Dashboard   │
          └─────────────────┘
```

---

# 36. Why This Project Matters

The project demonstrates several practical cybersecurity and system administration concepts:

* Security log collection
* Windows event monitoring
* Linux authentication monitoring
* Python development
* REST API development
* API authentication
* Log parsing
* Event normalization
* Structured security data
* Cross-platform system administration
* Network communication
* Configuration management
* Security monitoring architecture

It also provides a foundation for implementing more advanced SOC and SIEM capabilities.

---

# 37. Current Project Status

### Completed

* [x] Flask ingestion API
* [x] API key authentication
* [x] Windows Security log collection
* [x] Linux systemd journal collection
* [x] Linux authentication log collection
* [x] Windows parser
* [x] Linux authentication parser
* [x] Common normalized event schema
* [x] JSON event storage
* [x] Environment-based configuration
* [x] Windows/Linux agent configuration
* [x] Cross-machine communication
* [x] Basic error handling
* [x] Git/GitHub project structure

### Planned

* [ ] Detection engine
* [ ] Event correlation
* [ ] Severity classification
* [ ] Risk scoring
* [ ] MITRE ATT&CK mapping
* [ ] Threat intelligence integration
* [ ] Database storage
* [ ] Web dashboard
* [ ] Real-time alerts
* [ ] Agent management
* [ ] TLS/HTTPS
* [ ] Production deployment architecture

---

# 38. Author

**Bijay Dahal**

Cybersecurity & System Administration

GitHub:

```text
https://github.com/draven070
```

Portfolio:

```text
https://bijaydahal.com.np
```

---

# 39. License

This project is intended for educational, research, and authorized security monitoring purposes.
