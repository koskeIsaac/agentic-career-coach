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

## 🤖 Agents

### 🧭 Supervisor Agent
- User-facing entry point
- Understands user intent
- Delegates all job-related tasks to Career Specialist
- Does NOT call MCP tools directly

### 👨‍💼 Career Specialist Agent
- Executes tasks delegated by Supervisor
- Calls MCP tools:
  - `fetch_jobs`
  - `sync_pipeline`
- Returns structured results

---

## 🔌 MCP Server (Cloud Run)

### 🌐 Endpoint