# Djnago web 框架
<!-- TOC -->

- [Djnago web 框架](#djnago-web-%e6%a1%86%e6%9e%b6)
  - [Model层](#model%e5%b1%82)
    - [字段类型](#%e5%ad%97%e6%ae%b5%e7%b1%bb%e5%9e%8b)
    - [Field选项](#field%e9%80%89%e9%a1%b9)

<!-- /TOC -->
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
