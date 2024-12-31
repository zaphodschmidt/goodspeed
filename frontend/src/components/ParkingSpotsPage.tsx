import React, { useRef, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Building, Camera, ParkingSpot, Vertex } from "../types";
import {
  Button,
  Flex,
  Box,
  BackgroundImage,
  Group,
} from "@mantine/core";
import Header from "./Header";
import cam1 from "../assets/cam1.jpg"; // Import the image
import { generateSlug } from "../generateSlug";
import "../App.css";
import { createParkingSpot } from "../apiService.ts";
import DraggableVertex from "./DraggableVertex.tsx";

interface BuildingsPageProps {
  buildings: Building[];
}

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

  // Update the image dimensions when the component mounts
  useEffect(() => {
    if (imageRef.current) {
      const rect = imageRef.current.getBoundingClientRect();
      setImageSize({ width: rect.width, height: rect.height });
    }
  }, []);

  const AddNewSpot = (camera: Camera) => {
    const spotNum = camera.parking_spots.length - 1;
    const middleX = 0;
    const middleY = 0;
    const offset = 40;

    const vertices: Vertex[] = [
      { x: middleX - offset, y: middleY - offset },
      { x: middleX - offset, y: middleY + offset },
      { x: middleX + offset, y: middleY - offset },
      { x: middleX + offset, y: middleY + offset }
    ];

    const newSpot: ParkingSpot = {
      camera: camera.id!,
      spot_num: spotNum,
      vertices,
    };
    console.log("newSpot:", newSpot)
    createParkingSpot(newSpot)
      .then((createdSpot) => {
        console.log("Parking spot created", createdSpot);
      })
      .catch((error) => {
        console.error("Error in creating parking spot", error);
      });
  }

  return (
    <div>
      <Header title={`Camera ${camNum} Feed`} home={false} />
      <Box
        maw="1000px"
        mx="auto"
        mt="lg"
        style={{
          // background: "black",
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
          {camera && camera.parking_spots && camera!.parking_spots.length > 0 &&
            camera!.parking_spots[1].vertices.map((vertex) => (
              <DraggableVertex
                key={vertex.id}
                vertex={vertex}
              />
            ))}
        </BackgroundImage>
      </Box>
      <Flex align="center" justify="center" mt="lg">
        <Group gap="lg">
          <Button onClick={() => AddNewSpot(camera)}>Add Spot To Camera</Button>
          <Button>Delete Spot From Camera</Button>
        </Group>
      </Flex>
    </div>
  );
}

export default BuildingsPage;
