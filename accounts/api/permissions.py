from rest_framework import permissions

class IsAutherReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate,self).has_permission(request, view)

class IsSuperUser(permissions.BasePermission):
   """
   Custom permission to only allow superuser to retrieve or edit.
   """
   def has_permission(self, request, view):
       return request.user and request.user.is_superuser 