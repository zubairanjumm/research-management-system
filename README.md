ResearchHub

ResearchHub is a frontend research management application for organizing projects, resources, notes, and bookmarks in one place.

The current version is built entirely with HTML, CSS, and vanilla JavaScript. It uses browser localStorage for frontend data persistence, so no backend or database is required to run the current version.

Features
Dashboard overview
Project management
Create projects
Search projects
Filter projects
Edit projects
Delete projects
Track project progress
Resource management
Notes management
Create notes
Search notes
Filter by project
Edit notes
Delete notes
Bookmark management
Add bookmarks
Search bookmarks
Filter by project
Edit bookmarks
Delete bookmarks
Persistent frontend data using localStorage
Shared sidebar navigation
Responsive layout
Global research search interface
Tech Stack
HTML5 — Page structure
CSS3 — Styling and layout
JavaScript (Vanilla JS) — Frontend functionality
LocalStorage — Client-side data persistence

No frameworks or frontend libraries are currently required.

Project Structure
research_hub/
│
├── frontend/
│   │
│   ├── index.html
│   ├── app.js
│   │
│   ├── pages/
│   │   ├── projects.html
│   │   ├── resources.html
│   │   ├── notes.html
│   │   └── bookmarks.html
│   │
│   ├── css/
│   │   ├── reset.css
│   │   ├── variables.css
│   │   ├── global.css
│   │   │
│   │   ├── components/
│   │   │   ├── sidebar.css
│   │   │   ├── topbar.css
│   │   │   ├── button.css
│   │   │   ├── card.css
│   │   │   └── panel.css
│   │   │
│   │   └── pages/
│   │       ├── dashboard.css
│   │       ├── projects.css
│   │       ├── resources.css
│   │       ├── notes.css
│   │       └── bookmarks.css
│   │
│   └── js/
│       ├── data.js
│       ├── projects.js
│       ├── resources.js
│       ├── notes.js
│       └── bookmarks.js
│
└── README.md
Running the Project

Because this is currently a frontend-only project, you don't need a backend server.

The easiest way to run it is with VS Code Live Server.

Open the project in VS Code.
Open frontend/index.html.
Start Live Server.
The ResearchHub dashboard will open in your browser.
Data Storage

ResearchHub currently stores application data in the browser using localStorage.

This means:

Data survives page refreshes.
Data is shared between the pages in the same browser/origin.
No database is currently required.
Clearing browser storage will remove the saved frontend data.

This is intentionally a frontend implementation. A backend/database can be connected later.

Current Architecture

The application is separated into three main layers:

HTML

Defines the structure of each page:

Dashboard
Projects
Resources
Notes
Bookmarks
CSS

CSS is separated into:

Global styles
Reusable components
Page-specific styles
JavaScript

JavaScript handles:

Rendering data
Creating records
Editing records
Deleting records
Searching
Filtering
Saving data to localStorage

The goal is to keep the frontend modular rather than putting everything into one JavaScript file.

Future Development

The frontend can later be extended with:

A proper global search system
Better dropdown menus for edit/delete actions
Resource CRUD improvements
Project detail pages
Authentication
Backend API integration
Database persistence
User accounts
Research file uploads
Tags and categories
Advanced filtering
AI-powered research features
Project Status

Frontend: In development

Backend: Not currently connected

Database: Not currently connected

Authentication: Not implemented

The current goal is to complete and stabilize the frontend before connecting the application to a backend API.
