import { useNavigate } from 'react-router-dom';
import { Building } from '../types';
import { Button, Stack, Flex } from '@mantine/core'
import Header from './Header'

interface BuildingsPageProps {
    buildings: Building[];
}

function BuildingsPage({ buildings }: BuildingsPageProps) {
    const navigate = useNavigate();

    return (
        <div>
            <Header title="Buildings" home={true} />
            <Flex align='center' justify='center' mt='lg'>
                <Stack h='500px' w='500px'>
                    {buildings.map((building) => (
                        <Button
                            key={building.id}
                            onClick={() => navigate(`/building/${building.id}`)}
                        >
                            {building.name}
                        </Button>
                    ))}
                </Stack>
            </Flex>
        </div>
    );
};

export default BuildingsPage;
