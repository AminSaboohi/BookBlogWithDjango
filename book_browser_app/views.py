from .models import ValidatedUrl
from django.views import generic
from .forms import SignUpForm, URLForm
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import BookRow, Author
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
from .url_data_parser import URLData


class HomeView(ListView):
    model = BookRow
    template_name = 'blog_home.html'
    ordering = ['id']


def logout_user(request):
    logout(request)
    messages.success(request, message="You Have Been Logged Out...")
    return redirect('url_validator')


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


def clean_book_author_db():
    for book_row_object in BookRow.objects.all():
        book_row_object.delete()
    for author_object in Author.objects.all():
        author_object.delete()


def add_book_list_to_db(book_list, url_db_obj):
    for book in book_list:
        if Author.objects.filter(name=book['auther']).exists():
            author = Author.objects.filter(name=book['auther']).get()
        else:
            author = Author.objects.create(name=book['auther'], url=url_db_obj)
        BookRow.objects.create(name=book['name'],
                               author=author,
                               rating_avg=book['rating_avg'],
                               raters=book['total_ratings'],
                               published_year=book['year'],
                               editions=book['editions'],
                               )


def url_validator(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            url_db_obj = ValidatedUrl.objects.create(url=url)

            url_parser_object = URLData(url)
            clean_book_author_db()
            book_list = url_parser_object.parse_data()
            add_book_list_to_db(book_list, url_db_obj)

            return redirect('home')
    else:
        form = URLForm()
    return render(request,
                  template_name='url_validator.html',
                  context={'form': form})
