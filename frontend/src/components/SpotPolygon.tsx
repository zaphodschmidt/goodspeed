import DraggableVertex from "./DraggableVertex";
import { ParkingSpot, Vertex } from "../types";
import { useState } from "react";
import { Text } from '@mantine/core'

interface SpotPolygonProps {
    parking_spot: ParkingSpot;
}

const colors = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'cyan', 'purple', 'pink', 'indigo', 'lime']
const vertexSize = 20

function SpotPolygon({ parking_spot }: SpotPolygonProps) {
    const [vertices, setVertices] = useState<Vertex[]>(parking_spot.vertices)
    const color = colors[parking_spot.spot_num % colors.length]
    
    const calculateCentroid = (vertices: Vertex[]): [number, number] => {
        let signedArea = 0; // Accumulate the polygon's signed area
        let Cx = 0; // Accumulate x-coordinate of centroid
        let Cy = 0; // Accumulate y-coordinate of centroid
    
        const n = vertices.length;
    
        for (let i = 0; i < n; i++) {
            const x0 = vertices[i].x;
            const y0 = vertices[i].y;
            const x1 = vertices[(i + 1) % n].x; // Wrap around to the first vertex
            const y1 = vertices[(i + 1) % n].y;
    
            const a = x0 * y1 - x1 * y0; // Calculate cross product
            signedArea += a;
            Cx += (x0 + x1) * a;
            Cy += (y0 + y1) * a;
        }
    
        signedArea *= 0.5;
        Cx = Cx / (6 * signedArea);
        Cy = Cy / (6 * signedArea);
    
        return [Cx, Cy];
    };
    

    const [centerX, centerY] = calculateCentroid(vertices)
    console.log(centerX)
    console.log(centerY)


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
                        .map((v) => `${v.x+vertexSize/2},${v.y+vertexSize/2}`)
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
                    vertexSize={vertexSize}
                    updateVertices={(updatedVertex) => setVertices(vertices.map((v) => (v.id === vertex.id ? updatedVertex : v)))}
                />
            ))}
            <Text 
                pos='absolute' 
                top={centerY} 
                left={centerX}
                c='white'
            >
                {parking_spot.spot_num}
            </Text>
        </>
    )
}

export default SpotPolygon