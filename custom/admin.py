from django.contrib import admin
from .models import Municipality,AdministrativePost,Village,Aldeia,AcademicLevel,Religion,Profession

# Register your models here.
admin.site.register(Municipality)
admin.site.register(AdministrativePost)
admin.site.register(Village)
admin.site.register(Aldeia)
admin.site.register(AcademicLevel)
admin.site.register(Religion)
admin.site.register(Profession)

