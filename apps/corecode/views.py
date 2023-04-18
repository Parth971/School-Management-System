from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
    LoginForm
)
from .models import (
    SiteConfig,
    StudentClass,
    Subject,
)
from django.contrib.auth import login, authenticate


def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
            else:
                message = 'Login failed!'
                return render(request, 'registration/login.html', context={'form': form, 'message': message})

            if user.is_staff and not user.is_superuser:
                staff_id = request.user.staff_set.first().id
                return redirect(f"/staff/{staff_id}/")
            elif not user.is_staff:
                student_id = request.user.student_set.first().id
                return redirect(f"/student/{student_id}/")
            return redirect("/")
    return render(
        request, 'registration/login.html', context={'form': form, 'message': message})


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        print(formset.data)
        name = SiteConfig.objects.get(id=1)
        slogan = SiteConfig.objects.get(id=2)
        location = SiteConfig.objects.get(id=3)
        name.value = formset.data.get('form-0-value')
        slogan.value = formset.data.get('form-1-value')
        location.value = formset.data.get('form-2-value')
        name.save()
        slogan.save()
        location.save()
        messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context

    def get_queryset(self):
        queryset = StudentClass.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(id=self.request.user.student_set.first().current_class.id)
        elif self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.staff_set.first().current_class.id)
        return queryset


class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name"]
    success_url = reverse_lazy("classes")
    success_message = "class successfully updated."
    template_name = "corecode/mgt_form.html"


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(current_class_id=self.request.user.student_set.first().current_class.id)
        elif self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(current_class_id=self.request.user.staff_set.first().current_class.id)
        return queryset



class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"

    def form_valid(self, form):
        instance = form.save()
        instance.current_class = self.request.user.staff_set.first().current_class
        instance.save()
        return redirect("/subject/list/")


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)
