from django.contrib import admin

from voting.models import Position, SACYear

# Register your models here.

admin.site.register(SACYear)

admin.site.register(Position)


