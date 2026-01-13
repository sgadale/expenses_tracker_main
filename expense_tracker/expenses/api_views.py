from rest_framework.decorators import api_view 
from rest_framework import status
from django.contrib.auth import authenticate 
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Expense, Category, MonthlyBudget
from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    BudgetSerializer
)

@api_view(['POST'])
def api_signup(request):
    serializer = SignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    token = Token.objects.create(user=user)

    return Response({
        'message': 'User created successfully',
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })


@api_view(['POST'])
def api_logout(request):
    request.auth.delete()   # 🔥 deletes token from DB
    return Response(
        {'message': 'Logged out successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def expense_list_api(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_expense_api(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)   # ✅ user from token
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def category_list_api(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def budget_api(request):
    if request.method == 'GET':
        budget = MonthlyBudget.objects.filter(user=request.user).last()
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    serializer = BudgetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


