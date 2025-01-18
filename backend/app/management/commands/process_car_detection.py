

PATH = './media/uploads/camera_snapshot_20250116222007_vertex1_cam7.jpeg'


class Command(BaseCommand):
    help = "Detects where the cars are in the parking lot"

    def handle(self, *args, **kwargs):
        parking = ParkingManagement(model_path = MODEL)
        parking.runParkingDetection(PATH)
        # solutions.ParkingPtsSelection()