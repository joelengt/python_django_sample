import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core import serializers

from .models import Book
from .forms import BookForm

# Rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
        
# simple html render with data
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# simple json reponse
def get_book_list(request):
    data = {}
    data['items'] = [1, 2, 3]
    data['title'] = 'books'
    return JsonResponse(data)


# get endpoint with rest framework
@api_view(['GET'])
def get_list_book(request):
    status = 200

    books = Book.objects.all()
    
    data = {
        'items': 'elements sample',
        'elements': [1, 2, 3, 4],
        'person': {
            'name': 'joel',
            'age': 21
        },
        'el': [
            {
                'title': 'sample1',
                'date': '2201'
            },
            {
                'title': 'sample2',
                'date': '1998'
            }
        ],
        'ha': json(books)
    }
    return Response(data, status=status)

def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'books/includes/partial_book_create.html')


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)
