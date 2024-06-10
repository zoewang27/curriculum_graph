from django import forms
from .models import Course, Trajectory
from collections import defaultdict
from django.db.models import Prefetch
from collections import defaultdict

class CourseObjectiveChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_counters = defaultdict(int)  # Initialize a counter for each course
    
    def label_from_instance(self, obj):
        course_id = obj.course_id
        self.course_counters[course_id] += 1
        return f" [{obj.course.course_name}]: {self.course_counters[course_id]}. {obj.content}"


class TrajectoryForm(forms.ModelForm):
    related_course_objectives = CourseObjectiveChoiceField(
        queryset=Course.Objective.objects.all(),
        required=False,
        widget=forms.SelectMultiple
    )

    class Meta:
        model = Trajectory
        fields = ['trajectory_name', 'objective_number', 'objective',  'level', 'related_course_objectives']
