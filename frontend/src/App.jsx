import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import GraphView from "./GraphView";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [year, setYear] = useState("");
  const [project, setProject] = useState("");
  const [skill, setSkill] = useState("");

  const [years, setYears] = useState([]);
  const [projects, setProjects] = useState([]);
  const [skills, setSkills] = useState([]);

  const [filters, setFilters] = useState(null);

  const [loadingProjects, setLoadingProjects] = useState(false);
  const [loadingSkills, setLoadingSkills] = useState(false);

  // Load available years when page opens
  useEffect(() => {
    loadYears();
  }, []);

  const loadYears = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/recommendations/filters`
      );

      setYears(response.data.years || []);
    } catch (error) {
      console.error("Unable to load years:", error);
    }
  };

  // Load projects when year changes
  const handleYearChange = async (value) => {
    setYear(value);
    setProject("");
    setSkill("");
    setSkills([]);
    setFilters(null);

    if (!value) {
      setProjects([]);
      return;
    }

    try {
      setLoadingProjects(true);

      const response = await axios.get(
        `${API_URL}/recommendations/filters`,
        {
          params: {
            year: Number(value),
          },
        }
      );

      setProjects(response.data.projects || []);
    } catch (error) {
      console.error("Unable to load projects:", error);
      setProjects([]);
    } finally {
      setLoadingProjects(false);
    }
  };

  // Load skills when project changes
  const handleProjectChange = async (value) => {
    setProject(value);
    setSkill("");
    setFilters(null);

    if (!value) {
      setSkills([]);
      return;
    }

    try {
      setLoadingSkills(true);

      const response = await axios.get(
        `${API_URL}/recommendations/filters`,
        {
          params: {
            year: Number(year),
            project: value,
          },
        }
      );

      setSkills(response.data.skills || []);
    } catch (error) {
      console.error("Unable to load skills:", error);
      setSkills([]);
    } finally {
      setLoadingSkills(false);
    }
  };

  const handleGenerate = () => {
    if (!year || !project || !skill) {
      alert("Please select Year, Project and Skill.");
      return;
    }

    setFilters({
      year: Number(year),
      project,
      skill,
    });
  };

  const handleClear = () => {
    setYear("");
    setProject("");
    setSkill("");

    setProjects([]);
    setSkills([]);

    setFilters(null);
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">

        <div>
          <h1>SkillGraph</h1>

          <p>
            Student Skill & Career Explorer
          </p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Connected
        </div>

      </header>


      <main className="container">

        {/* HERO */}

        <section className="hero">

          <h2>
            Explore Your Career Path
          </h2>

          <p>
            Select your academic year, project and
            skill to discover relevant careers and companies.
          </p>

        </section>


        {/* FILTER CARD */}

        <section className="input-card">

          <h2>
            Build Your Skill Graph
          </h2>


          <div className="form-grid">

            {/* YEAR */}

            <div className="form-group">

              <label>
                Academic Year
              </label>

              <select
                value={year}
                onChange={(e) =>
                  handleYearChange(e.target.value)
                }
              >

                <option value="">
                  Select Year
                </option>

                {years.map((item) => (

                  <option
                    key={item}
                    value={item}
                  >
                    Year {item}
                  </option>

                ))}

              </select>

            </div>


            {/* PROJECT */}

            <div className="form-group">

              <label>
                Project
              </label>

              <select
                value={project}
                onChange={(e) =>
                  handleProjectChange(e.target.value)
                }
                disabled={!year || loadingProjects}
              >

                <option value="">
                  {loadingProjects
                    ? "Loading projects..."
                    : "Select Project"}
                </option>

                {projects.map((item) => (

                  <option
                    key={item}
                    value={item}
                  >
                    {item}
                  </option>

                ))}

              </select>

            </div>


            {/* SKILL */}

            <div className="form-group">

              <label>
                Skill
              </label>

              <select
                value={skill}
                onChange={(e) => {
                  setSkill(e.target.value);
                  setFilters(null);
                }}
                disabled={!project || loadingSkills}
              >

                <option value="">
                  {loadingSkills
                    ? "Loading skills..."
                    : "Select Skill"}
                </option>

                {skills.map((item) => (

                  <option
                    key={item}
                    value={item}
                  >
                    {item}
                  </option>

                ))}

              </select>

            </div>

          </div>


          {/* BUTTONS */}

          <div className="button-row">

            <button
              className="generate-button"
              onClick={handleGenerate}
              disabled={
                !year ||
                !project ||
                !skill
              }
            >
              Generate Skill Graph
            </button>


            {filters && (

              <button
                className="clear-button"
                onClick={handleClear}
              >
                Clear
              </button>

            )}

          </div>

        </section>


        {/* GRAPH */}

        {filters && (

          <section className="graph-section">

            <div className="graph-heading">

              <div>

                <h2>
                  Your Skill Graph
                </h2>

                <p>

                  Showing results for{" "}

                  <strong>
                    Year {filters.year}
                  </strong>

                  {" • "}

                  <strong>
                    {filters.project}
                  </strong>

                  {" • "}

                  <strong>
                    {filters.skill}
                  </strong>

                </p>

              </div>

            </div>


            <GraphView
              filters={filters}
            />

          </section>

        )}

      </main>

    </div>
  );
}

export default App;