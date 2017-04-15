from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

class YearQuerySet(models.QuerySet):
    def get_current(self):
        now = timezone.now()
        try:
            return self.get(start_date__lte=now, end_date__gte=now)
        except ObjectDoesNotExist:
            return self.order_by('end_date').last()
