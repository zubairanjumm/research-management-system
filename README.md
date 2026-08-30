# ResearchHub

ResearchHub is a research management platform designed to organize projects, resources, notes, and bookmarks in one place.

The goal is to turn scattered research material into structured, searchable workspaces that can eventually support AI-assisted research workflows.

## Overview

ResearchHub is built around the idea of **Projects**.

<<<<<<< HEAD
Because this is currently a frontend-only project, you don't need a backend server.
=======
Each project acts as a research workspace containing:

* Resources
* Notes
* Bookmarks
* Research progress
* Project metadata

The current application is being migrated from a frontend-only `localStorage` implementation to a proper backend architecture using FastAPI, SQLAlchemy, and SQLite.

### Core relationship

```text
Project
│
├── Resources
├── Notes
└── Bookmarks
```

Each resource, note, and bookmark belongs to a project through a `project_id` foreign key.

---

## Features

### Projects

Projects represent individual research topics or areas.

Each project contains:

* Name
* Description
* Symbol
* Progress
* Status
* Creation timestamp
* Last updated timestamp

Supported operations:

* Create project
* View all projects
* View a project by ID
* Update project
* Delete project
* Search/filter projects

---

### Resources

Resources are research materials associated with a project.

Supported resource types include:

* PDF
* Website
* Book

Each resource contains:

* Title
* Description
* Type
* Project
* Creation timestamp
* Last updated timestamp

Planned operations:

* Create resource
* View resources
* View resource by ID
* Update resource
* Delete resource
* Search resources
* Filter by type
* Filter by project
* Sort resources

---

### Notes

Notes allow research findings and ideas to be stored inside a project.

Each note contains:

* Title
* Content
* Project
* Creation timestamp
* Last updated timestamp

Planned operations:

* Create note
* View notes
* View note by ID
* Update note
* Delete note
* Search notes
* Filter by project

---

### Bookmarks

Bookmarks allow useful external websites and references to be saved inside a project.

Each bookmark contains:

* Title
* URL
* Description
* Project
* Creation timestamp
* Last updated timestamp

Planned operations:

* Create bookmark
* View bookmarks
* View bookmark by ID
* Update bookmark
* Delete bookmark
* Search bookmarks
* Filter by project

---

# Architecture

ResearchHub follows a client-server architecture.

```text
                    ResearchHub
                         │
              ┌──────────┴──────────┐
              │                     │
          Frontend                Backend
              │                     │
          JavaScript              FastAPI
              │                     │
              │                  Routers
              │                     │
              │                  Schemas
              │                     │
              │                 SQLAlchemy
              │                     │
              │                   SQLite
              │
              └────── HTTP / JSON ──┘
```

### Request flow

```text
User
 │
 ▼
Frontend
 │
 │ HTTP request
 ▼
FastAPI
 │
 ▼
Router
 │
 ▼
Pydantic Schema
 │
 ▼
SQLAlchemy Model
 │
 ▼
Database
 │
 ▼
Response Schema
 │
 ▼
JSON response
 │
 ▼
Frontend
 │
 ▼
UI
```

---

# Backend Architecture

The backend is organized by responsibility.

```text
backend/
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── resource.py
│   │   ├── note.py
│   │   └── bookmark.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── resource.py
│   │   ├── note.py
│   │   └── bookmark.py
│   │
│   └── routers/
│       ├── __init__.py
│       ├── projects.py
│       ├── resources.py
│       ├── notes.py
│       └── bookmarks.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---
>>>>>>> bc3ca92 (Build backend foundation and project CRUD)

# Technology Stack

## Frontend

* HTML
* CSS
* JavaScript
* Browser `fetch()` API
* LocalStorage during the initial prototype

The frontend will eventually communicate with the backend through REST APIs instead of using LocalStorage as the primary data store.

---

## Backend

### FastAPI

FastAPI provides the REST API and handles:

* HTTP requests
* Routing
* Request validation
* Response serialization
* API documentation

### Pydantic

Pydantic is used for:

* Request validation
* Response schemas
* Data constraints
* Serialization

Example:

```text
ProjectCreate
ProjectUpdate
ProjectResponse
```

---

### SQLAlchemy

SQLAlchemy is the ORM responsible for mapping Python classes to database tables.

For example:

```text
Python Model              Database Table

