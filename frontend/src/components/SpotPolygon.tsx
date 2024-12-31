import DraggableVertex from "./DraggableVertex";
import { ParkingSpot, Vertex } from "../types";
import { useState } from "react";
import { Box, NumberInput, Popover, Button } from '@mantine/core'
import { updateParkingSpot } from "../apiService";

interface SpotPolygonProps {
    parking_spot: ParkingSpot;
    colorKey: number;
}

const colors = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'cyan', 'purple', 'pink', 'indigo', 'lime']
const vertexSize = 20

function SpotPolygon({ parking_spot, colorKey }: SpotPolygonProps) {
    const [vertices, setVertices] = useState<Vertex[]>(parking_spot.vertices)
    const [spotLabel, setSpotLabel] = useState<string | number>(parking_spot.spot_num)
    // const [popoverOpened, setPopoverOpened] = useState(false);
    // const [popoverPosition, setPopoverPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
    const color = (colors[colorKey % colors.length])

    const updateSpotNumber = () => {
        const newNum = parseInt(spotLabel.toString())
        const updatedSpot: ParkingSpot = { ...parking_spot, spot_num: newNum }
        updateParkingSpot(updatedSpot)
    }

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

    const handleRightClick = (event: React.MouseEvent) => {
        console.log("wow")
        event.preventDefault(); // Prevent the default context menu
        setPopoverPosition({ x: event.clientX, y: event.clientY });
        setPopoverOpened(true);
    };

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
                onContextMenu={handleRightClick} // Add right-click handler
            >
                <polygon
                    points={vertices
                        .map((v) => `${v.x + vertexSize / 2},${v.y + vertexSize / 2}`)
                        .join(' ')}
                    style={{
                        fill: 'rgba(0, 0, 0, 0.25)', // Semi-transparent red
                        stroke: color, // Optional border
                        strokeWidth: 2,
                        cursor: "context-menu", // Show context menu cursor
                        pointerEvents: "all", // Enable pointer events for polygon
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
            <NumberInput
                variant="unstyled"
                pos='absolute'
                top={centerY}
                left={centerX}
                allowNegative={false}
                allowDecimal={false}
                hideControls
                value={spotLabel}
                onChange={setSpotLabel}
                onBlur={updateSpotNumber}
                styles={{
                    input: {
                        color: "white", // Change font color
                    },
                }}
            />
            {/* <Popover
                opened={popoverOpened}
                onClose={() => setPopoverOpened(false)}
                onChange={setPopoverOpened}
                position="right-start"
                shadow="md"
                styles={{
                    dropdown: { position: 'absolute', top: popoverPosition.y, left: popoverPosition.x },
                }}
            >
                <Popover.Target>
                    <Box style={{ position: 'absolute', left: 0, top: 0 }}></Box>
                </Popover.Target>
                <Popover.Dropdown>
                    <Button variant='subtle' color='gray' onClick={() => console.log("yey")}>
                        Delete Spot {parking_spot.spot_num}
                    </Button>
                </Popover.Dropdown>
            </Popover> */}
        </>
    )
}

export default SpotPolygon