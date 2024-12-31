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
import { createParkingSpot, deleteParkingSpot } from "../apiService.ts";
import SpotPolygon from "./SpotPolygon.tsx";

interface BuildingsPageProps {
  buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {

  const { buildingSlug, camNum } = useParams<{
    buildingSlug: string;
    camNum: string;
  }>();

  const building = (buildings.find((b) => generateSlug(b.name) === buildingSlug));
  const camera = (building?.cameras.find((c) => c.cam_num === Number(camNum)));
  const [spots, setSpots] = useState<ParkingSpot[]>(camera?.parking_spots || [])

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

  const deleteAllSpots = () => {
    for(const parking_spot of spots){
      deleteParkingSpot(parking_spot)
    }
    setSpots([])
  }

  const AddNewSpot = (camera: Camera) => {
    const spotNum = spots.length;

    const vertices: Vertex[] = [
      { x: Math.round(imageSize.width * 0.25), y: Math.round(imageSize.height * 0.25) },
      { x: Math.round(imageSize.width * 0.75), y: Math.round(imageSize.height * 0.25) },
      { x: Math.round(imageSize.width * 0.75), y: Math.round(imageSize.height * 0.75) },
      { x: Math.round(imageSize.width * 0.25), y: Math.round(imageSize.height * 0.75) },
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
        setSpots([...spots, createdSpot])
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
            position: 'relative',
            width: "100%",
            height: "100%",
            objectFit: "cover", // Ensure the image scales properly without being cut off
            borderRadius: "8px", // Optional: Rounded corners
          }}
        >
          {spots.length > 0 &&
            spots.map((spot) => (
              <SpotPolygon
                key={spot.id}
                parking_spot={spot}
              />
            ))}
        </BackgroundImage>
      </Box>
      <Flex align="center" justify="center" mt="lg">
        <Group gap="lg">
          <Button onClick={() => AddNewSpot(camera)}>Add Spot To Camera</Button>
          <Button onClick={deleteAllSpots}>Delete Spot From Camera</Button>
        </Group>
      </Flex>
    </div>
  );
}

export default BuildingsPage;
