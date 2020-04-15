## 日常问题

* rewrite时post转get了，该怎么解决？

```
location /api/demo {
    rewrite 307 https://api.test.com$request_uri;
}
```

