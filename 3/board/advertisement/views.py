from django.shortcuts import render
from django.http import HttpResponse


def advertisement_list(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement_list.html', {})


def advertisement_detail(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement_details.html', {})


def advertisement_python_part_1(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement-python-part-1.html', {})


def advertisement_python_part_2(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement-python-part-2.html', {})


def advertisement_python_django(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement-python-django.html', {})


def advertisement_python_advanced(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement-python-advanced.html', {})


def advertisement_web_layout(request, *args, **kwargs):
    return render(request, 'advertisement/advertisement-web-layout.html', {})
