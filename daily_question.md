## 日常问题


### Nginx
* rewrite时post转get了，该怎么解决？

```
location /api/demo {
    rewrite 307 https://api.test.com$request_uri;
}
```

* rewrite 用法
  - rewrite 全站
  ```
    {
        server 80;
        server 443 ssl;

        server www.old.com;
        return 301 $scheme://www.new.com$request_uri;
    }
    ```
  - rewrite 路径重写
  ```
    rewrite ^(/download/.*)/media/(\w+)\.?.*$ $1/mp3/$2.mp3 last;
    rewrite ^(/download/.*)audio/(\w+)\.?.*$ $1/mp3/$2.ra last;
  ``` 
* return 用法
    - return (301 | 302 | 302 | 307 ) url;
    - `return 301 https://new.com/api/feed.go`
    - return (1xx | 2xx | 3xx | 4xx | 5xx) ["text"] 
    - `return 401 "Access denied because of token is expired or invalid"`