Project          ───────► projects
Resource         ───────► resources
Note             ───────► notes
Bookmark         ───────► bookmarks
```

---

### SQLite

SQLite is currently used as the database because ResearchHub is currently a local/small-scale application.

The database contains:

```text
projects
resources
notes
bookmarks
```

The database file is intentionally excluded from Git.

---

### Uvicorn

Uvicorn runs the FastAPI application as an ASGI server.

Development server:

```bash
uv run uvicorn app.main:app --reload
```

---

### uv

`uv` is used for Python project and dependency management.

---

# API

The planned API structure is:

```text
/api
│
├── /projects
│
├── /resources
│
├── /notes
│
└── /bookmarks
```

## Projects

```text
GET     /api/projects/
POST    /api/projects/
GET     /api/projects/{project_id}
PUT     /api/projects/{project_id}
DELETE  /api/projects/{project_id}
```

## Resources

```text
GET     /api/resources/
POST    /api/resources/
GET     /api/resources/{resource_id}
PUT     /api/resources/{resource_id}
DELETE  /api/resources/{resource_id}
```

## Notes

```text
GET     /api/notes/
POST    /api/notes/
GET     /api/notes/{note_id}
PUT     /api/notes/{note_id}
DELETE  /api/notes/{note_id}
```

## Bookmarks

```text
GET     /api/bookmarks/
POST    /api/bookmarks/
GET     /api/bookmarks/{bookmark_id}
PUT     /api/bookmarks/{bookmark_id}
DELETE  /api/bookmarks/{bookmark_id}
```

---

# Database Design

The database follows a simple relational structure.

```text
                         projects
                       ┌────────────┐
                       │ id         │
                       │ name       │
                       │ description│
                       │ symbol     │
                       │ progress   │
                       │ status     │
                       └─────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              │              │              │
              ▼              ▼              ▼
        resources          notes        bookmarks
        ┌─────────┐      ┌─────────┐     ┌──────────┐
        │ id      │      │ id      │     │ id       │
        │ title   │      │ title   │     │ title    │
        │ type    │      │ content │     │ url      │
        │project_id│     │project_id│    │project_id│
        └─────────┘      └─────────┘     └──────────┘
```

The child tables reference the project using:

```text
project_id → projects.id
```

This provides a proper relational relationship instead of storing project names repeatedly.

---

# Current Development Status

ResearchHub is currently under active development.

### Completed

* Initial frontend application
* Project management UI
* Resource management UI
* Notes UI
* Bookmark UI
* Initial LocalStorage-based persistence
* FastAPI backend setup
* SQLAlchemy database setup
* SQLite database
* Project database model
* Project Pydantic schemas
* Project API router
* Project creation endpoint
* Project listing endpoint
* Project retrieval by ID
* Project update endpoint
* Project deletion endpoint
* Swagger/OpenAPI API documentation

### In Progress

* Resource backend
* Notes backend
* Bookmark backend
* Backend filtering/search
* Frontend → backend integration

---

# Roadmap

## Phase 1 — Core Backend

* [x] Database setup
* [x] Project model
* [x] Project schemas
* [x] Project CRUD API
* [ ] Resource model
* [ ] Resource schemas
* [ ] Resource CRUD API
* [ ] Note model
* [ ] Note schemas
* [ ] Note CRUD API
* [ ] Bookmark model
* [ ] Bookmark schemas
* [ ] Bookmark CRUD API

---

## Phase 2 — Frontend Integration

Replace LocalStorage persistence with REST API requests.

Current:

```text
Frontend
   ↓
JavaScript
   ↓
LocalStorage
```

Target:

```text
Frontend
   ↓
