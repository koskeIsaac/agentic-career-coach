# 🧠 Agentic Internship Search Assistant (GCP + MCP + Multi-Agent System)

## 📌 Overview

This project is a **multi-agent internship search assistant** built on **Google Cloud Platform (GCP)**. It demonstrates modern autonomous AI architecture using:

- Vertex AI Agent Builder (Supervisor + Career Specialist agents)
- Model Context Protocol (MCP) for tool standardization
- Cloud Run (backend MCP server)
- Cloud Firestore (persistent state storage)
- Agent-to-Agent (A2A) communication

The system simulates an intelligent career assistant that can:
- Search internships/jobs
- Save applications
- Track application status
- Maintain persistent career pipeline data

---

## 🏗️ Architecture
User
↓
Supervisor Agent (Lead Orchestrator)
↓ (A2A delegation)
Career Specialist Agent
↓ (MCP tool calls)
Cloud Run MCP Server
↓
Cloud Firestore



---


---

# 🤖 Agent Design

## 🧭 Supervisor Agent (Lead Orchestrator)

### Responsibilities:
- User-facing entry point
- Understands user intent
- Breaks down tasks
- Delegates ALL job-related tasks to Career Specialist
- Does NOT call MCP tools directly

### Rules:
- Never performs job search directly
- Never calls MCP tools
- Always uses Career Specialist via A2A

---

## 👨‍💼 Career Specialist Agent

### Responsibilities:
- Executes all delegated tasks
- Calls MCP tools
- Handles data retrieval and updates

### MCP Tools Used:
- `fetch_jobs` → retrieve internships
- `sync_pipeline` → manage application pipeline

---

# 🔌 MCP SERVER (Cloud Run)

## 🌐 Base URL
https://mcp-server-591823173342.us-central1.run.app/mcp


---

## 🛠️ Available Tools

### 1. fetch_jobs

Fetch internship/job listings with filters.

```json
{
  "role": "software engineer intern",
  "location": "NYC"
}

### 2. sync_pipeline

Manages internship application pipeline in Firestore.

Actions:
create
update
list
Example: Create entry

{
  "action": "create",
  "data": {
    "job_id": "1",
    "company": "Google",
    "title": "Software Engineer Intern",
    "location": "Remote",
    "status": "saved"
  }
}

Example: List entries

{
  "action": "list"
}

🗄️ FIRESTORE DATABASE
Collection: pipeline

Each document stores internship application data.

Schema:

{
  "job_id": "string",
  "company": "string",
  "title": "string",
  "location": "string",
  "status": "saved | applied | interviewing",
  "timestamp": "auto-generated"
}

🔁 SYSTEM WORKFLOWS
🔍 1. Job Search Flow

User:

“Find internships in NYC for Amazon”

Flow:
User
 → Supervisor Agent
 → Career Specialist Agent
 → MCP fetch_jobs
 → Results returned to user

 💾 2. Save Internship Flow

User:

“Save Google internship”

Flow:

User
 → Supervisor
 → Career Specialist
 → MCP sync_pipeline (create)
 → Firestore updated

 📊 3. View Applications Flow

User:

“Show my applications”

Flow:
Career Specialist → MCP sync_pipeline (list)
→ Firestore data 

☁️ DEPLOYMENT
Deploy MCP Server (Cloud Run)

gcloud run deploy mcp-server \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

  🧪 TESTING
Direct MCP Test

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "fetch_jobs",
    "params": {
      "role": "intern",
      "location": "NYC"
    }
  }' \
  https://mcp-server-591823173342.us-central1.run.app/mcp