from django.urls import re_path, path

from api.api import ClassAPIView, YearAPIView, StudentAPIView
from api.views import StatisticsTemplateView, HomeTemplateView

app_name = 'api'

urlpatterns = [
    re_path(r"^statistics/(?P<search_text>\w+)/$", StatisticsTemplateView.as_view(), name="statistics-template"),
    path("", HomeTemplateView.as_view(), name="home-template"),
    path("api/statistics/class", ClassAPIView.as_view(), name="class_report"),
    path("api/statistics/student", StudentAPIView.as_view(), name="student_report"),
    path("api/statistics/year", YearAPIView.as_view(), name="yearly_report"),
]
