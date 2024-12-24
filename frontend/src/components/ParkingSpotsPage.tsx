import React, { useRef, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Building } from '../types';
import { Button, Stack, Flex, Box, BackgroundImage} from '@mantine/core';
import Header from './Header';
import cam1 from '../assets/cam1.jpg'; // Import the image
import { generateSlug } from '../generateSlug';

interface BuildingsPageProps {
    buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {
    const { buildingSlug, camNum } = useParams<{ buildingSlug: string; camNum: string }>();

    const building = buildings.find((b) => generateSlug(b.name) === buildingSlug);
    const camera = building?.cameras.find((c) => c.cam_num === Number(camNum));

    // Reference to the BackgroundImage to get its dimensions
    const imageRef = useRef<HTMLDivElement>(null);

    // State to store the image dimensions
    const [imageSize, setImageSize] = useState({ width: 0, height: 0 });

    // Example hardcoded vertices (in relative percentages)
    const vertices = [
        { x: 5, y: 10 }, // Top-left
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

            {/* Background Image with Polygon Overlay */}
            <Box
                maw="1000px"
                mx="auto"
                mt="lg"
                style={{
                    position: 'relative',
                    aspectRatio: '16 / 9', // Maintain 16:9 aspect ratio for the image
                    overflow: 'hidden', // Prevent overflow of content outside the box
                }}
            >
                <BackgroundImage
                    ref={imageRef}
                    src={cam1}
                    style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover', // Ensure the image scales properly without being cut off
                        borderRadius: '8px', // Optional: Rounded corners
                    }}
                >
                    {/* SVG Polygon Overlay */}
                    <svg
                        width={imageSize.width}
                        height={imageSize.height}
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            pointerEvents: 'none', // Allow clicks to pass through the polygon
                        }}
                    >
                        <polygon
                            points={vertices
                                .map(
                                    (v) =>
                                        `${(v.x / 100) * imageSize.width},${(v.y / 100) * imageSize.height}`
                                )
                                .join(' ')}
                            style={{
                                fill: 'rgba(255, 0, 0, 0.5)', // Semi-transparent red
                                stroke: 'black', // Optional border
                                strokeWidth: 2,
                            }}
                        />
                    </svg>
                </BackgroundImage>


            </Box>

            {/* Parking Spot Buttons */}
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
