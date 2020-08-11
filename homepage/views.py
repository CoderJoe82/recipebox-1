from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Recipe, Author
from .forms import AddAuthorForm, AddRecipeForm


def index(request):
    recipes_list = Recipe.objects.all()
    return render(request, "index.html",
                  {"data": recipes_list, "title": "Recipe Box"})


def recipeDetail(request, recipe_id):
    recipe_detail = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html",
                  {"recipe": recipe_detail})


def authorDetail(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    return render(request, "author_detail.html",
                  {"recipes": recipes, "author": author})


def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddAuthorForm()
    return render(request, "generic_form.html", {
        "form": form, "heading": "Add Author"})


def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions')
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddRecipeForm()
    return render(request, "generic_form.html", {
        "form": form, "heading": "Add Recipe"})
