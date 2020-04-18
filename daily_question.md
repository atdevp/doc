## 日常问题


### Nginx
* rewrite时post转get了，该怎么解决？

```
location /api/demo {
    rewrite 307 https://api.test.com$request_uri;
}
```

* rewrite 到新域名
```
{
    server 80;
    server 443 ssl;

    server www.old.com;
    return 301 $scheme://www.new.com$request_uri;
}
```