from django.shortcuts import render, redirect


def home(request):
    """홈페이지 - estedu 웹사이트로 리다이렉트"""
    return redirect("https://estedu.framer.website/")
