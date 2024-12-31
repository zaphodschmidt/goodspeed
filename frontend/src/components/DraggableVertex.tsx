import Draggable, { DraggableEvent, DraggableData } from "react-draggable";
import { Vertex } from "../types";
import React, { useState } from "react";
import { updateVertex } from "../apiService.ts";

interface DraggableVertexProps {
    vertex: Vertex;
    color: string;
    updateVertices: (vertex: Vertex) => void
};

const size = 20

function DraggableVertex({ vertex, color, updateVertices }: DraggableVertexProps) {
    const [position, setPosition] = useState({ x: vertex.x, y: vertex.y });

    const handleDrag = (e: DraggableEvent, data: DraggableData) => {
        setPosition({ x: data.x, y: data.y });

        // Update the vertex in the array
        const updatedVertex: Vertex = { ...vertex, x: data.x, y: data.y };
        updateVertices(updatedVertex);
    };

    const handleStop = (e: DraggableEvent, data: DraggableData) => {
        console.log(position)
        const updatedVertex: Vertex = { ...vertex, x: data.x, y: data.y };
        updateVertex(updatedVertex);
    };

    return (
        <Draggable
            position={position}
            onDrag={handleDrag}
            onStop={handleStop}
            bounds='parent'
        >
            <div
                className="ball"
                style={{
                    backgroundColor: color,
                    width: `${size}px`,
                    height: `${size}px`,
                    position: 'absolute',
                    transform: 'translate(-50%, -50%)'
                }}
            />
        </Draggable>
    );
}

export default DraggableVertex