from django.db import models

class Course(models.Model):
    COURSE_CATEGORY_CHOICES = [
        ('Compulsory', 'Compulsory'),
        ('Elective', 'Elective'),
    ]
    SOURCE_CHOICES = [
        ('ACM', 'ACM'),
        ('UvA', 'UvA'),
    ]
    YEAR_CHOICES = [(i, str(i)) for i in range(1, 4)]
    
    course_id = models.AutoField(primary_key=True)
    course_number = models.IntegerField(blank=True, null=True)
    course_name = models.CharField(max_length=100)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, blank=True, null=True)
    lecturer = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    course_category = models.CharField(max_length=10, choices=COURSE_CATEGORY_CHOICES, blank=True, null=True)
    year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    period = models.CharField(max_length=20, blank=True, null=True)
    csv_file = models.FileField(upload_to='CSV/', blank=True, null=True)
    
    class Objective(models.Model):
        objective_id = models.IntegerField(default=0)
        course = models.ForeignKey('Course', related_name='objectives', on_delete=models.CASCADE)
        content = models.TextField()
        level = models.CharField(max_length=20)
        
        def __str__(self):
            return self.content

    def __str__(self):
        return self.course_name



class Trajectory(models.Model):
    TRAJECTORY_CHOICES = [
        ('Software Systems', 'Software Systems'),
        ('Modelbased Systems', 'Modelbased Systems'),
        ('Mathematics and Computer Science Theory', 'Mathematics and Computer Science Theory'),
        ('Data and Information Systems', 'Data and Information Systems'),
        ('Computer Systems', 'Computer Systems'),
        ('Academic Competences', 'Academic Competences'),
    ]
    trajectory_id = models.AutoField(primary_key=True)
    trajectory_name = models.CharField(max_length=100, choices=TRAJECTORY_CHOICES)
    objective_number = models.CharField(max_length=100, blank=True)
    objective = models.TextField()
    level = models.CharField(max_length=20, blank=True)
    related_course_objectives = models.ManyToManyField(Course.Objective, blank=True)

    def __str__(self):
        return self.trajectory_name
