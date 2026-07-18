# AI-Powered Project Management System

An intelligent project management platform designed to help teams plan, manage, and track projects efficiently. The system centralizes project information, task management, collaboration, and reporting while leveraging AI-powered capabilities to improve productivity and decision-making.

## 🚀 Overview

The AI-Powered Project Management System is a web application that enables organizations to manage projects, tasks, teams, and resources from a single platform.

The system provides project tracking, task assignment, milestone monitoring, dashboards, analytics, and AI-powered assistance to support project execution and collaboration.

---

## ✨ Features

### Project Management

- Create and manage projects
- Define project milestones
- Monitor project progress
- Track project status

### Task Management

- Create and assign tasks
- Set priorities and due dates
- Track task completion
- Manage task workflows

### Team Collaboration

- Team workspaces
- Activity tracking
- Notifications
- Shared project visibility

### Reporting & Analytics

- Project dashboards
- Team performance metrics
- Progress reporting
- Power BI integration

### Security

- JWT Authentication
- Role-Based Access Control (RBAC)
- Secure API endpoints

### AI Features

- AI Project Assistant
- Knowledge Base Search
- Intelligent Project Insights
- Automated Summaries
- RAG-Powered Chatbot

---

## 🛠 Technology Stack

### Frontend

- React
- TypeScript
- Tailwind CSS
- React Router
- Axios

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

### Database

- Microsoft SQL Server

### Authentication

- JWT
- RBAC

### AI

- OpenAI GPT-4.1
- LangChain
- RAG Architecture

### Reporting

- Power BI

### Cloud Services

- Microsoft Azure

---

## 📂 Project Structure

```text
project-management-system/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── main.py
│   │
│   ├── alembic/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── layouts/
│
├── docs/
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/project-management-system.git

cd project-management-system
```

### Backend Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=mssql+pyodbc://username:password@localhost/ProjectManagementDB?driver=ODBC+Driver+18+for+SQL+Server
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-api-key
```

Run database migrations:

```bash
alembic upgrade head
```

Start the API server:

```bash
uvicorn app.main:app --reload
```

---

### Frontend Setup

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

---

## 📈 Planned Modules

- Authentication & Authorization
- User Management
- Team Management
- Project Management
- Task Management
- Kanban Board
- Comments & Activity Logs
- Notifications
- File Management
- Dashboard & Analytics
- AI Assistant
- Reporting

---

## 🗺 Roadmap

### MVP

- [ ] Authentication
- [ ] User Management
- [ ] Project Management
- [ ] Task Management
- [ ] Team Management

### Phase 2

- [ ] Kanban Board
- [ ] Notifications
- [ ] File Uploads
- [ ] Activity Logs

### Phase 3

- [ ] AI Assistant
- [ ] RAG Knowledge Base
- [ ] Smart Recommendations
- [ ] Automated Reporting

---

## 👨‍💻 Author

**Carl Mathew Morada**

EHS Data Technologist I | Data Engineer | Python Developer

Building scalable web applications, automation solutions, and AI-powered business systems using FastAPI, React, SQL Server, and Azure.
