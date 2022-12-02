
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
import ExpenseTracker


# Create your views here.
INTEGER_CHOICES = [tuple([x, x]) for x in range(1, 32)]
NAME_CHOICES = [
    ('food', 'Food'),
    ('transportation', 'Transportation'),
    ('rent', 'Rent'),
    ('education', 'Education'),
    ('leisure', 'Leisure'),
    ('utilities', 'Utilities'),
    ('other', 'Other')
]

MONTH_CHOICES = [
    ('january', 'Januaray'),
    ('february', 'February'),
    ('march', 'March'),
    ('april', 'April'),
    ('may', 'May'),
    ('june', 'June'),
    ('july', 'July'),
    ('august', 'August'),
    ('september', 'September'),
    ('october', 'October'),
    ('november', 'November'),
    ('december', 'December')
]


class NewTaskForm(forms.Form):
    name = forms.CharField(label="name")
    salary = forms.IntegerField(label="salary", min_value=1)


class ItemTaskForm(forms.Form):
    item_name = forms.CharField(
        label="item name", widget=forms.Select(choices=NAME_CHOICES))

    item_price = forms.IntegerField(label="item price (USD)", min_value=0)

    item_month = forms.CharField(
        label="month of purchase", widget=forms.Select(choices=MONTH_CHOICES))

    item_date = forms.IntegerField(
        label="day of purchase", widget=forms.Select(choices=INTEGER_CHOICES))


def tables(request):
    if "itemmonths" not in request.session:
        request.session["itemnames"] = []
        request.session["itemprices"] = []
        request.session["itemmonths"] = []
        request.session["itemdates"] = []

    return render(request, "main/tables.html", {
        "itemprices": request.session["itemprices"],
        "itemnames": request.session["itemnames"],
        "itemmonths": request.session["itemmonths"],
        "itemdates": request.session["itemdates"]

    })


def index(request):
    return render(request, "main/index.html")


def create(request, salary):
    #salary = request.POST['salary']
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if (form.is_valid()):
            name = form.cleaned_data["name"]
            request.session["name"] = []
            request.session["name"] += [name]

            salary = form.cleaned_data["salary"]
            request.session["salary"] = []
            request.session["salary"] += [salary]
            Savings = ExpenseTracker.Savings.set_money(salary)

            #ExpenseTracker.Savings.set_money(salary, salary)
            context = {}
            context["some_string"] = ExpenseTracker.Savings.get_money(Savings)

            return render(request, "main/create.html", context)
        else:
            return render(request, "main/create.html", {
                "forms": form
            })
    return render(request, "main/create.html", {
        "forms": NewTaskForm()
    })


def add(request):
    if request.method == "POST":
        form = ItemTaskForm(request.POST)
        if form.is_valid():

            item_price = form.cleaned_data["item_price"]
            request.session["itemprices"] += [item_price]

            item_date = form.cleaned_data["item_date"]
            request.session["itemdates"] += [item_date]

            item_month = form.cleaned_data["item_month"]
            request.session["itemmonths"] += [item_month]

            item_name = form.cleaned_data["item_name"]
            request.session["itemnames"] += [item_name]

            return HttpResponseRedirect(reverse("main:tables"))
        else:
            return render(request, "main/add.html", {
                "form": form
            })
    return render(request, "main/add.html", {
        "form": ItemTaskForm()
    })


def Summary(request):
    return HttpResponse("hello")
