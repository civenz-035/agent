# Autonomous Engineering Assistant (Google ADK)

A personal autonomous AI assistant built with the **Google Agent Development Kit (ADK)**, running on **Google Cloud Vertex AI Enterprise Backend**.

Equipped with autonomous terminal execution, file system management, and engineering reasoning.

---

## Capabilities & Tools

1. **Terminal Command Execution (`run_command`)**: Runs bash commands directly in the local WSL/Linux environment with full stdout/stderr capture.
2. **File Reading (`read_file`)**: Reads file content with line ranges and line numbers.
3. **File Creation (`write_file`)**: Creates or overwrites files with automatic parent directory creation.
4. **File Editing (`edit_file`)**: Exact substring replacement for robust code editing.
5. **Directory Explorer (`list_directory`)**: Inspects file trees, file sizes, and directory structures.

---

## Quick Start

### 1. Interactive Terminal CLI
To chat and work with the agent directly in your terminal:
```bash
adk run ~/agent
```

### 2. Local Web UI
To launch the agent with a modern web browser chat interface:
```bash
adk web ~/agent
```
Open `http://localhost:8000` (or the URL shown in terminal) in your browser.

### 3. API Server (FastAPI)
To expose the agent as a REST API for integrations (e.g. Webhooks, bots):
```bash
adk api_server ~/agent
```

---

## Configuration & Credentials

The agent uses **Google Cloud Vertex AI Enterprise Backend**:
* **Project**: `gen-lang-client-0021900495`
* **Location**: `us-central1`
* **Credentials**: Application Default Credentials (`~/.config/gcloud/application_default_credentials.json`)
* **Billing Account**: Tied to your Google Cloud credit.
