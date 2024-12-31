import DraggableVertex from "./DraggableVertex";
import { ParkingSpot, Vertex } from "../types";
import { useState } from "react";

interface SpotPolygonProps {
    parking_spot: ParkingSpot;
}

const colors = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'cyan', 'purple', 'pink', 'indigo', 'lime']

function SpotPolygon({ parking_spot }: SpotPolygonProps) {
    const [vertices, setVertices] = useState<Vertex[]>(parking_spot.vertices)
    console.log(vertices)
    const color = colors[parking_spot.spot_num % colors.length]

    return (
        <>
            <svg
                style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "100%",
                    height: "100%",
                    pointerEvents: "none", // Prevent blocking interactions with DraggableVertex
                }}
            >
                <polygon
                    points={vertices
                        .map((v) => `${v.x+10},${v.y+10}`)
                        .join(' ')}
                    style={{
                        fill: 'rgba(0, 0, 0, 0.25)', // Semi-transparent red
                        stroke: color, // Optional border
                        strokeWidth: 2,
                    }}
                />
            </svg>
            {vertices.map((vertex, index) => (
                <DraggableVertex
                    key={index}
                    vertex={vertex}
                    color={color}
                    updateVertices={(updatedVertex) => setVertices(vertices.map((v) => (v.id === vertex.id ? updatedVertex : v)))}
                />
            ))}
        </>
    )
}

export default SpotPolygon