from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe, Author
from .forms import AddAuthorForm, AddRecipeForm, LoginForm


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


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(
                    username=data.get("username"),
                    password=data.get("password")
                )
                Author.objects.create(
                    name=data.get('username'),
                    bio=data.get('bio'),
                    user=new_user
                )
                login(request, new_user)
                return HttpResponseRedirect(reverse("homepage"))
    else:
        return render(request, "no_access.html")

    form = AddAuthorForm()
    return render(request, "generic_form.html", {
        "form": form, "heading": "Add Author"})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=request.user.author,
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions')
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddRecipeForm()
    return render(request, "generic_form.html", {
        "form": form, "heading": "Add Recipe"})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data.get("username"),
                password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage')))
    form = LoginForm()
    return render(request, "generic_form.html", {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
