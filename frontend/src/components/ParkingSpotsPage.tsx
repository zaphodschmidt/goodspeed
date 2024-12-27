import React, { useRef, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Building } from "../types";
import { Button, Stack, Flex, Box, BackgroundImage } from "@mantine/core";
import Header from "./Header";
import cam1 from "../assets/cam1.jpg"; // Import the image
import { generateSlug } from "../generateSlug";
import '../App.css';
import Draggable, {DraggableEvent, DraggableData} from 'react-draggable';


interface BuildingsPageProps {
  buildings: Building[];
}

const VerticesDiv = () => {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleDrag = (e: DraggableEvent, data: DraggableData) => {
    setPosition({ x: data.x, y: data.y });
  };

  const handleStop = (e: DraggableEvent, data: DraggableData) => {
    setPosition({ x: data.x, y: data.y });
  };

  return (
    <div>
      {/* <p>Position: X-{position.x}, Y-{position.y}</p> */}
      {/* <div className='box'> */}
      <Draggable onDrag={handleDrag} onStop={handleStop} bounds="parent">
        <div className="ball" />
      </Draggable>
    </div>
  );
};

function BuildingsPage({ buildings }: BuildingsPageProps) {
  const { buildingSlug, camNum } = useParams<{
    buildingSlug: string;
    camNum: string;
  }>();

  const building = buildings.find((b) => generateSlug(b.name) === buildingSlug);
  const camera = building?.cameras.find((c) => c.cam_num === Number(camNum));

  // Reference to the BackgroundImage to get its dimensions
  const imageRef = useRef<HTMLDivElement>(null);

  // State to store the image dimensions
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });

  // Example hardcoded vertices (in relative percentages)
  const vertices = [
    { x: 30, y: 10 }, // Top-left
    { x: 80, y: 5 }, // Top-right
    { x: 90, y: 100 }, // Bottom-right
    { x: 10, y: 90 }, // Bottom-left
  ];

  // Update the image dimensions when the component mounts
  useEffect(() => {
    if (imageRef.current) {
      const rect = imageRef.current.getBoundingClientRect();
      setImageSize({ width: rect.width, height: rect.height });
    }
  }, []);

  return (
    <div>
      <Header title={`Camera ${camNum} Feed`} home={false} />
      <Box
        maw="1000px"
        mx="auto"
        mt="lg"
        z="0"
        style={{
          position: "relative",
          aspectRatio: "16 / 9", // Maintain 16:9 aspect ratio for the image
          overflow: "hidden", // Prevent overflow of content outside the box
        }}
      >
        <BackgroundImage
          ref={imageRef}
          src={cam1}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover", // Ensure the image scales properly without being cut off
            borderRadius: "8px", // Optional: Rounded corners
          }}
        >
         
        </BackgroundImage>
      </Box>
      <Flex align="center" justify="center" mt="lg">
        <Stack h="500px" w="500px">
          {camera?.parking_spots.map((spot) => (
            <Button
              key={spot.id}
              // onClick={() =>
              //     navigate(`/building/${buildingSlug}/camera/${cameraNum}/spot/${spot.id}`)
              // }
            >
              Edit Vertices for Spot {spot.spot_num}
            </Button>
          ))}
        </Stack>
      </Flex>
    </div>
  );
}

export default BuildingsPage;
