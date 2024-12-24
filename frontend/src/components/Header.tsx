import { Button, Flex, Title } from '@mantine/core';
import { useNavigate } from 'react-router-dom';

interface HeaderProps {
    title: string;
    home?: boolean;
}

function Header({ title, home }: HeaderProps) {
    const navigate = useNavigate();

    const handleHomeRedirect = () => {
        navigate('/');
    };

    const handleBackRedirect = () => {
        navigate(-1); // Navigate to the previous page
    };

    return (
        <Flex justify="space-between" align="center" mb='lg' mt='sm' style={{ position: 'relative', width: '100%' }}>
            {/* Left-aligned Back Button */}
            {!home && (
                <Button
                    variant="light"
                    radius="md"
                    color="blue"
                    onClick={handleBackRedirect}
                    style={{ position: 'absolute', left: '0', marginLeft: '10px' }}
                >
                    Back
                </Button>
            )}

            {/* Left-aligned Home Button */}
            {!home && (
                <Button
                    variant="light"
                    radius="md"
                    color="blue"
                    onClick={handleHomeRedirect}
                    style={{ position: 'absolute', left: '90px' }}
                >
                    Home
                </Button>
            )}

            {/* Center-aligned Title */}
            <Title style={{ margin: '0 auto', textAlign: 'center' }}>
                {title}
            </Title>
        </Flex>
    );
}

export default Header;
