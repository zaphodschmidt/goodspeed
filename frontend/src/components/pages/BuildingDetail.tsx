import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Building, Camera, ParkingSpot } from '../../types';
import { Stack, Pagination, Grid, AspectRatio, Image, Text, Group, Tabs, Title } from '@mantine/core'
import { generateSlug } from '../misc/generateSlug';
import no_image from "../../assets/no_image.jpeg";
import SpotTable from '../spotComponents/SpotTable';
import { useBuildings } from '../misc/useBuildingsContext';
import CustomLoader from '../misc/CustomLoader';

function BuildingDetail() {
    const { buildings } = useBuildings()
    const { buildingSlug } = useParams<{ buildingSlug: string }>();
    const navigate = useNavigate();
    const building: Building | undefined = buildings.find((b) => generateSlug(b.name) === buildingSlug);
    const cameras: Camera[] = building?.cameras.sort((a, b) => a.cam_num - b.cam_num) || []

    const [activePage, setPage] = useState(1);

    const camsPerPage = 15
    const numPages = Math.ceil(cameras.length / camsPerPage)
    const displayedCameras: Camera[] = cameras.slice((activePage - 1) * 15, (activePage * 15))
    const [activeTab, setActiveTab] = useState<string | null>('cameras');

    const spots: ParkingSpot[] = cameras?.flatMap((camera) =>
        camera.parking_spots.map((spot) =>
            ({ ...spot, cam_num: camera.cam_num })
        )
    ).sort((a, b) => a.spot_num - b.spot_num) || [];

    useEffect(() => {
        setPage(1)
        setActiveTab('cameras')
    }, [building])

    if (!building) return <CustomLoader />

    return (
        <Stack mt='lg' mb='lg'>
            <Title ta='center'>{building.name}</Title>
            <Tabs value={activeTab} onChange={setActiveTab}>
                <Tabs.List>
                    <Tabs.Tab value="cameras">Cameras</Tabs.Tab>
                    <Tabs.Tab value="spots">Parking Spots</Tabs.Tab>
                </Tabs.List>
                <Tabs.Panel value="cameras">
                    <Stack align="center">
                        <Grid columns={5} align='center' justify="flex-start" p='md'>
                            {displayedCameras.map((camera) => (
                                <Grid.Col span={1} key={camera.id} >
                                    <AspectRatio
                                        w='1000px'
                                        ratio={4 / 3}
                                    >
                                        <div
                                            style={{ cursor: 'pointer' }}
                                            onClick={() => navigate(`/building/${buildingSlug}/camera/${camera.cam_num}`)}
                                        >
                                            <Image
                                                src={camera.image?.image_url || no_image}
                                                onError={(event) => {
                                                    event.currentTarget.src = no_image; // Set fallback image if the original URL is invalid
                                                }}
                                                radius='md'
                                            />
                                        <Group justify='space-between'>
                                            <Text fz='xl'>{camera.cam_num}</Text>
                                            <Text ta='right' c='gray'>{camera.MAC}</Text>
                                        </Group>

                                    </div>
                                </AspectRatio>
                                </Grid.Col>
                            ))}
                    </Grid>
                    <Pagination value={activePage} onChange={setPage} total={numPages} />
                </Stack>
            </Tabs.Panel>
            <Tabs.Panel value="spots">
                <SpotTable spots={spots} detailed />
            </Tabs.Panel>
        </Tabs>
        </Stack >
    );
};

export default BuildingDetail;
