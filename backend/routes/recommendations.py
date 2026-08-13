from fastapi import APIRouter, HTTPException
from database import driver
from typing import Optional

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


# ============================================================
# 1. FILTERS
# ============================================================

@router.get("/filters")
def get_graph_filters(
    year: Optional[int] = None,
    project: Optional[str] = None
):
    try:
        with driver.session() as session:

            query = """
            MATCH (s:Student)-[:WORKED_ON]->(p:Project)
                  -[:USES_SKILL]->(skill:Skill)

            WHERE
                ($year IS NULL OR s.year = $year)
                AND
                ($project IS NULL OR toLower(p.name) = toLower($project))

            RETURN DISTINCT
                s.year AS year,
                p.name AS project,
                skill.name AS skill

            ORDER BY year, project, skill
            """

            result = session.run(
                query,
                year=year,
                project=project
            )

            records = [record.data() for record in result]

            years = sorted(set(
                record["year"]
                for record in records
                if record["year"] is not None
            ))

            projects = sorted(set(
                record["project"]
                for record in records
                if record["project"] is not None
            ))

            skills = sorted(set(
                record["skill"]
                for record in records
                if record["skill"] is not None
            ))

            return {
                "years": years,
                "projects": projects,
                "skills": skills
            }

    except Exception as e:

        print("FILTER ERROR:", e)

        raise HTTPException(
            status_code=503,
            detail=f"Unable to load filters: {str(e)}"
        )


# ============================================================
# 2. STUDENT GRAPH
# ============================================================

@router.get("/{student_id}/graph")
def explore_student_graph(
    student_id: str,
    project: Optional[str] = None,
    skill: Optional[str] = None,
    year: Optional[int] = None
):

    try:

        with driver.session() as session:

            query = """
            MATCH (s:Student)
                  -[:WORKED_ON]->(p:Project)
                  -[:USES_SKILL]->(skill:Skill)
                  -[:REQUIRED_FOR]->(role:JobRole)
                  <-[:REQUIRED_FOR]-(required:Skill)

            OPTIONAL MATCH (role)
                  -[:OFFERED_BY]->(company:Company)

            WHERE
                s.id = $student_id

                AND
                ($project IS NULL OR
                 toLower(p.name) = toLower($project))

                AND
                ($skill IS NULL OR
                 toLower(skill.name) = toLower($skill))

                AND
                ($year IS NULL OR
                 s.year = $year)

            RETURN DISTINCT
                s.name AS student,
                s.id AS student_id,
                s.year AS year,
                p.name AS project,
                skill.name AS skill,
                role.name AS job_role,
                company.name AS company

            ORDER BY
                p.name,
                skill.name,
                role.name,
                company.name
            """

            result = session.run(
                query,
                student_id=student_id,
                project=project,
                skill=skill,
                year=year
            )

            paths = [
                record.data()
                for record in result
            ]

            if not paths:

                raise HTTPException(
                    status_code=404,
                    detail="No graph connections found for the selected filters"
                )

            return {
                "student_id": student_id,

                "filters": {
                    "project": project,
                    "skill": skill,
                    "year": year
                },

                "connections": paths
            }

    except HTTPException:
        raise

    except Exception as e:

        print("GRAPH ERROR:", e)

        raise HTTPException(
            status_code=503,
            detail=f"Unable to explore student graph: {str(e)}"
        )


# ============================================================
# 3. RECOMMENDATIONS
# ============================================================

@router.get("/{student_id}")
def get_recommendations(student_id: str):

    try:

        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})
                  -[:HAS_SKILL]->(skill:Skill)
                  -[:REQUIRED_FOR]->(role:JobRole)

            WITH
                s,
                role,
                count(DISTINCT skill) AS matching_skills

            MATCH (role)
                  <-[:REQUIRED_FOR]-(required:Skill)

            WITH
                s,
                role,
                matching_skills,
                count(DISTINCT required) AS total_required

            WHERE total_required > 0

            RETURN
                role.id AS job_id,
                role.name AS job_role,
                matching_skills,
                total_required,
                100.0 * matching_skills / total_required
                    AS match_percentage

            ORDER BY match_percentage DESC
            """

            result = session.run(
                query,
                student_id=student_id
            )

            recommendations = [
                record.data()
                for record in result
            ]

            if not recommendations:

                raise HTTPException(
                    status_code=404,
                    detail="No recommendations found"
                )

            return {
                "student_id": student_id,
                "recommendations": recommendations
            }

    except HTTPException:
        raise

    except Exception as e:

        print("RECOMMENDATION ERROR:", e)

        raise HTTPException(
            status_code=503,
            detail=f"Unable to generate recommendations: {str(e)}"
        )


# ============================================================
# 4. MISSING SKILLS
# ============================================================

@router.get("/{student_id}/{job_id}/missing-skills")
def get_missing_skills(
    student_id: str,
    job_id: str
):

    try:

        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})

            MATCH (role:JobRole {id: $job_id})
                  <-[:REQUIRED_FOR]-(required:Skill)

            OPTIONAL MATCH
                (s)-[:HAS_SKILL]->(owned:Skill)

            WITH
                role,
                required,
                collect(owned.name) AS owned_skills

            WHERE NOT required.name IN owned_skills

            RETURN
                role.name AS job_role,
                collect(required.name) AS missing_skills
            """

            result = session.run(
                query,
                student_id=student_id,
                job_id=job_id
            )

            record = result.single()

            if record is None:

                raise HTTPException(
                    status_code=404,
                    detail="Student or job role not found"
                )

            return {
                "job_role": record["job_role"],
                "missing_skills": record["missing_skills"]
            }

    except HTTPException:
        raise

    except Exception as e:

        print("MISSING SKILLS ERROR:", e)

        raise HTTPException(
            status_code=503,
            detail=f"Unable to calculate missing skills: {str(e)}"
        )


# ============================================================
# 5. GRAPH SUMMARY
# ============================================================

@router.get("/{student_id}/graph-summary")
def graph_summary(student_id: str):

    try:

        with driver.session() as session:

            query = """
            MATCH (s:Student {id: $student_id})
                  -[:WORKED_ON]->(p:Project)
                  -[:USES_SKILL]->(skill:Skill)
                  -[:REQUIRED_FOR]->(role:JobRole)

            OPTIONAL MATCH
                (role)-[:OFFERED_BY]->(company:Company)

            RETURN
                collect(DISTINCT p.name) AS projects,
                collect(DISTINCT skill.name) AS skills,
                collect(DISTINCT role.name) AS job_roles,
                collect(DISTINCT company.name) AS companies
            """

            result = session.run(
                query,
                student_id=student_id
            )

            record = result.single()

            if record is None:

                raise HTTPException(
                    status_code=404,
                    detail="Student graph not found"
                )

            return {
                "student_id": student_id,
                "projects": record["projects"],
                "skills": record["skills"],
                "job_roles": record["job_roles"],
                "companies": record["companies"]
            }

    except HTTPException:
        raise

    except Exception as e:

        print("SUMMARY ERROR:", e)

        raise HTTPException(
            status_code=503,
            detail=f"Unable to generate graph summary: {str(e)}"
        )