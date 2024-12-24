import { useNavigate, useParams } from 'react-router-dom';
import { Building } from '../types';
import { Button, Stack, Flex } from '@mantine/core'
import Header from './Header'
import { generateSlug } from '../generateSlug';

interface BuildingsPageProps {
    buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {
    const { buildingSlug } = useParams<{ buildingSlug: string }>();
    const navigate = useNavigate();
    console.log(buildings[0]?.name.toLowerCase().replace(/ /g,''))
    const building = buildings.find((b) => generateSlug(b.name) === buildingSlug);

    return (
        <div>
             <Header title={`Cameras for ${building?.name}`} home={false} />
            <Flex align='center' justify='center'>
                <Stack h='500px' w='500px'>
                    {building?.cameras.map((camera) => (
                        <Button
                            key={camera.id}
                            onClick={() => navigate(`/building/${buildingSlug}/camera/${camera.cam_num}`)}
                        >
                            Camera {camera.cam_num}
                        </Button>
                    ))}
                </Stack>
            </Flex>
        </div>
    );
};

export default BuildingsPage;
