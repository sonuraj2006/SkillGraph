MATCH (s:Student)
RETURN s.id AS id,
       s.name AS name,
       s.degree AS degree,
       s.year AS year
ORDER BY s.name;
MATCH (s:Student {id: $student_id})-[:HAS_SKILL]->(skill:Skill)
RETURN s.name AS student,
       collect(skill.name) AS skills;
       MATCH (s:Student {id: $student_id})-[:WORKED_ON]->(p:Project)
RETURN s.name AS student,
       p.id AS project_id,
       p.name AS project,
       p.description AS description;
       MATCH (s:Student {id: $student_id})
      -[:WORKED_ON]->(p:Project)
      -[:USES_SKILL]->(skill:Skill)
RETURN s.name AS student,
       p.name AS project,
       collect(DISTINCT skill.name) AS skills;