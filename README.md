# SkillGraph – Student Skill & Career Explorer

SkillGraph is a graph-database-powered career exploration application.

It connects a student's:

Student → Project → Skill → Job Role → Company

and uses these relationships to provide career recommendations and identify missing skills.

## Problem

Students often know their skills and projects but do not clearly understand:

- Which career roles match their skills
- Which skills are missing for a particular role
- How their projects connect to their skills
- Which companies offer suitable career opportunities

SkillGraph solves this by representing these relationships as a graph.

## Why a Graph Database?

A graph database is suitable because the main questions in SkillGraph are relationship-based.

For example:

- Which jobs match a student's skills?
- Which skills are missing for a particular job?
- Which projects demonstrate a student's skills?
- Which companies offer jobs requiring skills demonstrated by the student?

These require traversing multiple relationships:

Student → Project → Skill → Job → Company

This type of connected traversal is natural in a graph database.

## Graph Data Model

### Nodes

- Student
- Project
- Skill
- Job
- Company

### Relationships

- STUDENT -[WORKED_ON]-> PROJECT
- PROJECT -[USES_SKILL]-> SKILL
- JOB -[REQUIRED_FOR]-> SKILL
- JOB -[OFFERED_BY]-> COMPANY

## Architecture

React Frontend
        ↓
FastAPI Backend
        ↓
Neo4j Driver
        ↓
CognoDB Graph Database

## Features

### Student Profile

Displays student information, degree and year.

### Skills

Displays the student's current technical skills.

### Projects

Displays projects completed by the student.

### Career Recommendations

Calculates job-role matches based on the student's skills.

### Missing Skills

Clicking a recommended job displays the skills the student needs to develop.

### Interactive Graph

Visualizes the relationships between:

Student → Project → Skill → Job → Company

## Technology Stack

### Frontend

- React
- Vite
- Axios
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- Neo4j Python Driver

### Database

- CognoDB
- OpenCypher
- Bolt protocol

## Main Queries

### Get Student Skills

Retrieves all skills connected to a student.

### Get Student Projects

Retrieves projects completed by the student.

### Career Recommendations

Traverses:

Student → Project → Skill → Job

to calculate matching skills for each job role.

### Missing Skills

Compares the student's skills with the skills required by a selected job.

### Graph Exploration

Traverses:

Student → Project → Skill → Job → Company

to show connected career opportunities.

## Project Structure

SkillGraph/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── queries/
│   ├── seed.py
│   ├── test_queries.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── GraphView.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md

## Environment Variables

Database credentials must be stored in environment variables.

Example:

COGNODB_URI=your_database_uri
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=your_password

Never commit the `.env` file.

## Running the Backend

cd backend

Create virtual environment:

python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start FastAPI:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Running the Frontend

cd frontend

Install dependencies:

npm install

Start development server:

npm run dev

Frontend:

http://localhost:5174

## Seed Database

From the backend directory:

python seed.py

The seed script creates the sample graph data.

## Screenshots

Add screenshots of:

1. Student dashboard
2. Career recommendations
3. Missing skills
4. Graph visualization

## Future Improvements

- Multiple student profiles
- Skill learning recommendations
- Job search integration
- More companies and job roles
- Authentication
- Advanced graph analytics

## Author

Banoth Sonuraj