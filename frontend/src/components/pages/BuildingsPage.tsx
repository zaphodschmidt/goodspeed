import { useNavigate } from 'react-router-dom';
import { Building } from '../../types';
import { Button, Stack, Center } from '@mantine/core';
import Header from '../misc/Header';
import { generateSlug } from '../misc/generateSlug';

interface BuildingsPageProps {
    buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {
    const navigate = useNavigate();

    return (
        <div>
            <Header title="Buildings" home={true} />
            <Center>
                <Stack h="500px" w="500px">
                    {buildings.map((building) => {
                        const slug = generateSlug(building.name);
                        return (
                            <Button
                                key={building.id}
                                onClick={() => navigate(`/building/${slug}`)}
                            >
                                {building.name}
                            </Button>
                        );
                    })}
                </Stack>
            </Center>
        </div>
    );
}

export default BuildingsPage;
