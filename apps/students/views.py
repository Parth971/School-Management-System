import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Student, StudentBulkUpload
from django.contrib.auth.models import User


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"

    def get_queryset(self):
        queryset = Student.objects.all()
        if self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(current_class_id = self.request.user.staff_set.first().current_class.id)
        return queryset


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = ['current_status', 'registration_number', 'surname', 'firstname',
    'other_name', 'gender', 'date_of_birth', 'current_class', 'date_of_admission', 'parent_mobile_number',
    'address']
    success_message = "New student successfully added."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        return form
    
    def form_valid(self, form):
        instance = form.save()
        user = User.objects.create_user(username=str(instance.registration_number), password=instance.date_of_birth.strftime("%Y%m%d"))
        instance.user = user
        instance.save()
        return redirect(f"/student/{instance.id}/")


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "surname",
                "firstname",
                "other_names",
                "gender",
                "parent_number",
                "address",
                "current_class",
            ]
        )

        return response
