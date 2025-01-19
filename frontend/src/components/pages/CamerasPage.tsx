import { useNavigate, useParams } from 'react-router-dom';
import { useState } from 'react';
import { Building, Camera, ParkingSpot } from '../../types';
import { Stack, Pagination, Grid, AspectRatio, Image, Text, Group, Tabs, Center, Loader } from '@mantine/core'
import Header from '../misc/Header'
import { generateSlug } from '../misc/generateSlug';
import no_image from "../../assets/no_image.jpeg";
import SpotTable from '../spotComponents/SpotTable';

interface BuildingsPageProps {
    buildings: Building[];
}

function CamerasPage({ buildings }: BuildingsPageProps) {
    const { buildingSlug } = useParams<{ buildingSlug: string }>();
    const navigate = useNavigate();
    const building: Building | undefined = buildings.find((b) => generateSlug(b.name) === buildingSlug);
    const cameras: Camera[] = building?.cameras.sort((a, b) => a.cam_num - b.cam_num) || []

    const [activePage, setPage] = useState(1);

    const camsPerPage = 15
    const numPages = Math.ceil(cameras.length / camsPerPage)
    const displayedCameras: Camera[] = cameras.slice((activePage - 1) * 15, (activePage * 15))

    const spots: ParkingSpot[] = cameras?.flatMap((camera) => camera.parking_spots.map((spot) => ({...spot, cam_num: camera.cam_num })))

    const [activeTab, setActiveTab] = useState<string | null>('cameras');

    if(!cameras || !spots){
        return(<Center><Loader/></Center>)
    }

    return (
        <div>
            <Header title={`Overview for ${building?.name}`} home={false} />
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
                                        maw={1000}
                                        mx="auto"
                                        ratio={4 / 3}
                                    >
                                        <div
                                            style={{ cursor: 'pointer' }}
                                            onClick={() => navigate(`/building/${buildingSlug}/camera/${camera.cam_num}`)}
                                        >
                                            <Image src={camera.image?.image_url || no_image} >
                                            </Image>
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
                    <SpotTable spots={spots} detailed/>
                </Tabs.Panel>
            </Tabs>
        </div>
    );
};

export default CamerasPage;
