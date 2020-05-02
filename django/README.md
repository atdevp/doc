# Djnago web 框架
<!-- TOC -->

- [Djnago web 框架](#djnago-web-%e6%a1%86%e6%9e%b6)
  - [跨域](#%e8%b7%a8%e5%9f%9f)
  - [Model层](#model%e5%b1%82)
    - [字段类型](#%e5%ad%97%e6%ae%b5%e7%b1%bb%e5%9e%8b)
    - [Field选项](#field%e9%80%89%e9%a1%b9)
  - [基于函数的API视图,重点用到了DRF的装饰器](#%e5%9f%ba%e4%ba%8e%e5%87%bd%e6%95%b0%e7%9a%84api%e8%a7%86%e5%9b%be%e9%87%8d%e7%82%b9%e7%94%a8%e5%88%b0%e4%ba%86drf%e7%9a%84%e8%a3%85%e9%a5%b0%e5%99%a8)
  - [基于类视图](#%e5%9f%ba%e4%ba%8e%e7%b1%bb%e8%a7%86%e5%9b%be)
  - [Permissions和Authentications](#permissions%e5%92%8cauthentications)
    - [Permissions](#permissions)
    - [Authentications](#authentications)
    - [自定义权限类](#%e8%87%aa%e5%ae%9a%e4%b9%89%e6%9d%83%e9%99%90%e7%b1%bb)
  - [Pagination](#pagination)
    - [PageNumberPagination](#pagenumberpagination)
    - [LimitOffsetPagination](#limitoffsetpagination)
    - [CustomPagination](#custompagination)

<!-- /TOC -->
## 跨域
* django自身解决
  - `安装插件`
    ```
    pip3  install django-cors-headers
    ```

  - `更新配置`

    ```
    INSTALLED_APPS = [
        "corsheaders"
    ]

    CORS_ORIGIN_ALLOW_ALL = True

    MIDDLEWARE = [
        <!-- 必须在CsrfViewMiddleware、CommonMiddleware之前 -->
        "corsheaders.middleware.CorsMiddleware"
    ]
    ```

## Model层

### 字段类型
https://www.xyhtml5.com/django-docs22/ref/models/fields.html

* SmallAutoField
* AutoField 
* BigAutoField
```
默认自增自建
SmallAutoField
id = models.AutoField(primary_key=True)
BigAutoField和AutoField差不多，取值变大1 to 9223372036854775807.
```

* SmallIntegerField
```
-32768 to 32767
```
* IntegerField
```
整型 -2147483648 to 2147483647
```

* BigIntegerField 
```
长整型 -9223372036854775808 to 9223372036854775807
```
* BinaryField
```
二进制字段
```
* BoolField、NullBoolField
* CharField、TextField
* DateField、DateTimeField、
```
auto_now：当对象被保存时,自动将该字段的值设置为当前时间.通常用于表示 “last-modified” 时间戳；
auto_now_add：当对象首次被创建时,自动将该字段的值设置为当前时间.通常用于表示对象创建时间。
```
* DecimalField
* DurationField
* EmailField
```
不接受 maxlength 参数
```
* FileField
* FilePathField
* FloatField
* ImageField
* GenericIPAddressField
* PositiveIntegerField
* PositiveSmallIntegerField
* TimeFiled
* URLField
```
用于保存 URL。 若 verify_exists 参数为 True (默认)， 给定的 URL 会预先检查是否存在(即URL是否被有效装入且没有返回404响应)。
```
* UUIDField
```
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```
* ForeignKey
* ManyToManyField
* OneToOneField
* PhoneNumberField
```
xxx-xxx-xxxx
```

### Field选项
* null
```
缺省设置为false.通常不将其用于字符型字段上，比如CharField,TextField上.字符型字段如果没有值会返回空字符串。
```
* blank
```
是否可以为空
```
* max_length
* choices
```
二位数组
HOST_CHOICES=((1, "virtual"),(2, "phyical"))
第一个值是实际存储的值，第二个用来方便进行选择
```
* db_index
* db_column
* default
* editable

```
如果为假，admin模式下将不能改写。缺省为真
```
* primary_key
* help_text
* unique
*


## 基于函数的API视图,重点用到了DRF的装饰器
```
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Reponse
from rest_framework.perssions import IsAdminUser, IsAuthenticated

@permission_classes('IsAdminUser', 'IsAuthencticated')
@api_view(http_method_names=['GET', 'POST']) # @api_view(['GET', 'POST'])
def user_list(request):
    users = UserModel.objects.all()
    return Reponse(data=users, status_code=)  

```

## 基于类视图

```
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.perssions import IsAdminUser, IsAuthenticated

class UserList(APIView):
    
    # 可插拔的API策略属性
    permisson_classes = [IsAdminUser, IsAuthenticated,]
    authentication_classes = []
    
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        pass

```

## Permissions和Authentications
### Permissions
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
### Authentications
* SessionAuthencation

* BaseAuthencation

* TokenAuthencation



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
