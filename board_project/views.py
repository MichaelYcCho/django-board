from django.shortcuts import render


def home(request):
    """홈페이지"""
    return render(request, "home.html")
