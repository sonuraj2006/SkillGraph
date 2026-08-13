# SkillGraph – Student Skill & Career Explorer

SkillGraph is a graph-based student skill and career exploration platform that connects a student's **academic year, projects, skills, job roles, and companies** using a graph database.

The system helps students understand how their existing skills relate to different career opportunities and identifies suitable job roles based on their skill set.

## 🚀 Live Demo

**Live Application:**
`https://skillgraph-frontend-e67f.onrender.com`

**GitHub Repository:**
`https://github.com/sonuraj2006/SkillGraph`

---

## 📌 Problem Statement

Students often have multiple technical skills and projects but may not clearly understand how these skills connect to potential career opportunities.

SkillGraph addresses this problem by creating relationships between:

* Students
* Academic years
* Projects
* Skills
* Job roles
* Companies

The platform allows students to explore these connections interactively.

---

## 💡 Solution

SkillGraph uses a **graph database** to represent relationships between student skills, projects, job roles, and companies.

A student can select:

1. Academic Year
2. Project
3. Skill

The system then generates an interactive skill graph showing related:

* Projects
* Skills
* Job roles
* Companies

The backend also provides career recommendations based on the student's existing skills.

---

## ✨ Features

### 🎓 Academic Year Filtering

Students can select their academic year, such as:

* Year 3
* Year 4

### 📁 Project Filtering

The application provides projects associated with the selected academic year.

Example projects include:

* SecurePrompt
* RAG Chatbot
* Computer Vision System
* E-Commerce Recommendation System
* Student Performance Predictor

### 🛠️ Skill Filtering

Students can select skills associated with their projects.

Examples:

* Python
* Machine Learning
* FastAPI
* React
* SQL
* NLP
* Pandas
* NumPy
* LangChain
* Computer Vision

### 🕸️ Interactive Skill Graph

The graph visually represents relationships between:

**Student → Project → Skill → Job Role → Company**

This makes career relationships easier to understand.

### 💼 Career Recommendations

The backend calculates job-role recommendations based on the student's skills.

The recommendation includes:

* Job role
* Matching skills
* Total required skills
* Match percentage

### 📚 Missing Skills Analysis

The system can identify skills that a student is missing for a particular job role.

This helps students understand what skills they should learn next.

---

## 🏗️ System Architecture

```text
                    Student
                       |
                       | WORKED_ON
                       ↓
                    Project
                       |
                       | USES_SKILL
                       ↓
                     Skill
                       |
                       | REQUIRED_FOR
                       ↓
                    Job Role
                       |
                       | OFFERED_BY
                       ↓
                    Company
```

### Application Architecture

```text
User
 ↓
React Frontend
 ↓
FastAPI Backend
 ↓
CognoDB / Neo4j Graph Database
 ↓
Graph Queries
 ↓
Recommendations & Skill Graph
```

---

## 🧰 Technology Stack

### Frontend

* React
* Vite
* Axios
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Database

* CognoDB
* Neo4j-compatible graph database
* Cypher

### Deployment

* GitHub
* Render

---

## 📂 Project Structure

```text
SkillGraph/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── seed.py
│   │
│   └── routes/
│       ├── students.py
│       └── recommendations.py
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   │
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── GraphView.jsx
│       ├── index.css
│       └── main.jsx
│
├── queires/
│   ├── jobs.cypher
│   ├── recommendations.cypher
│   ├── skills.cypher
│   └── students.cypher
│
├── .gitignore
└── README.md
```

---

## 🔄 How It Works

### Step 1 – Select Academic Year

The frontend requests available academic years from the FastAPI backend.

### Step 2 – Select Project

After selecting an academic year, the available projects for that year are retrieved from the graph database.

### Step 3 – Select Skill

After selecting a project, the associated skills are retrieved.

### Step 4 – Generate Skill Graph

The selected filters are sent to the backend.

The backend executes Cypher queries to retrieve graph relationships.

### Step 5 – Explore Career Connections

The resulting graph displays connections between:

```text
Student
   ↓
Project
   ↓
Skill
   ↓
Job Role
   ↓
Company
```

### Step 6 – Career Recommendation

The recommendation API compares the student's skills with the skills required by different job roles and calculates a matching percentage.

---

## 🔌 API Endpoints

### Health Check

```text
GET /health
```

Checks the connection between the FastAPI backend and CognoDB.

### Graph Filters

```text
GET /recommendations/filters
```

Returns available:

* Years
* Projects
* Skills

### Student Recommendations

```text
GET /recommendations/{student_id}
```

Returns recommended job roles based on matching skills.

### Missing Skills

```text
GET /recommendations/{student_id}/{job_id}/missing-skills
```

Returns the skills required for a job role that the student does not currently have.

### Student Graph

```text
GET /recommendations/{student_id}/graph
```

Returns graph connections based on selected filters.

### Graph Summary

```text
GET /recommendations/{student_id}/graph-summary
```

Returns available projects, skills, job roles, and companies connected to the student.

---

## 📊 Example Recommendation

For student `S001`, the system can produce recommendations such as:

```text
AI Engineer
Matching Skills: 4 / 6
Match Percentage: 66.67%

Data Scientist
Matching Skills: 4 / 6
Match Percentage: 66.67%

Backend Developer
Matching Skills: 3 / 5
Match Percentage: 60%

Data Analyst
Matching Skills: 3 / 5
Match Percentage: 60%

Machine Learning Engineer
Matching Skills: 2 / 5
Match Percentage: 40%
```

These recommendations are generated from the graph relationships stored in the database.

---

## ⚙️ Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/sonuraj2006/SkillGraph.git
cd SkillGraph
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing your database credentials:

```text
COGNODB_URI=your_database_uri
COGNODB_USERNAME=your_username
COGNODB_PASSWORD=your_password
```

Start the backend:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 3. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at the local URL shown by Vite.

---

## 🔐 Security

Database credentials are stored using environment variables and should **not** be committed to GitHub.

The `.env` file is excluded using `.gitignore`.

---

## ☁️ Deployment

The project is deployed using Render.

### Backend

The FastAPI backend is deployed as a Render web service.

### Frontend

The React/Vite frontend is deployed separately as a Render web service.

### Database

The application connects to CognoDB using environment variables configured in Render.

---

## 🎯 Future Improvements

Possible future improvements include:

* Personalized learning-path recommendations
* Skill-gap visualization
* More job roles and companies
* Resume-based skill extraction
* AI-powered career recommendations
* Student profile management
* Authentication and authorization
* Advanced graph analytics
* Skill trend analysis
* Job-market data integration

---

## 👨‍💻 Author

**Banoth Sonuraj**

B.Tech – Computer Science & Engineering (AI & ML)

MLR Institute of Technology

### Profiles

GitHub:
`https://github.com/sonuraj2006`

LinkedIn:
`https://www.linkedin.com/in/banoth-sonu-raj-15748a353/`
