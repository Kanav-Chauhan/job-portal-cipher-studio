from django.urls import path
from .views import *

urlpatterns = [
  path("jobs/", JobListCreate.as_view()),
  path("jobs/<int:id>/", JobDetail.as_view()),
  path("jobs/<int:id>/duplicate/", JobDuplicate.as_view()),
  path("analytics/", Analytics.as_view()),
]
