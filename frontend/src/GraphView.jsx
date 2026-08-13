import { useEffect, useState } from "react";
import axios from "axios";

import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
  Handle,
  Position,
} from "reactflow";

import "reactflow/dist/style.css";
const API_URL = "https://skillgraph-i513.onrender.com";


/* =====================================================
   CUSTOM NODE
   ===================================================== */

function CustomNode({ data }) {
  let background = "#ffffff";
  let border = "#64748b";

  if (data.nodeType === "Student") {
    background = "#eef2ff";
    border = "#6366f1";
  }

  if (data.nodeType === "Project") {
    background = "#ecfeff";
    border = "#06b6d4";
  }

  if (data.nodeType === "Skill") {
    background = "#ecfdf5";
    border = "#22c55e";
  }

  if (data.nodeType === "Job Role") {
    background = "#fff7ed";
    border = "#f97316";
  }

  if (data.nodeType === "Company") {
    background = "#fdf4ff";
    border = "#d946ef";
  }

  return (
    <div
      style={{
        width: "170px",
        minHeight: "55px",
        padding: "10px",
        backgroundColor: background,
        border: `2px solid ${border}`,
        borderRadius: "10px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        boxSizing: "border-box",
        color: "#111827",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        fontWeight: "600",
        fontSize: "13px",
      }}
    >
      <Handle
        type="target"
        position={Position.Left}
        style={{
          background: border,
        }}
      />

      <div
        style={{
          fontSize: "10px",
          fontWeight: "700",
          color: border,
          marginBottom: "5px",
          textTransform: "uppercase",
        }}
      >
        {data.nodeType}
      </div>

      <div
        style={{
          color: "#111827",
          fontWeight: "700",
          wordBreak: "break-word",
        }}
      >
        {data.label}
      </div>

      <Handle
        type="source"
        position={Position.Right}
        style={{
          background: border,
        }}
      />
    </div>
  );
}

const nodeTypes = {
  custom: CustomNode,
};

/* =====================================================
   GRAPH VIEW
   ===================================================== */

