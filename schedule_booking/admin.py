from django.contrib import admin

from .models import Place, Schedule, Appointment, Student, Config


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    filter_horizontal = ("students",)


class StudentAdmin(admin.ModelAdmin):
    list_display = ("lastname", "firstname", "email", "school")


admin.site.register(Student, StudentAdmin)
admin.site.register(Schedule)
admin.site.register(Place)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Config)
