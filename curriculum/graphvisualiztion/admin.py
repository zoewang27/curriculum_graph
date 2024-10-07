from django.contrib import admin
from .models import Course, Trajectory
from .forms import TrajectoryForm

class ObjectiveInline(admin.TabularInline):
    model = Course.Objective
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id','course_number', 'course_name','source', 'year', 'period', 'csv_file')
    list_display_links = ('course_number', 'course_name', 'year', 'period')
    inlines = (ObjectiveInline,)
    ordering = ('source','course_number')

class TrajectoryAdmin(admin.ModelAdmin):
    list_display = ('trajectory_name','objective_number', 'objective', 'level')
    list_display_links = ('trajectory_name','objective_number', 'objective', 'level')
    form = TrajectoryForm
    filter_horizontal = ('related_course_objectives',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Trajectory, TrajectoryAdmin)