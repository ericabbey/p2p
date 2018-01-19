from django.shortcuts import render

def about(request):
    return render(request, 'flatpages/about.html', {})

def hiw(request):
    return render(request, 'flatpages/hiw.html', {})

def index(request):
    return render(request, 'flatpages/index.html', {})

def terms(request):
    return render(request, 'flatpages/terms.html', {})

def faq(request):
    return render(request, 'flatpages/faq.html', {})