fetch()
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
SQLite
```

Tasks:

* [ ] Connect Projects frontend to API
* [ ] Connect Resources frontend to API
* [ ] Connect Notes frontend to API
* [ ] Connect Bookmarks frontend to API
* [ ] Remove LocalStorage as the source of truth
* [ ] Handle API errors in the frontend
* [ ] Add loading states
* [ ] Add empty states

---

# Phase 3 — Better Backend

After the core CRUD system is stable:

* [ ] Better validation
* [ ] Pagination
* [ ] Advanced filtering
* [ ] Search
* [ ] Sorting
* [ ] Proper exception handling
* [ ] Database migrations with Alembic
* [ ] Automated tests
* [ ] API integration tests
* [ ] Environment-based configuration
* [ ] PostgreSQL support

---

# Phase 4 — Authentication

Once the core application is stable:

* [ ] User registration
* [ ] Login
* [ ] Password hashing
* [ ] JWT authentication
* [ ] User-specific projects
* [ ] Authorization
* [ ] Protected API routes

The database relationship would then become:

```text
User
 │
 └── Projects
      │
      ├── Resources
      ├── Notes
      └── Bookmarks
```

---

# Phase 5 — AI Research Features

The long-term goal is to evolve ResearchHub from a CRUD research organizer into an AI-assisted research platform.

Potential features:

### AI Research Assistant

Allow users to ask questions about their research workspace.

```text
User
 │
 ▼
ResearchHub AI
 │
 ├── Project data
 ├── Notes
 ├── Resources
 └── Bookmarks
```

---

### RAG

ResearchHub could eventually implement Retrieval-Augmented Generation.

Potential architecture:

```text
Research Documents
       │
       ▼
Document Processing
       │
       ▼
Chunking
       │
       ▼
Embeddings
       │
       ▼
Vector Database
       │
       ▼
Retriever
       │
       ▼
LLM
       │
       ▼
Research Answer
```

Potential technologies:

* LangChain
* LangGraph
* Embedding models
* PostgreSQL + pgvector
* Vector databases
* LLM APIs

---

### AI Research Workflows

Potential future workflows:

* Summarize research papers
* Extract key findings
* Generate research questions
* Compare sources
* Find relationships between notes
* Answer questions using project knowledge
* Generate literature-review drafts
* Automatically organize research material

---

# Future Production Architecture

The long-term architecture could evolve into:

```text
                        Client
                          │
                          ▼
                    Frontend App
                          │
                          ▼
                      REST API
                          │
                          ▼
                       FastAPI
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
          PostgreSQL    Redis       AI Services
             │                         │
             │                         ▼
             │                    LLM / RAG
             │                         │
             ▼                         ▼
          Research Data          AI Research
```

This is not the current architecture. It is the intended direction as the application grows.

---

# Development

Clone the repository:

```bash
git clone https://github.com/zubairanjumm/research_hub.git
```

Move into the backend:

```bash
cd research_hub/backend
```

Install dependencies with `uv`:

```bash
uv sync
```

Run the development server:

```bash
uv run uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Environment Variables

Environment-specific secrets should be stored in `.env`.

Example:

```env
DATABASE_URL=sqlite:///./research_hub.db
```

The `.env` file should never be committed to Git.

---

# Project Principles

ResearchHub is being developed around a few principles:

### 1. Keep the core simple

CRUD functionality should work correctly before adding AI features.

### 2. Separate responsibilities

```text
Routers → HTTP
Schemas → Validation
Models → Database
Database → Persistence
Frontend → UI
```

### 3. Use relational data correctly

Resources, notes, and bookmarks reference projects through foreign keys rather than duplicating project names.

### 4. Build incrementally

The application is developed in vertical slices:

```text
Model
 ↓
Schema
 ↓
Router
 ↓
API
 ↓
Frontend integration
```

### 5. AI comes after the foundation

AI/RAG features will be built on top of a stable research-data system rather than being added before the core application works.

---

# Status

**Active development**

ResearchHub is currently transitioning from a frontend prototype into a full-stack research management application.

The immediate goal is to complete the backend CRUD system and connect the existing frontend to the API.

---

## Author

**Zubair Anjum**

GitHub: `zubairanjumm`

ResearchHub is a learning and development project focused on building practical full-stack and AI engineering systems.
