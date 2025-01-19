import { useMemo } from "react";
import { ParkingSpot } from "../../types"
import { MantineReactTable, MRT_ColumnDef, useMantineReactTable } from 'mantine-react-table';
import { IconCheck, IconX } from "@tabler/icons-react";
import { Text } from '@mantine/core'
import dayjs from 'dayjs'

interface SpotTableProps{
    spots: ParkingSpot[];
    // onSpotEdit: (spot: ParkingSpot) => void
}

export default function SpotTable({ spots } : SpotTableProps){

    const columns = useMemo<MRT_ColumnDef<ParkingSpot>[]>(
        () => [
            {
                accessorKey: 'spot_num',
                header: 'Spot #'
            },
            {
                accessorKey: 'occupied',
                header: 'Occupied?',
                Cell: ({ cell }) => {
                    return cell.getValue<boolean>() ? (<IconCheck color='green'/>) : (<IconX  color='red'/>)
                }
            },
            {
                accessorKey: 'occupied_by_lpn',
                header: 'Occupied by (LPN)',
            },
            {
                accessorKey: 'reserved_by_lpn',
                header: 'Reserved by (LPN)',
            },
            {
                accessorKey: 'start_datetime',
                header: 'Reservation Starts',
                Cell: ({ cell }) => {
                    const datetime = cell.getValue<string>()
                    if(datetime)
                        return <Text size='sm'>{dayjs(datetime).format('MM/DD/YYYY HH:mm')}</Text>
                    return <></>
                }
            },
            {
                accessorKey: 'end_datetime',
                header: 'Reservation Ends',
                Cell: ({ cell }) => {
                    const datetime = cell.getValue<string>()
                    if(datetime)
                        return <Text size='sm'>{dayjs(datetime).format('MM/DD/YYYY HH:mm')}</Text>
                    return <></>
                }
            },
        ],
        [],
    );

    const table = useMantineReactTable({
        columns,
        data: spots,
        enableSorting: false,
        enableColumnActions: false,
        initialState: {
            density: 'xs',
        },
        enableTopToolbar: false,
        enableBottomToolbar: false,
    })

    return(<MantineReactTable table={table}/>)

}