function GraphView({ filters }) {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    if (filters) {
      loadGraph();
    }
  }, [filters]);

  /* =====================================================
     LOAD GRAPH
     ===================================================== */

  const loadGraph = async () => {
    try {
      setLoading(true);
      setError("");
      setSelectedNode(null);

      const response = await axios.get(
        `${API_URL}/recommendations/S001/graph`,
        {
          params: {
            project: filters.project,
            skill: filters.skill,
            year: filters.year,
          },
        }
      );

      console.log("GRAPH API RESPONSE:", response.data);

      const connections = response.data.connections || [];

      if (connections.length === 0) {
        setError("No graph connections found.");
        setNodes([]);
        setEdges([]);
        return;
      }

      const nodeMap = new Map();
      const edgeMap = new Map();

      /* =====================================================
         CREATE NODES AND EDGES
         ===================================================== */

      connections.forEach((item) => {
        console.log("GRAPH ITEM:", item);

        const studentId = `student-${item.student_id}`;

        const projectId = `project-${item.project}`;

        const skillId = `skill-${item.skill}`;

        const roleId = `role-${item.job_role}`;

        const companyId = `company-${item.company}`;

        /* ================= STUDENT ================= */

        if (!nodeMap.has(studentId)) {
          nodeMap.set(studentId, {
            id: studentId,
            type: "custom",
            data: {
              label: item.student || "Student",
              nodeType: "Student",
            },
            position: {
              x: 0,
              y: 0,
            },
          });
        }

        /* ================= PROJECT ================= */

        if (!nodeMap.has(projectId)) {
          nodeMap.set(projectId, {
            id: projectId,
            type: "custom",
            data: {
              label: item.project || "Project",
              nodeType: "Project",
            },
            position: {
              x: 300,
              y: 0,
            },
          });
        }

        /* ================= SKILL ================= */

        if (!nodeMap.has(skillId)) {
          nodeMap.set(skillId, {
            id: skillId,
            type: "custom",
            data: {
              label: item.skill || "Skill",
              nodeType: "Skill",
            },
            position: {
              x: 600,
              y: 0,
            },
          });
        }

        /* ================= JOB ================= */

        if (!nodeMap.has(roleId)) {
          nodeMap.set(roleId, {
            id: roleId,
            type: "custom",
            data: {
              label: item.job_role || "Job Role",
              nodeType: "Job Role",
            },
            position: {
              x: 900,
              y: 0,
            },
          });
        }

        /* ================= COMPANY ================= */

        if (!nodeMap.has(companyId)) {
          nodeMap.set(companyId, {
            id: companyId,
            type: "custom",
            data: {
              label: item.company || "Company",
              nodeType: "Company",
            },
            position: {
              x: 1200,
              y: 0,
            },
          });
        }

        /* =====================================================
           EDGES
           ===================================================== */

        edgeMap.set(
          `${studentId}-${projectId}`,
          {
            id: `${studentId}-${projectId}`,
            source: studentId,
            target: projectId,
            label: "WORKED ON",
            type: "smoothstep",
            markerEnd: {
              type: MarkerType.ArrowClosed,
            },
          }
        );

        edgeMap.set(
          `${projectId}-${skillId}`,
          {
            id: `${projectId}-${skillId}`,
            source: projectId,
            target: skillId,
            label: "USES SKILL",
            type: "smoothstep",
            markerEnd: {
              type: MarkerType.ArrowClosed,
            },
          }
        );

        edgeMap.set(
          `${skillId}-${roleId}`,
          {
            id: `${skillId}-${roleId}`,
            source: skillId,
            target: roleId,
            label: "REQUIRED FOR",
            type: "smoothstep",
            markerEnd: {
              type: MarkerType.ArrowClosed,
            },
          }
        );

        edgeMap.set(
          `${roleId}-${companyId}`,
          {
            id: `${roleId}-${companyId}`,
            source: roleId,
            target: companyId,
            label: "OFFERED BY",
            type: "smoothstep",
            markerEnd: {
              type: MarkerType.ArrowClosed,
            },
          }
        );
      });

      /* =====================================================
         GROUP NODES
         ===================================================== */

      const students = [];
      const projects = [];
      const skills = [];
      const jobs = [];
      const companies = [];

      nodeMap.forEach((node) => {
        if (node.data.nodeType === "Student") {
          students.push(node);
        }

        if (node.data.nodeType === "Project") {
          projects.push(node);
        }

        if (node.data.nodeType === "Skill") {
          skills.push(node);
        }

        if (node.data.nodeType === "Job Role") {
          jobs.push(node);
        }

        if (node.data.nodeType === "Company") {
          companies.push(node);
        }
      });

      /* =====================================================
         POSITIONS
         ===================================================== */

      students.forEach((node, index) => {
        node.position = {
          x: 0,
          y: 150 + index * 160,
        };
      });

      projects.forEach((node, index) => {
        node.position = {
          x: 300,
          y: 150 + index * 160,
        };
      });

      skills.forEach((node, index) => {
        node.position = {
          x: 600,
          y: 100 + index * 130,
        };
      });

      jobs.forEach((node, index) => {
        node.position = {
          x: 900,
          y: 100 + index * 130,
        };
      });

      companies.forEach((node, index) => {
        node.position = {
          x: 1200,
          y: 100 + index * 150,
        };
      });

      /* =====================================================
         SET GRAPH
         ===================================================== */

      setNodes([
        ...students,
        ...projects,
        ...skills,
        ...jobs,
        ...companies,
      ]);

      setEdges(Array.from(edgeMap.values()));

    } catch (err) {
      console.error("Graph loading error:", err);

      setNodes([]);
      setEdges([]);

      setError(
        err.response?.data?.detail ||
        "Unable to load graph."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =====================================================
     LOADING
     ===================================================== */

  if (loading) {
    return (
      <div className="graph-message">
        <h3>Loading SkillGraph...</h3>
        <p>
          Finding matching careers and companies.
        </p>
      </div>
    );
  }

  /* =====================================================
     ERROR
     ===================================================== */

  if (error) {
    return (
      <div className="graph-message error-message">
        <h3>No Graph Found</h3>
        <p>{error}</p>
      </div>
    );
  }

  /* =====================================================
     GRAPH
     ===================================================== */

  return (
    <div
      className="graph-wrapper"
      style={{
        width: "100%",
      }}
    >

      {/* LEGEND */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          flexWrap: "wrap",
          padding: "15px",
          marginBottom: "10px",
          fontSize: "14px",
          fontWeight: "600",
        }}
      >
        <span>🟣 Student</span>
        <span>🔵 Project</span>
        <span>🟢 Skill</span>
        <span>🟠 Job Role</span>
        <span>🩷 Company</span>
      </div>

      {/* GRAPH */}

      <div
        style={{
          width: "100%",
          height: "700px",
          border: "1px solid #ddd",
          borderRadius: "12px",
          background: "#ffffff",
        }}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={(event, node) => {
            setSelectedNode(node);
          }}
          fitView
          fitViewOptions={{
            padding: 0.2,
          }}
          minZoom={0.3}
          maxZoom={1.5}
        >

          <Background
            variant="dots"
            gap={20}
            size={1}
          />

          <Controls />

          <MiniMap
            nodeStrokeWidth={3}
            zoomable
            pannable
            position="top-right"
          />

        </ReactFlow>
      </div>

      {/* SELECTED NODE */}

      {selectedNode && (
        <div
          style={{
            marginTop: "15px",
            padding: "20px",
            border: "1px solid #ddd",
            borderRadius: "10px",
            background: "#ffffff",
          }}
        >

          <button
            onClick={() => setSelectedNode(null)}
            style={{
              float: "right",
              border: "none",
              background: "transparent",
              fontSize: "22px",
              cursor: "pointer",
            }}
          >
            ×
          </button>

          <div
            style={{
              fontSize: "12px",
              fontWeight: "700",
              color: "#6366f1",
              textTransform: "uppercase",
            }}
          >
            {selectedNode.data.nodeType}
          </div>

          <h3>
            {selectedNode.data.label}
          </h3>

        </div>
      )}

    </div>
  );
}

export default GraphView;