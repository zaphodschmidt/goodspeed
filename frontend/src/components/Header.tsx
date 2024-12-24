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

    return (
        <Flex justify="space-between" align="center" style={{ position: 'relative', width: '100%' }}>
            {/* Left-aligned Home Button */}
            {!home && (
                <Button
                    variant="light"
                    radius="md"
                    color="blue"
                    onClick={handleHomeRedirect}
                    style={{ position: 'absolute', left: 0 }}
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
