from django.urls import path

from . import views


urlpatterns = [
    # path("graph", views.graph,name="graph"),
    # path("contentmgmt", views.contentmgmt),

    # single course graph
    path("singlecourse", views.singleCourse, name="singlecourse"),
    path("showCourseGraph/", views.showCourseGraph, name="show-course-graph"),

    # Two courses semantic similarity
    path("similarity", views.SimilarityPage, name="similarity"),
    path("detect/", views.detectSimilarCourse, name="similarity-detect"),

    # All courses semantic similarity
    path("allcourses", views.allCourses, name="allcourses"),
    path("detectAllcourses/", views.detectAllcourses, name="all-courses-similarity"),

    # upload and delete csv files, and clear JSON files
    path("filesManagement", views.filesManagement, name="filesManagement"),
    path("uploadfiles/", views.uploadfile, name="upload-file"),
    path("deleteCSVfiles/", views.deleteCSVfile, name="delete-csv-file"),
    path("deleteJSONfiles/", views.deleteJSONfile, name="delete-json-file"),
    path('download-csv-file/<int:course_id>/', views.download_csv_file, name='download-csv-file'),

     # trajectory
    path("trajectory", views.trajectory, name="trajectory"),
    path("showTrajectory", views.showTrajectory, name="showTrajectory"),

    path("editGraph/<int:course_id>/", views.editGraph, name="editGraph"),
    # path("overview", views.overview, name="overview"),
    path('', views.overview, name='overview'),
    path("save-changes/", views.saveChanges, name="save-changes"),

]