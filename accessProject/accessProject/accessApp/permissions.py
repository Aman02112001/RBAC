# your_app_name/permissions.py
from rest_framework import permissions

# class CanAddUsers(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Add logic here to check if the user has admin role or not
#         return request.user.is_authenticated and request.user.role in ['Admin']

# class CanAddAPIs(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['Admin', 'User']

# class CanRemoveUsers(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['Admin']
    
# class CanRemoveAPIs(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['Admin', 'User']
    
# class CanViewUsers(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Add logic here to check if the user has admin role or not
#         return request.user.is_authenticated and request.user.role in ['Admin']
    
# class CanViewAPIs(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['Admin', 'User', 'Viewer']
    
# class CanUpdateUsers(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Add logic here to check if the user has admin role or not
#         return request.user.is_authenticated and request.user.role in ['Admin']
    
# class CanUpdateAPIs(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['Admin', 'User']

class CanAddOrUpdateOrRemoveAPIs(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET request to all authenticated users (Admin, User, Viewer)
        if request.method == 'GET' and request.user.is_authenticated:
            return True

        # Allow POST request to only Admin and User
        elif request.method == 'POST' and request.user.is_authenticated and request.user.role in ['Admin', 'User']:
            return True
        
        elif request.method == 'PUT' and request.user.is_authenticated and request.user.role in ['Admin', 'User']:
            return True
        
        elif request.method == 'DELETE' and request.user.is_authenticated and request.user.role in ['Admin', 'User']:
            return True

        return False
    
class AdminCanManageUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, POST, PUT, DELETE requests only if the user is authenticated as an Admin
        return request.user.is_authenticated and request.user.role == 'Admin'
    

# Define other custom permissions for updating, removing, and viewing users and APIs
