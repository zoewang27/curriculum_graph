
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphvisualiztion/", include("graphvisualiztion.urls")),
    path("account/", include("account.urls")),
    path('', lambda request: redirect('graphvisualiztion/', permanent=False)), 

]
