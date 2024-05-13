from django.urls import path

from . import views


urlpatterns = [
    path("graph", views.graph,name="graph"),
    path("contentmgmt", views.contentmgmt),

    # single course graph
    path("singlecourse", views.singleCourse, name="singlecourse"),
    path("showCourseGraph/", views.showCourseGraph, name="show-course-graph"),

    # Two courses semantic similarity
    path("similarity", views.SimilarityPage, name="similarity"),
    path("detect/", views.detectSimilarCourse, name="similarity-detect"),

    # All courses semantic similarity
    path("allcourses/", views.allCourses, name="allcourses"),
    path("detectAllcourses/", views.detectAllcourses, name="all-courses-similarity"),

    # upload and delete csv files
    path("filesManagement/", views.filesManagement, name="filesManagement"),
    path("uploadfiles/", views.uploadfile, name="upload-file"),
    path("deletefiles/", views.deletefile, name="delete-file"),

]