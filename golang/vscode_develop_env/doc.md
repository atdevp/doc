# 使用vscode作为开发环境基本配置

## 安装插件
```
commmand+shift+P
Install extensions  选择go版本
```

### 自动补全和自动倒入包

* 国内用户配置下代理
    ```
    perferences->settings  找到http.proxy,编辑settings.json

    {
        "http.proxy": "http://127.0.0.1:9999"
    }
    ```
* command+shift+P ,输入 go:install/update/tools
    ```
    gocode
    gopkgs
    go-outline
    go-symbols
    guru
    gorename
    dlv
    godef
    godoc
    goreturns
    golint
    gotests
    gomodifytags
    impl
    fillstruct
    goplay
    ```

* 编辑settings.json
    ```
    {
        "go.autocompleteUnimportedPackages": true,
    }
    ```