import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load .env from the same folder as this file
load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")

# Check configuration before creating the driver
if not COGNODB_URI:
    raise ValueError("COGNODB_URI is missing from .env")

if not COGNODB_USERNAME:
    raise ValueError("COGNODB_USERNAME is missing from .env")

if not COGNODB_PASSWORD:
    raise ValueError("COGNODB_PASSWORD is missing from .env")

driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)


def test_connection():
    with driver.session() as session:
        result = session.run(
            "RETURN 'CognoDB connection successful' AS message"
        )
        return result.single()["message"]