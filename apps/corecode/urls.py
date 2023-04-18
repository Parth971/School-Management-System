from django.urls import path

from .views import (
    ClassCreateView,
    ClassDeleteView,
    ClassListView,
    ClassUpdateView,
    IndexView,
    SiteConfigView,
    SubjectCreateView,
    SubjectDeleteView,
    SubjectListView,
    SubjectUpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("site-config", SiteConfigView.as_view(), name="configs"),
    path("class/list/", ClassListView.as_view(), name="classes"),
    path("class/create/", ClassCreateView.as_view(), name="class-create"),
    path("class/<int:pk>/update/", ClassUpdateView.as_view(), name="class-update"),
    path("class/<int:pk>/delete/", ClassDeleteView.as_view(), name="class-delete"),
    path("subject/list/", SubjectListView.as_view(), name="subjects"),
    path("subject/create/", SubjectCreateView.as_view(), name="subject-create"),
    path(
        "subject/<int:pk>/update/",
        SubjectUpdateView.as_view(),
        name="subject-update",
    ),
    path(
        "subject/<int:pk>/delete/",
        SubjectDeleteView.as_view(),
        name="subject-delete",
    ),
]
