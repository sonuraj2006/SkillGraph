MATCH (s:Student {id: $student_id})
      -[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(skill:Skill)
      -[:REQUIRED_FOR]->(role:JobRole)
RETURN s.name AS student,
       p.name AS project,
       skill.name AS skill,
       role.name AS job_role
ORDER BY role.name;
MATCH (s:Student {id: $student_id})
      -[:HAS_SKILL]->(skill:Skill)
      -[:REQUIRED_FOR]->(role:JobRole)
WITH s, role, count(DISTINCT skill) AS matching_skills

MATCH (role)<-[:REQUIRED_FOR]-(required:Skill)

WITH s,
     role,
     matching_skills,
     count(DISTINCT required) AS total_required

RETURN
    role.id AS job_id,
    role.name AS job_role,
    matching_skills,
    total_required,
    round(
        100.0 * matching_skills / total_required,
        1
    ) AS match_percentage
ORDER BY match_percentage DESC;
MATCH (s:Student {id: $student_id})
      -[:HAS_SKILL]->(current:Skill)

MATCH (role:JobRole {id: $job_id})
      <-[:REQUIRED_FOR]-(required:Skill)

WHERE NOT (s)-[:HAS_SKILL]->(required)

RETURN
    role.name AS job_role,
    collect(required.name) AS missing_skills;
    MATCH (s:Student {id: $student_id})
      -[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(skill:Skill)
      -[:REQUIRED_FOR]->(role:JobRole)
      -[:OFFERED_BY]->(company:Company)

RETURN
    role.name AS job_role,
    company.name AS company,
    collect(DISTINCT skill.name) AS relevant_skills,
    count(DISTINCT p) AS related_projects
ORDER BY related_projects DESC;