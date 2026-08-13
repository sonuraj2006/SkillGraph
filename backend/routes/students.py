from fastapi import APIRouter, HTTPException
from database import driver

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("")
def get_students():
    try:
        with driver.session() as session:
            query = """
            MATCH (s:Student)
            RETURN s.id AS id,
                   s.name AS name,
                   s.degree AS degree,
                   s.year AS year
            ORDER BY s.name
            """

            result = session.run(query)

            students = [record.data() for record in result]

            return {
                "students": students
            }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve students from CognoDB"
        )


@router.get("/{student_id}/skills")
def get_student_skills(student_id: str):
    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})
                  -[:HAS_SKILL]->(skill:Skill)

            RETURN s.name AS student,
                   collect(skill.name) AS skills
            """

            result = session.run(
                query,
                student_id=student_id
            )

            record = result.single()

            if record is None:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found"
                )

            return {
                "student": record["student"],
                "skills": record["skills"]
            }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve student skills"
        )


@router.get("/{student_id}/projects")
def get_student_projects(student_id: str):
    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})
                  -[:WORKED_ON]->(p:Project)

            RETURN p.id AS project_id,
                   p.name AS project,
                   p.description AS description
            ORDER BY p.name
            """

            result = session.run(
                query,
                student_id=student_id
            )

            projects = [record.data() for record in result]

            return {
                "student_id": student_id,
                "projects": projects
            }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve student projects"
        )