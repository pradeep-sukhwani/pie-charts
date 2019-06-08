import random
import string
from django.core.management.base import BaseCommand
from core.models import IdMapping, Report


class Command(BaseCommand):
    help = "Fixtures for Table: IdMapping, Report, Login data"
    message = "Done"

    def handle(self, *args, **options):
        char_set = string.ascii_uppercase + string.digits
        pass_fail_choice = [True, False]
        grade_choice = ['A', 'A+', 'B', 'B+', 'C']
        for i in range(0, 10):
            id_mapping = IdMapping.objects.create(name="".join(random.sample(char_set * 6, 6)))
            Report.objects.create(
                students=id_mapping,
                std=i + 1,
                year=2017 + i,
                sci=16.5 * i,
                math=16.5 * i,
                language=16.5 * i,
                social=16.5 * i,
                total=16.5 * i * 4,
                grade=random.choice(grade_choice),
                pass_fail=random.choice(pass_fail_choice)
            )
        return self.message
