from django.contrib import admin

from voting.models import Position, SACYear

from voting.forms import PositionForm

# Register your models here.

admin.site.register(SACYear)

admin.site.register(Position)


