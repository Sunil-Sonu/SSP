from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *


class CategoriesView(ListView):
    model = Categories

