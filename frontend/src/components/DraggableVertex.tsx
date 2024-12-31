import Draggable, { DraggableEvent, DraggableData } from "react-draggable";
import { Vertex } from "../types";
import { useState } from "react";
import {updateVertex} from "../apiService.ts";

type DraggableVertexProps = {
    vertex: Vertex;
};

function DraggableVertex({ vertex }: DraggableVertexProps) {
    const [position, setPosition] = useState({ x: vertex.x, y: vertex.y });
  
    const handleDrag = (e: DraggableEvent, data: DraggableData) => {
    //   const updatedVertex: Vertex = { ...vertex, x: data.x, y: data.y };
      setPosition({ x: data.x, y: data.y });
    //   updateVertex(updatedVertex);
    };
  
    const handleStop = (e: DraggableEvent, data: DraggableData) => {
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
        <div className="ball" style={{ backgroundColor: 'red' }} />
      </Draggable>
    );
  }

export default DraggableVertex