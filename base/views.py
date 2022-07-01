from distutils.log import Log
from turtle import title
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from base.models import Books
# Create your views here.

# Login Functionality


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('books')


# user creation
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        user = form.save()
        if(user is not None):
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # redirect users
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('books')
        return super(RegisterPage, self).get(*args, **kwargs)


# CRUD Functionalities
# after adding LoginRequiredMixin it will be restricted
# need to override default urls
class BookList(LoginRequiredMixin, ListView):
    model = Books
    context_object_name = 'books'

    # user should get his own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = context['books']
        context['count'] = context['books'].filter(
            finished_reading=False).count()
        return context


class BookDetail(LoginRequiredMixin, DetailView):
    model = Books
    context_object_name = 'book'
    template_name = 'base/book.html'


class BookCreate(LoginRequiredMixin, CreateView):
    model = Books
    fields = ['title', 'author', 'finished_reading', 'review']
    success_url = reverse_lazy('books')
    template_name = 'base/book_form.html'

    # setting default user as user logged in in form handling
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BookCreate, self).form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Books
    fields = ['title', 'author', 'finished_reading', 'review']
    success_url = reverse_lazy('books')
    template_name = 'base/book_form.html'


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Books
    context_object_name = 'book'
    success_url = reverse_lazy('books')
    template_name = 'base/book_confirm_delete.html'
