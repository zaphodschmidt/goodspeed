import { useMemo } from "react";
import { ParkingSpot } from "../../types";
import {
  MantineReactTable,
  MRT_ColumnDef,
  useMantineReactTable,
} from "mantine-react-table";
import { IconCheck, IconX } from "@tabler/icons-react";
import { Group, Text } from "@mantine/core";
import dayjs from "dayjs";
// import hashSpotColor from "./hashSpotColor";

interface SpotTableProps {
  spots: ParkingSpot[];
  detailed?: boolean;
}

const sortDateTime = (a: string, b: string): number => {
  const dateA = new Date(a).getTime(); // Convert to timestamp
  const dateB = new Date(b).getTime();

  return dateA - dateB; // Ascending order
};

export default function SpotTable({ spots, detailed }: SpotTableProps) {
  const columns = useMemo<MRT_ColumnDef<ParkingSpot>[]>(
    () => [
      {
        accessorKey: "spot_num",
        header: "Spot #",
        Cell: ({ cell }) => {
          // const color = hashSpotColor(row.index)
          return (
            <Group>
              <Text size="sm">{cell.getValue<string>()}</Text>
              {/* {!detailed &&
                                <Tooltip label='Spot color' openDelay={500}>
                                    <div
                                        className="ball"
                                        style={{
                                            backgroundColor: color,
                                            width: `7px`,
                                            height: `7px`,
                                            cursor: 'default'
                                        }}
                                    />
                                </Tooltip>
                            } */}
            </Group>
          );
        },
      },
      {
        accessorKey: "cam_num",
        id: "cam_num",
        header: "Camera #",
      },
      {
        accessorKey: "occupied",
        header: "Occupied?",
        Cell: ({ cell }) => {
          return cell.getValue<boolean>() ? (
            <IconCheck color="green" />
          ) : (
            <IconX color="red" />
          );
        },
      },
      {
        accessorKey: "occupied_by_lpn",
        header: "Occupied by (LPN)",
        enableSorting: false,
      },
      {
        accessorKey: "reserved_by_lpn",
        header: "Reserved by (LPN)",
        enableSorting: false,
      },
      {
        accessorKey: "start_datetime",
        header: "Reservation Starts",
        Cell: ({ cell }) => {
          const datetime = cell.getValue<string>();
          if (datetime)
            return (
              <Text size="sm">
                {dayjs(datetime).format("MM/DD/YYYY HH:mm")}
              </Text>
            );
          return <></>;
        },
        sortingFn: (rowA, rowB) => {
          const a = rowA.getValue<string>("end_datetime");
          const b = rowB.getValue<string>("end_datetime");
          return sortDateTime(a, b);
        },
      },
      {
        accessorKey: "end_datetime",
        header: "Reservation Ends",
        Cell: ({ cell }) => {
          const datetime = cell.getValue<string>();
          if (datetime)
            return (
              <Text size="sm">
                {dayjs(datetime).format("MM/DD/YYYY HH:mm")}
              </Text>
            );
          return <></>;
        },
        sortingFn: (rowA, rowB) => {
          const a = rowA.getValue<string>("end_datetime");
          const b = rowB.getValue<string>("end_datetime");
          return sortDateTime(a, b);
        },
      },
    ],
    []
  );

  const table = useMantineReactTable({
    columns,
    data: spots,
    enableSorting: detailed ?? false,
    enableColumnActions: false,
    initialState: {
      density: "xs",
      // pagination: { pageSize: 50, pageIndex: 0 },
      columnVisibility: { cam_num: detailed ?? false },
    },
    enableTopToolbar: false,
    enableBottomToolbar: false,
    // mantinePaginationProps: {
    //     showRowsPerPage: false,
    //     withEdges: false, // Customizes pagination controls
    // },
    enablePagination: false,
    mantinePaperProps: {
      style: {
        border: "0px",
        boxShadow: "none",
      },
    },
  });

  return <MantineReactTable table={table} />;
}
