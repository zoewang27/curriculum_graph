from django.urls import path

from . import views


urlpatterns = [
    path("graph", views.graph,name="graph"),
    path("contentmgmt", views.contentmgmt),

    path("similarity", views.SimilarityPage, name="similarity"),
    path("detect/", views.detectSimilarCourse, name="similarity-detect"),

    path("allcourses/", views.allCourses, name="allcourses"),
    path("detectAllcourses/", views.detectAllcourses, name="all-courses-similarity"),

]