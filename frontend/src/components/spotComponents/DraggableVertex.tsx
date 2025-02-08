import Draggable, { DraggableEvent, DraggableData } from "react-draggable";
import { Vertex } from "../../types.ts";

const vertexSize = 20;

interface DraggableVertexProps {
  vertex: Vertex;
  color: string;
  updateVertexPosition: (vertex: Vertex) => void;
  handleUpdateVertex: (vertex: Vertex) => void;
}

function DraggableVertex({
  vertex,
  color,
  updateVertexPosition,
  handleUpdateVertex,
}: DraggableVertexProps) {
  const position = { x: vertex.x - vertexSize / 2, y: vertex.y - vertexSize / 2 };

  const handleDrag = (_: DraggableEvent, data: DraggableData) => {
    // Update the vertex in the array
    const updatedVertex: Vertex = {
      ...vertex,
      x: Math.round(data.x + vertexSize / 2),
      y: Math.round(data.y + vertexSize / 2),
    };
    updateVertexPosition(updatedVertex);
  };

  const handleStop = (_: DraggableEvent, data: DraggableData) => {
    const updatedVertex: Vertex = {
      ...vertex,
      x: Math.round(data.x + vertexSize / 2),
      y: Math.round(data.y + vertexSize / 2),
    };
    handleUpdateVertex(updatedVertex)
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
