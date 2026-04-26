from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import *
# from store.urls import store_indexindex


def index(request):
    return redirect('store_index')
