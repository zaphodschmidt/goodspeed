import { AppShell, Flex, Group, Title, ActionIcon, useMantineColorScheme, ThemeIcon, Burger } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { IconHome, IconSun, IconMoon, IconCar } from '@tabler/icons-react'
import { useDisclosure } from '@mantine/hooks';

export default function CustomAppShell({ children }: { children: React.ReactNode }) {
    const navigate = useNavigate();
    const { colorScheme, toggleColorScheme } = useMantineColorScheme()
    const [opened, { toggle }] = useDisclosure();

    return (
        <AppShell
            header={{ height: 75 }}
            navbar={{
                width: 300,
                breakpoint: 'sm',
                collapsed: { mobile: !opened },
            }}
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
                        <Burger
                            opened={opened}
                            onClick={toggle}
                            hiddenFrom="sm"
                            size="sm"
                        />
                        <ThemeIcon variant='filled' size='xl' radius='50%'>
                            <IconCar />
                        </ThemeIcon>
                        <Title order={3} fs="italic" fw={700} >
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

            <AppShell.Navbar p="md">Navbar</AppShell.Navbar>

            <AppShell.Main>{children}</AppShell.Main>
        </AppShell>
    );
}