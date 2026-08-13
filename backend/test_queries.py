from database import driver


def test_student_skills():
    with driver.session() as session:

        query = """
        MATCH (s:Student {id: $student_id})
              -[:HAS_SKILL]->(skill:Skill)

        RETURN s.name AS student,
               collect(skill.name) AS skills
        """

        result = session.run(
            query,
            student_id="S001"
        )

        record = result.single()

        print("\nStudent:")
        print(record["student"])

        print("\nSkills:")
        for skill in record["skills"]:
            print("-", skill)


if __name__ == "__main__":
    test_student_skills()