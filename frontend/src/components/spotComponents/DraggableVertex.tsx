import Draggable, { DraggableEvent, DraggableData } from "react-draggable";
import { Vertex } from "../../types.ts";
import { useState } from "react";
import { updateVertex } from "../../apiService.ts";

interface DraggableVertexProps {
  xScale: number;
  yScale: number;
  vertex: Vertex;
  color: string;
  vertexSize: number;
  updateVertices: (vertex: Vertex) => void;
}

function DraggableVertex({
  // yScale,
  // xScale,
  vertex,
  color,
  vertexSize,
  updateVertices,
}: DraggableVertexProps) {
  const [position, setPosition] = useState({ x: vertex.x, y: vertex.y });

  const handleDrag = (_: DraggableEvent, data: DraggableData) => {
    setPosition({ x: data.x, y: data.y });

    // Update the vertex in the array
    const updatedVertex: Vertex = { ...vertex, x: data.x, y: data.y };
    updateVertices(updatedVertex);
  };

  const handleStop = (_: DraggableEvent, data: DraggableData) => {
    const updatedVertex: Vertex = { ...vertex, x: data.x, y: data.y };
    updateVertex(updatedVertex);
  };

  return (
    <Draggable
      position={position}
      onDrag={handleDrag}
      onStop={handleStop}
      bounds="parent"
    >
      <div
        className="ball"
        style={{
          backgroundColor: color,
          width: `${vertexSize}px`,
          height: `${vertexSize}px`,
          position: "absolute",
        }}
      />
    </Draggable>
  );
}

export default DraggableVertex;
