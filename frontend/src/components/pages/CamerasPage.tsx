import { useNavigate, useParams } from 'react-router-dom';
import { Building } from '../../types';
import { Button, Grid, AspectRatio, Image } from '@mantine/core'
import Header from '../misc/Header'
import { generateSlug } from '../misc/generateSlug';
import no_image from "../../assets/no_image.jpeg";

interface BuildingsPageProps {
    buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {
    const { buildingSlug } = useParams<{ buildingSlug: string }>();
    const navigate = useNavigate();
    console.log(buildings[0]?.name.toLowerCase().replace(/ /g, ''))
    const building = buildings.find((b) => generateSlug(b.name) === buildingSlug);
    const cameras = building?.cameras.sort((a, b) => a.cam_num - b.cam_num) || []

    return (
        <div>
            <Header title={`Cameras for ${building?.name}`} home={false} />
            <Grid columns={10} align='center' justify="flex-start" p='md'>
                {cameras.map((camera) => (
                    <Grid.Col span={2} key={camera.id} >
                        <AspectRatio
                            maw={1000}
                            mx="auto"
                            ratio={4 / 3}
                        >
                            <div
                                style={{ cursor: 'pointer' }}
                                onClick={() => navigate(`/building/${buildingSlug}/camera/${camera.cam_num}`)}
                            >
                                <Image src={camera.image?.image_url || no_image} />
                            </div>
                        </AspectRatio>
                    </Grid.Col>
                ))}
            </Grid>
        </div>
    );
};

export default BuildingsPage;
