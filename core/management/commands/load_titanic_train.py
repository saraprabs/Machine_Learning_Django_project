import csv
from django.core.management.base import BaseCommand
from core.models import Passenger
from django.utils import timezone

class Command(BaseCommand):
    help = 'Imports cleaned Titanic data from a CSV into the Passenger model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('--type', type=str, choices=['train', 'test'], default='train')

    def handle(self, *args, **options):
        file_path = options['file_path']
        data_type = options['type']
        count = 0
        try:
            with open(options['file_path'], 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # The .save() method in your model will automatically calculate 
                    # family_size and age_group based on the fields below
                    Passenger.objects.create(
                        passenger_id=int(row['PassengerId']),
                        survived=bool(int(row['Survived'])),
                        pclass=int(row['Pclass']),
                        name=row['Name'],
                        sex=row['Sex'].lower(), # Matches choices ['male', 'female']
                        age=int(row['Age']) if row['Age'] and row['Age'] != '' else None,
                        sibsp=int(row['SibSp']) if row['SibSp'] else 0,
                        parch=int(row['Parch']) if row['Parch'] else 0,
                        ticket=row['Ticket'],
                        fare=float(row['Fare']) if row['Fare'] and row['Fare'] != '' else 0.0,
                        cabin=row.get('Cabin', ''),
                        embarked=row['Embarked'].upper() if row['Embarked'] else '',
                        data_source='train', # Defaulting to training data
                        imported_at=timezone.now()
                    )
                    count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} passengers.'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found at: {options['file_path']}"))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"CSV is missing required column: {e}"))