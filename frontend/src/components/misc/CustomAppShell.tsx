import { AppShell, Flex, Group, Title, ActionIcon, useMantineColorScheme, ThemeIcon } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { IconHome, IconSun, IconMoon, IconCar } from '@tabler/icons-react'

export default function CustomAppShell({ children }: { children: React.ReactNode }) {
    const navigate = useNavigate();
    const { colorScheme, toggleColorScheme } = useMantineColorScheme()

    return (
        <AppShell
            header={{ height: 75 }}
            padding="md"
        >
            <AppShell.Header>
                <Group justify='space-between'>
                    <Flex 
                        align='center' p='md' 
                        gap='md' 
                        onClick={() => navigate('/')} // Add navigation on click
                        style={{ cursor: 'pointer' }} 
                    >
                        <ThemeIcon variant='filled' size='xl' radius='50%'>
                            <IconCar />
                        </ThemeIcon>
                        <Title order={1} fs="italic" fw={1000} >
                            Goodspeed.info
                        </Title>
                    </Flex>
                    <Flex align='center' p='md' justify='flex-end' gap='md' onClick={() => navigate('/')}>
                        <ActionIcon size='xl' variant='light' >
                            <IconHome />
                        </ActionIcon>
                        <ActionIcon size='xl' variant='light' onClick={toggleColorScheme}>
                            {colorScheme === 'dark' ? <IconSun /> : <IconMoon />}
                        </ActionIcon>
                    </Flex>

                </Group>
            </AppShell.Header>

            <AppShell.Main>{children}</AppShell.Main>
        </AppShell>
    );
}