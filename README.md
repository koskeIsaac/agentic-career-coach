# 🧠 Agentic Internship Search Assistant (GCP + MCP + Multi-Agent System)

## 📌 Overview
This is a multi-agent internship search assistant built on GCP using Vertex AI Agent Builder, MCP (Model Context Protocol), Cloud Run, and Firestore. It enables users to search internships, save applications, and track career pipelines through autonomous agents.

## 🏗️ Architecture
User → Supervisor Agent → Career Specialist Agent → MCP Server (Cloud Run) → Firestore

## 🤖 Agents
Supervisor Agent: Handles user interaction, breaks down tasks, and delegates all job-related actions to Career Specialist.

Career Specialist Agent: Executes tasks, calls MCP tools, and manages job/application data.

## 🔌 MCP Server
Base URL:
https://mcp-server-591823173342.us-central1.run.app/mcp

## 🛠️ Tools

fetch_jobs:
{
  "role": "software engineer intern",
  "location": "NYC"
}

sync_pipeline:

Create:
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

List:
{
  "action": "list"
}

## 🗄️ Firestore
Collection: pipeline

Schema:
{
  "job_id": "string",
  "company": "string",
  "title": "string",
  "location": "string",
  "status": "saved | applied | interviewing",
  "timestamp": "auto"
}

## 🔁 Workflows

Search:
User → Supervisor → Career Specialist → fetch_jobs → Results

Save:
User → Supervisor → Career Specialist → sync_pipeline(create) → Firestore

List:
Career Specialist → sync_pipeline(list) → Firestore

## ☁️ Deploy
gcloud run deploy mcp-server --source . --region us-central1 --allow-unauthenticated

## 🧪 Test
curl -X POST -H "Content-Type: application/json" -d '{
  "tool": "fetch_jobs",
  "params": {
    "role": "intern",
    "location": "NYC"
  }
}' https://mcp-server-591823173342.us-central1.run.app/mcp

## 🚀 Future Work
- Resume matching
- Job recommendations using embeddings
- Notifications for new internships
- Authentication per user
