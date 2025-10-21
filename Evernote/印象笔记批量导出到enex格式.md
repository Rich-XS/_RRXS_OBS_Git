最新推荐文章于 2025-04-18 11:44:23 发布

原创 于 2024-12-17 16:23:53 发布 · 1.4k 阅读

· ![](https://csdnimg.cn/release/blogv2/dist/pc/img/newHeart2023Black.png) 9

· ![](https://csdnimg.cn/release/blogv2/dist/pc/img/tobarCollect2.png) 5 ·

#### 印象笔记批量导出到enex格式

- [用到的工具](#_2)
- [工具安装和使用](#_7)

## 用到的工具

大神写的[evernote-backup](https://github.com/vzhd1701/evernote-backup)  
电脑（我这里用的是MacOS，[命令执行](https://so.csdn.net/so/search?q=%E5%91%BD%E4%BB%A4%E6%89%A7%E8%A1%8C&spm=1001.2101.3001.7020)都是在terminal里）

## 工具安装和使用

macOS采用[brew](https://so.csdn.net/so/search?q=brew&spm=1001.2101.3001.7020)安装很方便，其他电脑系统的安装可以去看evernote-backup官网。

```
brew install evernote-backup
```

安装后直接使用

```
mkdir evernoteBackup #创建要保存的目录，可以自定义
cd evernoteBackup

evernote-backup init-db --backend china  #这里是国内的印象笔记要加的后缀--backend china
```

如果顺利的话，可以直接输入用户名，密码了，可惜我这一步不成功，输入密码后一直报错，可以确认密码没错的。于是去[issue](https://github.com/vzhd1701/evernote-backup/issues/70)里找了一个方法：  
先通过这个授权[链接](https://app.yinxiang.com/api/DeveloperToken.action)登陆印象笔记，复制其中的开发者token，然后输入：

```
evernote-backup init-db --backend china -t "复制的token"
evernote-backup reauth --token "复制的token"
```

这里就成功登陆了，然后开始备份：

```
evernote-backup sync
evernote-backup export output_dir/
```

此时去output_dir目录下就能看到导出的enex文件了。  
若不想按照notebook导出，而要全部导出为单独的文件，可以加上–single-notes命令，如果要导出回收箱中的文件，可以加上–include-trash选项，这两个选项我也没试过，如果运行有错误的话还是建议取消。