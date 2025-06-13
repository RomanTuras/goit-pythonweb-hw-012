from src.database.models import Contact
from datetime import datetime

contacts = [
    Contact(
        first_name="Luke",
        last_name="Skywalker",
        email="luke@test.com",
        phone="0991234567",
        birth_date=datetime(year=1999, month=3, day=15),
        additional="Jedi Knight",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Darth",
        last_name="Vader",
        email="vader@test.com",
        phone="0997654321",
        birth_date=datetime(year=1977, month=5, day=25),
        additional="Sith Lord",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Leia",
        last_name="Organa",
        email="leia@test.com",
        phone="0991112233",
        birth_date=datetime(year=1999, month=3, day=15),
        additional="Princess of Alderaan",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Han",
        last_name="Solo",
        email="han@test.com",
        phone="0996543210",
        birth_date=datetime(year=1977, month=7, day=11),
        additional="Smuggler",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Chewbacca",
        last_name="Wookiee",
        email="chewie@test.com",
        phone="0992233445",
        birth_date=datetime(year=1977, month=3, day=20),
        additional="Wookiee Warrior",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Yoda",
        last_name="Master",
        email="yoda@test.com",
        phone="0995566778",
        birth_date=datetime(year=900, month=5, day=3),
        additional="Jedi Master",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Obi-Wan",
        last_name="Kenobi",
        email="obiwan@test.com",
        phone="0993344556",
        birth_date=datetime(year=1999, month=3, day=15),
        additional="Jedi Knight",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="Boba",
        last_name="Fett",
        email="boba@test.com",
        phone="0996677889",
        birth_date=datetime(year=1977, month=2, day=14),
        additional="Bounty Hunter",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="R2-D2",
        last_name="Droid",
        email="r2d2@test.com",
        phone="0999988776",
        birth_date=datetime(year=1977, month=3, day=5),
        additional="Astromech Droid",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    Contact(
        first_name="C-3PO",
        last_name="Droid",
        email="c3po@test.com",
        phone="0998877665",
        birth_date=datetime(year=1977, month=4, day=15),
        additional="Protocol Droid",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
