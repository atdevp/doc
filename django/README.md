# Django

# Django Rest Framework
## Permissions
### 基本权限类 permissions.BasePermission
* IsAuthenticated
```
return bool(request.user and request.user.is_authenticated)
```
* IsAdminUser
```
return bool(request.user and request.user.is_staff)
```
* 两个基本函数
```
To implement a custom permission, override BasePermission and implement either, or both, of the following methods:

    .has_permission(self, request, view)
    .has_object_permission(self, request, view, obj)
The methods should return True if the request should be granted access, and False otherwise.
```
* 

### 自定义权限类
```
class BlockListPermission(BasePermission):
    def has_permission(self, request, view):
        ip = request.META('REMOTE_ADDR')
        return bool(ip in ip_black_list)

    def has_object_permission(self, request, view, obj):
        if obj.user_id = request.user.id:
            return True
        return False
```

## Pagination
### PageNumberPagination

### LimitOffsetPagination

### CustomPagination

