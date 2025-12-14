# AI Kata – Sweet Shop Management System

## Project Overview
A full-stack Sweet Shop Management System built using FastAPI and React.
It allows managing sweets, stock, cart-based purchases, and user authentication.

---

## Features

### Backend
- JWT-based authentication
- Role-based access (Admin / User)
- Product CRUD operations
- Stock management
- Cart checkout logic
- Fully tested APIs

### Frontend
- React + Vite UI
- Navbar with routing
- Home hero section
- Sweets, Cart, Login & Register pages
- Traditional Indian sweets theme

### Testing
- Automated backend tests using pytest
- Edge cases covered

---

## Tech Stack
- Backend: FastAPI, SQLAlchemy
- Frontend: React, Vite
- Database: SQLite
- Testing: pytest

---

## Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload


##Frontend
cd frontend
npm install
npm run dev


Screenshots

Screenshots are available in:
docs/screenshots/

Diagrams

Backend UML: docs/diagrams/backend_uml.png

Database ER Diagram: docs/diagrams/database_er_diagram.png

My AI Usage

AI tools (ChatGPT) were used for learning assistance, architecture guidance,
and best-practice suggestions. All core logic, UI design decisions,
debugging, and final implementation were manually performed and understood by me.

AI was used as a helper, not a replacement for development.