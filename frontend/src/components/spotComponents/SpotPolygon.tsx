import DraggableVertex from "./DraggableVertex";
import { ParkingSpot, Vertex } from "../../types";
import { useEffect, useState } from "react";
import { Box, NumberInput, Popover, Button } from "@mantine/core";
import hashSpotColor from "./hashSpotColor";
import { updateVertex } from "../../api/apiService";


interface SpotPolygonProps {
  xScale: number;
  yScale: number;
  spot: ParkingSpot;
  colorKey: number;
  deleteSpot: (spot: ParkingSpot) => void;
  handleUpdateSpot: (spot: ParkingSpot) => void;
  setSpot: (spot: ParkingSpot) => void;
  editMode: boolean;
}

export default function SpotPolygon({
  xScale,
  yScale,
  spot,
  colorKey,
  deleteSpot,
  handleUpdateSpot,
  setSpot,
  editMode,
}: SpotPolygonProps) {

  //consts
  const scaledVertices = spot.vertices.map((vertex) => ({
    ...vertex,
    y: vertex.y * yScale,
    x: vertex.x * xScale,
  }));
  const color = hashSpotColor(colorKey);

  console.log(xScale)
  console.log(yScale)
  console.log(scaledVertices)


  //states
  const [centerX, centerY] = calculateCentroid(scaledVertices);
  const [spotLabel, setSpotLabel] = useState<string | number>(spot.spot_num);
  const [popoverOpened, setPopoverOpened] = useState(false);
  const [popoverPosition, setPopoverPosition] = useState<{
    x: number;
    y: number;
  }>({ x: 0, y: 0 });

  /*
  Functions
  */
  const handleRightClick = (event: React.MouseEvent) => {
    event.preventDefault(); // Prevent the default context menu
    setPopoverPosition({ x: event.pageX, y: event.pageY }); // Use pageX and pageY for proper positioning
    setPopoverOpened(true);
  };


  const updateSpotNumber = () => {
    const newNum = parseInt(spotLabel.toString());
    const updatedSpot: ParkingSpot = { ...spot, spot_num: newNum };
    handleUpdateSpot(updatedSpot);
  };

  function updateVertexPosition(vertex: Vertex) {
     const normalizedVertex ={
      ...vertex,
      y: Math.round(vertex.y / yScale),
      x: Math.round(vertex.x / xScale),
    };
    const updatedVertices = spot.vertices.map((v) => (v.id === vertex.id ? normalizedVertex : v))
    const updatedSpot: ParkingSpot = { ...spot, vertices: updatedVertices}
    setSpot(updatedSpot)
  }

  async function handleUpdateVertex(vertex: Vertex){ 
    const normalizedVertex ={
      ...vertex,
      y: Math.round(vertex.y / yScale),
      x: Math.round(vertex.x / xScale),
    };
    await updateVertex(normalizedVertex)
  }

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
          points={scaledVertices
            .map((v) => `${v.x},${v.y}`)
            .join(" ")}
          style={{
            fill: "rgba(0, 0, 0, 0.25)", // Semi-transparent fill
            stroke: color, // Optional border
            strokeWidth: 2,
            cursor: editMode ? "context-menu" : "default", // Change cursor based on editMode
            pointerEvents: "all", // Enable pointer events for polygon
          }}
        />
      </svg>
      {editMode &&
        scaledVertices.map((vertex, index) => (
          <DraggableVertex
            key={index}
            vertex={vertex}
            color={color}
            updateVertexPosition={updateVertexPosition}
            handleUpdateVertex={handleUpdateVertex}
          />
        ))}
      <NumberInput
        variant="unstyled"
        pos="absolute"
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
            backgroundColor: "transparent",
            textAlign: 'center'
          },
        }}
        style={{
          transform: 'translate(-50%, -50%)'
        }}
      />
      <Popover
        opened={popoverOpened}
        onClose={() => setPopoverOpened(false)}
        onChange={setPopoverOpened}
        position="bottom-start"
        shadow="md"
        styles={{
          dropdown: {
            position: "absolute",
            top: popoverPosition.y,
            left: popoverPosition.x,
          },
        }}
      >
        <Popover.Target>
          <Box style={{ position: "absolute", left: 0, top: 0 }}></Box>
        </Popover.Target>
        <Popover.Dropdown>
          <Button
            variant="subtle"
            color="gray"
            onClick={() => deleteSpot(spot)}
          >
            Delete Spot {spot.spot_num}
          </Button>
        </Popover.Dropdown>
      </Popover>
    </>
  );
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
