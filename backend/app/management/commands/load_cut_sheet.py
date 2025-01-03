from django.core.management.base import BaseCommand
from app.models import Building, Camera
import os
import csv
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates building/cameras in database by reading from CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='The path to the CSV file to import',
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if not os.path.exists(file_path):
            raise CommandError(f"The file '{file_path}' does not exist.")
        
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                subnet = ''
                building = None
                
                for row in reader:
                    if 'building' in row[0].lower():
                        #extract building name
                        building_name = row[1].strip()
                        
                        #Delete existing building if one exists with the same name 
                        existing_building = Building.objects.filter(name=building_name).first()
                        if(existing_building):
                            existing_building.delete()

                        #Create new building
                        building = Building.objects.create(
                            name=building_name
                        )

                    elif 'subnet' in row[0].lower():
                        subnet = row[1].strip() #extract subnet
                        while(subnet[-1]!='.'):
                            subnet = subnet[:-1]
                    
                    elif 'camera num' in row[0].lower():
                        pass

                    elif(row[0] and row[1]):
                        cam_num = row[0]
                        MAC = row[1]
                        IP = subnet+cam_num
                        print(cam_num, MAC, IP, subnet)
                        Camera.objects.create(
                            cam_num=cam_num,
                            building=building,
                            MAC=MAC,
                            IP=IP,
                        )

                        
        except Exception as e:
            raise CommandError(f"An error occurred while processing the file: {e}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully imported data from '{file_path}'"))
