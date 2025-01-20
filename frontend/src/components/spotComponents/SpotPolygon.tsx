import DraggableVertex from "./DraggableVertex";
import { ParkingSpot, Vertex } from "../../types";
import { useState } from "react";
import { Box, NumberInput, Popover, Button } from '@mantine/core'
import hashSpotColor from "./hashSpotColor";

interface SpotPolygonProps {
    parking_spot: ParkingSpot;
    colorKey: number;
    deleteSpot: (spot: ParkingSpot) => void
    handleUpdateSpot: (spot: ParkingSpot) => void
    editMode: boolean
}

const vertexSize = 20

function SpotPolygon({ parking_spot, colorKey, deleteSpot, handleUpdateSpot, editMode }: SpotPolygonProps) {
    const [vertices, setVertices] = useState<Vertex[]>(parking_spot.vertices)
    const [spotLabel, setSpotLabel] = useState<string | number>(parking_spot.spot_num)
    const [popoverOpened, setPopoverOpened] = useState(false);
    const [popoverPosition, setPopoverPosition] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

    const color = hashSpotColor(colorKey)

    const updateSpotNumber = () => {
        const newNum = parseInt(spotLabel.toString())
        const updatedSpot: ParkingSpot = { ...parking_spot, spot_num: newNum }
        handleUpdateSpot(updatedSpot)
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
        event.preventDefault(); // Prevent the default context menu
        setPopoverPosition({ x: event.pageX, y: event.pageY }); // Use pageX and pageY for proper positioning
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
                onContextMenu={editMode ? handleRightClick : undefined} //Right click handler
            >
                <polygon
                    points={vertices
                        .map((v) => `${v.x + vertexSize / 2},${v.y + vertexSize / 2}`)
                        .join(' ')}
                    style={{
                        fill: 'rgba(0, 0, 0, 0.25)', // Semi-transparent fill
                        stroke: color, // Optional border
                        strokeWidth: 2,
                        cursor: editMode ? "context-menu" : "default", // Change cursor based on editMode
                        pointerEvents: "all", // Enable pointer events for polygon
                    }}
                />
            </svg>
            {editMode && vertices.map((vertex, index) => (
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
                disabled={!editMode}
                fw={editMode ? 500 : 300}
                styles={{
                    input: {
                        color: "white", // Change font color
                        backgroundColor: "transparent"
                    },
                }}
            />
            <Popover
                opened={popoverOpened}
                onClose={() => setPopoverOpened(false)}
                onChange={setPopoverOpened}
                position="bottom-start"
                shadow="md"
                styles={{
                    dropdown: { position: 'absolute', top: popoverPosition.y, left: popoverPosition.x },
                }}
            >
                <Popover.Target>
                    <Box style={{ position: 'absolute', left: 0, top: 0 }}></Box>
                </Popover.Target>
                <Popover.Dropdown>
                    <Button variant='subtle' color='gray' onClick={() => deleteSpot(parking_spot)}>
                        Delete Spot {parking_spot.spot_num}
                    </Button>
                </Popover.Dropdown>
            </Popover>
        </>
    )
}

export default SpotPolygon