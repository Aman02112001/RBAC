# Create your views here.

# your_app_name/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import API, CustomUser, Token
from .permissions import CanAddOrUpdateOrRemoveAPIs, AdminCanManageUsers
from .serializers import CustomUserSerializer, APISerializer
from rest_framework.views import APIView
from .forms import UserRegistrationForm, UserLoginForm
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db import models

# @api_view(['POST'])
# def register_user(request):
#     # Your logic to register a user
#     serializer = CustomUserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def register(request):-
#     form = UserRegistrationForm() 
#     return render(request, 'registration.html',  {'form': form})

################################ Home Page ########################################
def home(request):
    return render(request, 'home.html')

################################ Register Page ########################################
@api_view(['GET', 'POST'])
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ')
            return redirect('login')
        context = {'form':form}
        return render(request, 'register.html', context)
    
    # For GET requests, render the registration form
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
    # try:
    #     form = UserRegistrationForm()
    #     if request.method == 'POST':
    #         form = UserRegistrationForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             user = form.cleaned_data.get('username')
    #             messages.success(request, 'Account was created for ' + user)

    #             return redirect('login')
                    
    #         context = {'form':form}
    #         return render(request, 'register.html', context)
        
    # except Exception as e:
    #     print("Error: ", str(e))

################################ Login Page ########################################
@api_view(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            refresh = RefreshToken.for_user(user)
            # Return the refresh token and access token as JSON response
            expires_at = timezone.now() + timedelta(seconds=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
            token, _ = Token.objects.update_or_create(
                user=user,
                defaults={
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'expires_at': expires_at
                }
            )

    # return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            # return JsonResponse({
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token)
            # })
            context = {
                'user': user,
                'access_token': str(refresh.access_token), 
            }
            return render(request, 'dashboard.html', context)

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# @api_view(['POST'])
# def user_login(request):
#     # Your logic for user login
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
    
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_200_OK)
#     return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

################################ Add User ########################################
def addUser(request):
    return render(request, 'add_user.html')

