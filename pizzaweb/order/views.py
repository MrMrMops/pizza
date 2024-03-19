from .tasks import send_email
from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, FormView

from cart.forms import CartAddProductFormPost
from pizzaweb.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL

from .forms import AddPostForm, LoginUserForm, RegisterForm, AboutForm
from order.models import Product


class Index(ListView):
    model = Product
    template_name = 'order/index.html'
    context_object_name = 'pizzas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        return dict(list(context.items()))
    def get_queryset(self):
        post_list_qs = cache.get('post_list_qs')
        if not post_list_qs:
            post_list_qs = Product.objects.all()
            cache.set(
                'post_list_qs',
                post_list_qs,
                60*15,
            )
        return post_list_qs

class AddPostFormView(LoginRequiredMixin,CreateView):
    form_class = AddPostForm
    template_name = 'order/add_post.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return dict(list(context.items()))

class PostView(DetailView):
    model = Product
    template_name = 'order/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'].price = int(context['post'].price)
        cart_product_form = CartAddProductFormPost()
        context['cart_product_form']= cart_product_form

        return context

def logout_user(request):

    logout(request)
    return redirect('index')

class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'order/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'order/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('index')

class AboutViewForm(FormView):
    form_class = AboutForm
    template_name = 'order/recall.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return dict(list(context.items()))

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        try:
            send_email.delay(subject,from_email, message,)
        except BadHeaderError:
            return HttpResponse('Ошибка в теме письма.')
        return redirect('index')

