from django.db import migrations

def add_initial_rooms(apps, schema_editor):
    Room = apps.get_model('reservations', 'Room')
    rooms = [
        {'unit': '101', 'type': 'studio', 'floor': 1, 'price': 4000},
        {'unit': '102', 'type': 'studio', 'floor': 1, 'price': 4000},
        {'unit': '103', 'type': '1-bed', 'floor': 1, 'price': 6000},
        {'unit': '104', 'type': '2-bed', 'floor': 1, 'price': 8000},
        {'unit': '201', 'type': 'studio', 'floor': 2, 'price': 4000},
        {'unit': '202', 'type': 'studio', 'floor': 2, 'price': 4000},
        {'unit': '203', 'type': '1-bed', 'floor': 2, 'price': 6000},
        {'unit': '204', 'type': '2-bed', 'floor': 2, 'price': 8000},
        {'unit': '301', 'type': 'studio', 'floor': 3, 'price': 4400},
        {'unit': '302', 'type': 'studio', 'floor': 3, 'price': 4400},
        {'unit': '303', 'type': '1-bed', 'floor': 3, 'price': 6400},
        {'unit': '304', 'type': '2-bed', 'floor': 3, 'price': 8400},
        {'unit': '401', 'type': 'studio', 'floor': 4, 'price': 4700},
        {'unit': '402', 'type': 'studio', 'floor': 4, 'price': 4700},
        {'unit': '403', 'type': '1-bed', 'floor': 4, 'price': 6700},
        {'unit': '404', 'type': '2-bed', 'floor': 4, 'price': 8700},
        {'unit': '501', 'type': 'studio', 'floor': 5, 'price': 5000},
        {'unit': '502', 'type': 'studio', 'floor': 5, 'price': 5000},
        {'unit': '503', 'type': '1-bed', 'floor': 5, 'price': 7000},
        {'unit': '504', 'type': '2-bed', 'floor': 5, 'price': 9000},
    ]
    for room in rooms:
        Room.objects.create(**room)

class Migration(migrations.Migration):
    dependencies = [
        ('reservations', '0001_initial'),  # Adjust to your initial migration
    ]

    operations = [
        migrations.RunPython(add_initial_rooms),
    ]
