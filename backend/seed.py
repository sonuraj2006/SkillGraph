from database import driver


def seed_database():
    with driver.session() as session:

        # -------------------------------------------------
        # 1. CREATE CONSTRAINTS
        # -------------------------------------------------

        constraints = [
            """
            CREATE CONSTRAINT student_id_unique IF NOT EXISTS
            FOR (s:Student)
            REQUIRE s.id IS UNIQUE
            """,

            """
            CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
            FOR (s:Skill)
            REQUIRE s.name IS UNIQUE
            """,

            """
            CREATE CONSTRAINT project_id_unique IF NOT EXISTS
            FOR (p:Project)
            REQUIRE p.id IS UNIQUE
            """,

            """
            CREATE CONSTRAINT jobrole_id_unique IF NOT EXISTS
            FOR (j:JobRole)
            REQUIRE j.id IS UNIQUE
            """,

            """
            CREATE CONSTRAINT company_id_unique IF NOT EXISTS
            FOR (c:Company)
            REQUIRE c.id IS UNIQUE
            """
        ]

        for query in constraints:
            session.run(query)

        print("✓ Constraints created")

        # -------------------------------------------------
        # 2. CREATE STUDENTS
        # -------------------------------------------------

        students = [
            {
                "id": "S001",
                "name": "Sonuraj",
                "degree": "B.Tech CSE - AI & ML",
                "year": 3
            },
            {
                "id": "S002",
                "name": "Rahul Kumar",
                "degree": "B.Tech Computer Science",
                "year": 3
            },
            {
                "id": "S003",
                "name": "Ananya Sharma",
                "degree": "B.Tech AI & Data Science",
                "year": 4
            },
            {
                "id": "S004",
                "name": "Priya Reddy",
                "degree": "B.Tech Computer Science",
                "year": 3
            }
        ]

        student_query = """
        MERGE (s:Student {id: $id})
        SET s.name = $name,
            s.degree = $degree,
            s.year = $year
        """

        for student in students:
            session.run(student_query, **student)

        print("✓ Students created")

        # -------------------------------------------------
        # 3. CREATE SKILLS
        # -------------------------------------------------

        skills = [
            "Python",
            "Java",
            "C",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Computer Vision",
            "FastAPI",
            "React",
            "LangChain",
            "Docker",
            "Git",
            "Data Analysis",
            "Pandas",
            "NumPy"
        ]

        skill_query = """
        MERGE (s:Skill {name: $name})
        """

        for skill in skills:
            session.run(skill_query, name=skill)

        print("✓ Skills created")

        # -------------------------------------------------
        # 4. CREATE PROJECTS
        # -------------------------------------------------

        projects = [
            {
                "id": "P001",
                "name": "RAG Chatbot",
                "description": "A retrieval augmented generation chatbot"
            },
            {
                "id": "P002",
                "name": "Student Performance Predictor",
                "description": "Machine learning system for predicting student performance"
            },
            {
                "id": "P003",
                "name": "Computer Vision System",
                "description": "Computer vision application for image analysis"
            },
            {
                "id": "P004",
                "name": "E-Commerce Recommendation System",
                "description": "Recommendation system for an online shopping platform"
            },
            {
                "id": "P005",
                "name": "SecurePrompt",
                "description": "Enterprise prompt security and sensitive-data protection system"
            }
        ]

        project_query = """
        MERGE (p:Project {id: $id})
        SET p.name = $name,
            p.description = $description
        """

        for project in projects:
            session.run(project_query, **project)

        print("✓ Projects created")

        # -------------------------------------------------
        # 5. CREATE JOB ROLES
        # -------------------------------------------------

        job_roles = [
            {
                "id": "J001",
                "name": "AI Engineer"
            },
            {
                "id": "J002",
                "name": "Machine Learning Engineer"
            },
            {
                "id": "J003",
                "name": "Data Scientist"
            },
            {
                "id": "J004",
                "name": "Backend Developer"
            },
            {
                "id": "J005",
                "name": "Data Analyst"
            }
        ]

        job_query = """
        MERGE (j:JobRole {id: $id})
        SET j.name = $name
        """

        for job in job_roles:
            session.run(job_query, **job)

        print("✓ Job roles created")

        # -------------------------------------------------
        # 6. CREATE COMPANIES
        # -------------------------------------------------

        companies = [
            {
                "id": "C001",
                "name": "TechNova",
                "industry": "Technology"
            },
            {
                "id": "C002",
                "name": "DataSphere",
                "industry": "Data & Analytics"
            },
            {
                "id": "C003",
                "name": "AI Labs",
                "industry": "Artificial Intelligence"
            },
            {
                "id": "C004",
                "name": "CloudWorks",
                "industry": "Cloud Technology"
            }
        ]

        company_query = """
        MERGE (c:Company {id: $id})
        SET c.name = $name,
            c.industry = $industry
        """

        for company in companies:
            session.run(company_query, **company)

        print("✓ Companies created")

        # -------------------------------------------------
        # 7. STUDENT → SKILL
        # -------------------------------------------------

        student_skills = {
            "S001": [
                "Python",
                "Machine Learning",
                "NLP",
                "FastAPI",
                "React",
                "LangChain",
                "Git",
                "Pandas",
                "NumPy"
            ],
            "S002": [
                "Java",
                "Python",
                "SQL",
                "Git",
                "Docker"
            ],
            "S003": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "SQL",
                "Pandas",
                "NumPy"
            ],
            "S004": [
                "Python",
                "Computer Vision",
                "Machine Learning",
                "React",
                "Git"
            ]
        }

        student_skill_query = """
        MATCH (s:Student {id: $student_id})
        MATCH (skill:Skill {name: $skill_name})
        MERGE (s)-[:HAS_SKILL]->(skill)
        """

        for student_id, student_skill_list in student_skills.items():
            for skill_name in student_skill_list:
                session.run(
                    student_skill_query,
                    student_id=student_id,
                    skill_name=skill_name
                )

        print("✓ Student-skill relationships created")

        # -------------------------------------------------
        # 8. STUDENT → PROJECT
        # -------------------------------------------------

        student_projects = {
            "S001": ["P001", "P002", "P005"],
            "S002": ["P004"],
            "S003": ["P002", "P004"],
            "S004": ["P003"]
        }

        student_project_query = """
        MATCH (s:Student {id: $student_id})
        MATCH (p:Project {id: $project_id})
        MERGE (s)-[:WORKED_ON]->(p)
        """

        for student_id, project_list in student_projects.items():
            for project_id in project_list:
                session.run(
                    student_project_query,
                    student_id=student_id,
                    project_id=project_id
                )

        print("✓ Student-project relationships created")

        # -------------------------------------------------
        # 9. PROJECT → SKILL
        # -------------------------------------------------

        project_skills = {
            "P001": [
                "Python",
                "NLP",
                "LangChain"
            ],
            "P002": [
                "Python",
                "Machine Learning",
                "Pandas",
                "NumPy"
            ],
            "P003": [
                "Python",
                "Computer Vision",
                "Machine Learning"
            ],
            "P004": [
                "Python",
                "Machine Learning",
                "SQL"
            ],
            "P005": [
                "Python",
                "NLP",
                "FastAPI",
                "React"
            ]
        }

        project_skill_query = """
        MATCH (p:Project {id: $project_id})
        MATCH (skill:Skill {name: $skill_name})
        MERGE (p)-[:USES_SKILL]->(skill)
        """

        for project_id, project_skill_list in project_skills.items():
            for skill_name in project_skill_list:
                session.run(
                    project_skill_query,
                    project_id=project_id,
                    skill_name=skill_name
                )

        print("✓ Project-skill relationships created")

        # -------------------------------------------------
        # 10. SKILL → JOB ROLE
        # -------------------------------------------------

        job_required_skills = {
            "J001": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "NLP",
                "FastAPI",
                "Docker"
            ],
            "J002": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "SQL",
                "Docker"
            ],
            "J003": [
                "Python",
                "Machine Learning",
                "SQL",
                "Pandas",
                "NumPy",
                "Data Analysis"
            ],
            "J004": [
                "Python",
                "FastAPI",
                "SQL",
                "Docker",
                "Git"
            ],
            "J005": [
                "Python",
                "SQL",
                "Pandas",
                "NumPy",
                "Data Analysis"
            ]
        }

        job_skill_query = """
        MATCH (j:JobRole {id: $job_id})
        MATCH (skill:Skill {name: $skill_name})
        MERGE (skill)-[:REQUIRED_FOR]->(j)
        """

        for job_id, required_skills in job_required_skills.items():
            for skill_name in required_skills:
                session.run(
                    job_skill_query,
                    job_id=job_id,
                    skill_name=skill_name
                )

        print("✓ Job-skill relationships created")

        # -------------------------------------------------
        # 11. SKILL → RELATED SKILL
        # -------------------------------------------------

        related_skills = [
            ("Python", "Machine Learning"),
            ("Machine Learning", "Deep Learning"),
            ("Machine Learning", "Data Analysis"),
            ("Python", "FastAPI"),
            ("Python", "Pandas"),
            ("Python", "NumPy"),
            ("NLP", "LangChain"),
            ("Python", "NLP"),
            ("Python", "Computer Vision"),
            ("SQL", "Data Analysis")
        ]

        related_skill_query = """
        MATCH (s1:Skill {name: $skill1})
        MATCH (s2:Skill {name: $skill2})
        MERGE (s1)-[:RELATED_TO]->(s2)
        """

        for skill1, skill2 in related_skills:
            session.run(
                related_skill_query,
                skill1=skill1,
                skill2=skill2
            )

        print("✓ Skill relationships created")

        # -------------------------------------------------
        # 12. JOB ROLE → COMPANY
        # -------------------------------------------------

        job_companies = {
            "J001": ["C001", "C003"],
            "J002": ["C001", "C003", "C004"],
            "J003": ["C002", "C003"],
            "J004": ["C001", "C004"],
            "J005": ["C002"]
        }

        job_company_query = """
        MATCH (j:JobRole {id: $job_id})
        MATCH (c:Company {id: $company_id})
        MERGE (j)-[:OFFERED_BY]->(c)
        """

        for job_id, company_list in job_companies.items():
            for company_id in company_list:
                session.run(
                    job_company_query,
                    job_id=job_id,
                    company_id=company_id
                )

        print("✓ Job-company relationships created")

    print("\n🎉 SkillGraph database seeded successfully!")


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print("\n❌ Error while seeding database:")
        print(e)