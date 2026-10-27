# 🛡️ OpsAegis: Autonomous SRE Remediation Agent

> **Built for the Meta Hackathon 2026 (Best Agentic AI Track)**  
> Autonomous incident triage, causal root-cause analysis, and container-safe remediation powered by **Meta Muse Spark Open** and **Modal Serverless Sandboxes**.

---

## 📌 Problem Statement

In modern cloud environments, infrastructure failures like cgroup Out-Of-Memory (OOM) kills, silent memory leaks, and cascading process crashes introduce costly downtime. Human Site Reliability Engineering (SRE) triage takes an average of 15–45 minutes per incident. 

**OpsAegis** eliminates human latency by delivering a fully closed-loop agentic remediation pipeline capable of diagnosing cryptic Linux kernel traces, planning unprivileged container-safe interventions, and executing verified fixes in under 10 seconds.

---

## 🧠 Architectural Overview

OpsAegis operates on an autonomous **Sense -> Reason -> Act -> Verify** loop:

- **1. Telemetry Ingestion:** Ingests raw Linux kernel logs (oom-killer, dmesg, cgroup memory traces).
- **2. Reasoning Core (Meta Muse Spark Open):** Performs deep causal inference, isolates offending PIDs, and synthesizes container-safe remediation commands (unprivileged, non-systemd).
- **3. Isolated Cloud Execution (Modal Sandbox):** Spawns ephemeral Debian containers, executes real background failure injection, and verifies system health (Exit Code 0).
- **4. Self-Healing Reflection:** Feeds runtime stderr back into Muse Spark Open if edge-case constraints are met, adapting commands dynamically until verified clean.

---

## ✨ Key Agentic Features

- **Deep Log Reasoning:** Parses low-level kernel failure mechanisms without rigid regex rules.
- **Environment-Aware Synthesis:** Adheres strictly to unprivileged container environments (avoids /proc/sys writes or systemctl).
- **Real Failure Verification:** Tests remediations against live, injected rogue processes running inside serverless sandboxes.
- **Autonomous Self-Healing Loop:** Automatically reflects on execution failures and recalibrates commands in real time.
- **Interactive Telemetry Dashboard:** Streamlit UI providing live visual telemetry, step-by-step model reasoning traces, and cloud sandbox feedback.

---

## 🛠️ Tech Stack

- **Reasoning Model:** Meta Muse Spark Open (meta-models/muse-spark-open via Baseten Model APIs)
- **Execution Engine:** Modal Serverless Cloud Sandboxes (modal.App)
- **Dashboard & Telemetry:** Streamlit & Rich CLI
- **Language & Orchestration:** Python 3.12+, OpenAI SDK, Pydantic

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- Baseten API Key with access to Meta Muse Spark Open
- Modal API Token configured (modal token set)

### 2. Installation
```bash
git clone [https://github.com/riyankhamdani/ops-aegis.git](https://github.com/riyankhamdani/ops-aegis.git)
cd ops-aegis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a .env file in the project root:
```env
BASETEN_API_KEY=your_baseten_api_key_here
BASETEN_MODEL_ID=meta-models/muse-spark-open
```

### 4. Running OpsAegis

**Terminal CLI Mode:**
```bash
python main.py
```

**Interactive Telemetry Dashboard:**
```bash
streamlit run app.py
```

---

## 🛡️ License
MIT License. Built for the Meta Hackathon 2026.
