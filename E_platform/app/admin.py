from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomeUser)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(StudentAssignment)
admin.site.register(Quiz)
