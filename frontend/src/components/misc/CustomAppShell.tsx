import { AppShell, Flex, Group, Title, ActionIcon, useMantineColorScheme, ThemeIcon, Burger, NavLink, ScrollArea } from '@mantine/core';
import { useNavigate, useLocation } from 'react-router-dom';
import { IconHome, IconSun, IconMoon, IconCar } from '@tabler/icons-react'
import { useDisclosure } from '@mantine/hooks';
import { useBuildings } from './useBuildingsContext';
import { generateSlug } from './generateSlug';

export default function CustomAppShell({ children }: { children: React.ReactNode }) {
    const navigate = useNavigate();
    const location = useLocation();
    const { colorScheme, toggleColorScheme } = useMantineColorScheme()
    const [opened, { toggle }] = useDisclosure();
    const { buildings } = useBuildings()

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

            <AppShell.Navbar p="md">
                <ScrollArea>
                    <NavLink
                        href="#required-for-focus"
                        label="Welcome"
                        active={location.pathname === '/'}
                        onClick={() => navigate(`/`)}
                    />

                    {buildings.map((building) => {
                        const slug = generateSlug(building.name)
                        const cameras = building.cameras
                        return (
                            <>
                                <NavLink
                                    href="#required-for-focus"
                                    label={building.name}
                                    childrenOffset={28}
                                >
                                    <NavLink
                                        variant='subtle'
                                        label='Overview'
                                        active={location.pathname === `/building/${slug}`}
                                        onClick={() => navigate(`/building/${slug}`)}
                                    />
                                    <NavLink
                                        href="#required-for-focus"
                                        label='Cameras'
                                        childrenOffset={28}
                                    >
                                        {cameras.map((camera) =>
                                            <NavLink
                                                variant='subtle'
                                                active={location.pathname === `/building/${slug}/camera/${camera.cam_num}`}
                                                label={`Camera #${camera.cam_num}`}
                                                onClick={() => navigate(`/building/${slug}/camera/${camera.cam_num}`)}
                                            />)}
                                    </NavLink>
                                </NavLink>

                            </>
                        )
                    })}
                </ScrollArea>
            </AppShell.Navbar>

            <AppShell.Main>{children}</AppShell.Main>
        </AppShell>
    );
}