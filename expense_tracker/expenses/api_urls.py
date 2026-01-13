from django.urls import path
from . import api_views

urlpatterns = [
    path('signup/', api_views.api_signup),
    path('login/', api_views.api_login), 
    path('logout/', api_views.api_logout), 
    path('expenses/', api_views.expense_list_api),
    path('expenses/add/', api_views.add_expense_api),
    path('categories/', api_views.category_list_api),
    path('budget/', api_views.budget_api),
]