@api_view(['POST'])
@permission_classes([AdminCanManageUsers])
def add_user(request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################ Add API ########################################
def addAPI(request):
    return render(request, 'add_api.html')

@api_view(['POST'])
@permission_classes([CanAddOrUpdateOrRemoveAPIs])
def add_api(request):
        api_data = {
        'user': request.user.id,
        'name': request.data.get('name'),
        'url': request.data.get('url'),
        'endpoint': request.data.get('endpoint'),
        'description': request.data.get('description'),
        'mapped_users': [request.user.id],
        }
        serializer = APISerializer(data=api_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################ Remove User ########################################
def removeUser(request):
    return render(request, 'remove_user.html')

@api_view(['DELETE'])
@permission_classes([AdminCanManageUsers])
def remove_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

################################ Remove API ########################################
def removeAPI(request):
    return render(request, 'remove_api.html')

@api_view(['DELETE'])
@permission_classes([CanAddOrUpdateOrRemoveAPIs])
def remove_api(request, api_id):
    try:
        api = API.objects.get(pk=api_id)
    except API.DoesNotExist:
        return Response({'detail': 'API not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 'Admin' and api.user_id != request.user.id:
        return Response({'detail': '401 Unauthorized Exception'}, status=status.HTTP_403_FORBIDDEN)
    
     # Check if the API is associated with any user
    if CustomUser.objects.filter(apis__id=api_id).exists() and api.user_id != request.user.id:
        return Response({'detail': 'The API is associated with a user. Delete the user first.'},
                        status=status.HTTP_400_BAD_REQUEST)

    api.delete()
    return Response({'detail': 'API deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

################################ Update User ########################################
@api_view(['GET'])
@permission_classes([AdminCanManageUsers])
def getUser(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
def updateUser(request,user_id):
    if user_id == 0 and request.method == 'GET' :
        return render(request, 'update_user.html')
    return render(request, 'update_user_form.html', {'user_id': user_id})

# def updateUserForm(request, user_id):
#     # print(user_id)
#     return render(request, 'update_user_form.html', {'user_id': user_id})

@api_view(['PUT'])
@permission_classes([AdminCanManageUsers])
def update_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # print(request.data)

    password = request.data.get('password')
    if password:
        hashed_password = make_password(password)
        request.data['password'] = hashed_password

    serializer = CustomUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################ Update API ########################################
@api_view(['GET'])
@permission_classes([CanAddOrUpdateOrRemoveAPIs])
def getApi(request, api_id):
    try:
        apis = API.objects.filter(id = api_id)
        serializer = APISerializer(apis, many=True)
        return Response(serializer.data)
    except API.DoesNotExist:
        return Response({'detail': 'API not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
def updateAPI(request, api_id):
    if api_id == 0 and request.method == 'GET':
        return render(request, 'update_api.html')
    return render(request, 'update_api_form.html', {'api_id': api_id})

# def updateAPIForm(request, api_id):
#     # print(user_id)
#     return render(request, 'update_api_form.html', {'api_id': api_id})

@api_view(['PUT'])
@permission_classes([CanAddOrUpdateOrRemoveAPIs])
def update_api(request, api_id):
    try:
        api = API.objects.get(pk=api_id)
    except API.DoesNotExist:
        return Response({'detail': 'API not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 'Admin' and api.user_id != request.user.id:
        return Response({'detail': '401 Unauthorized Exception'}, status=status.HTTP_403_FORBIDDEN)

    api_data = {
    'user': request.user.id,
    'name': request.data.get('name'),
    'url': request.data.get('url'),
    'endpoint': request.data.get('endpoint'),
    'description': request.data.get('description'),
    }
    serializer = APISerializer(api, data=api_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################ View API ########################################
def viewAPI(request):
    return render(request, 'view_api.html')

@api_view(['GET'])
@permission_classes([CanAddOrUpdateOrRemoveAPIs])
def view_api(request):
    if request.user.role in ['Admin', 'Viewer']:
        # Viewer and Admin can view all APIs
        apis = API.objects.all()
        print(apis)
    else:
        # User can view only their own APIs
        # apis = API.objects.filter(user_id = request.user.id)
        apis = API.objects.filter(models.Q(user_id=request.user.id) | models.Q(mapped_users=request.user)).distinct()
        # apis_list = list(apis)

    # Step 2: Remove duplicate elements by converting the list to a set
    # unique_apis_set = set(apis_list)

    # Step 3: If you need to convert the set back to a list for serializer input
    # unique_apis_list = list(unique_apis_set)

    serializer = APISerializer(apis, many=True)
    return Response(serializer.data)

################################ View User ########################################
def viewUser(request):
    return render(request, 'view_user.html')

@api_view(['GET'])
@permission_classes([AdminCanManageUsers])
def view_user(request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
        # return render(request, 'view_user.html', {'users': serializer.data})


################################## Map User to Api ####################################
def map_page(request):
    return render(request, 'map_page.html')

def map_input_page(request, api_id):
    return render(request, 'map_input_page.html',  {'api_id': api_id})

@api_view(['GET','POST'])
@permission_classes([AdminCanManageUsers])  # Only admin can map APIs to users
def map_api_to_users(request, api_id):
    if request.method == 'POST':
        try:
            api = API.objects.get(pk=api_id)
        except API.DoesNotExist:
            return Response({'detail': 'API not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get a list of usernames to be mapped with the API
        usernames = request.data.get('usernames', [])

        # Check if all usernames exist in the User database
        for username in usernames:
            try:
                user = CustomUser.objects.get(username=username)
            except user.DoesNotExist:
                return Response({'detail': f'User with username "{username}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the User objects for the provided usernames
        users = CustomUser.objects.filter(username__in=usernames)

        # Add the valid users to the mapped_users field using add()
        api.mapped_users.add(*users)

        return Response({'detail': 'API mapped to users successfully'}, status=status.HTTP_200_OK)
    
    else:
        return render(request, 'map_api_to_user.html')


# @api_view(['GET', 'POST'])
# class APIListView(APIView):
#     permission_classes = [CanAddOrUpdateOrRemoveAPIs]  # Add the required permission class

#     def get(self, request):
#         apis = API.objects.all()
#         serializer = APISerializer(apis, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = APISerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # Implement other views for updating, removing, and viewing users and APIs with respective permissions

#Views for APIs

# @api_view(['GET', 'POST'])
# @permission_classes([CanAddOrUpdateOrRemoveAPIs, IsOwnerOfAPI])
# def api_list(request):
    # if request.method == 'GET':
    #     if request.user.role == 'Viewer':
    #         # Viewer can view all APIs
    #         apis = API.objects.all()
    #     else:
    #         # User can view only their own APIs
    #         apis = API.objects.filter(user_id = request.user.id)
        
    #     serializer = APISerializer(apis, many=True)
    #     return Response(serializer.data)

    # elif request.method == 'POST':
    #     api_data = {
    #     'user': request.user.id,
    #     'name': request.data.get('name'),
    #     'url': request.data.get('url'),
    #     'endpoint': request.data.get('endpoint'),
    #     'description': request.data.get('description'),
    #     }
    #     serializer = APISerializer(data=api_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([CanAddOrUpdateOrRemoveAPIs])
# def api_detail(request, api_id):
    # try:
    #     api = API.objects.get(pk=api_id)
    # except API.DoesNotExist:
    #     return Response({'detail': 'API not found.'}, status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     serializer = APISerializer(api)
    #     return Response(serializer.data)

    # elif request.method == 'PUT':
    #     if api.user_id != request.user.id:
    #         return Response({'detail': '401 UnAuthorized Exception'}, status=status.HTTP_403_FORBIDDEN)

    #     api_data = {
    #     'user': request.user.id,
    #     'name': request.data.get('name'),
    #     'url': request.data.get('url'),
    #     'endpoint': request.data.get('endpoint'),
    #     'description': request.data.get('description'),
    #     }
    #     serializer = APISerializer(api, data=api_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     if api.user_id != request.user.id:
    #         return Response({'detail': '401 UnAuthorized Exception'}, status=status.HTTP_403_FORBIDDEN)

    #     api.delete()
    #     return Response({'detail': 'API deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#Views for Users

# @api_view(['GET', 'POST'])
# @permission_classes([AdminCanManageUsers])
# def user_list(request):
    # if request.method == 'GET':
    #     users = CustomUser.objects.all()
    #     serializer = CustomUserSerializer(users, many=True)
    #     return Response(serializer.data)

    # elif request.method == 'POST':
    #     serializer = CustomUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([AdminCanManageUsers])
# def user_detail(request, user_id):
    # try:
    #     user = CustomUser.objects.get(pk=user_id)
    # except CustomUser.DoesNotExist:
    #     return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     serializer = CustomUserSerializer(user)
    #     return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = CustomUserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     user.delete()
    #     return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
