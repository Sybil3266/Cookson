from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Recipe
# Create your views here.

class RecipeListView(ListView):
    model = Recipe
    paginate_by = 10
    template_name = 'recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
