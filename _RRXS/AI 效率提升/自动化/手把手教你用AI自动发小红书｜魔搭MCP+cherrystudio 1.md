https://blog.csdn.net/seeyouintokyo/article/details/147470874?ops_request_misc=elastic_search_misc&request_id=3a2a60677a7303041e5204a89f14f362&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-147470874-null-null.142^v102^pc_search_result_base3&utm_term=AI%E8%87%AA%E5%8A%A8%E5%8F%91%E5%B8%83%E5%86%85%E5%AE%B9%E5%88%B0%E5%B0%8F%E7%BA%A2%E4%B9%A6MCP%E5%B9%B3%E5%8F%B0%E7%9A%84%E6%96%B9%E6%B3%95%E5%92%8C%E5%B7%A5%E5%85%B7&spm=1018.2226.3001.4187
#### **背景**

最近很多开发者弄了各种MCP

（可以延伸阅读[飞书文档秒变高颜值网站！扣子空间MCP杀疯了，小白3步生成商务风主页！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247489583&idx=1&sn=51b1fe0ceb1a4905754dc5a6c5753c65&scene=21#wechat_redirect "飞书文档秒变高颜值网站！扣子空间MCP杀疯了，小白3步生成商务风主页！")），[小红书](https://so.csdn.net/so/search?q=%E5%B0%8F%E7%BA%A2%E4%B9%A6&spm=1001.2101.3001.7020)的、高德地图的、点餐的……

可能有人会说实用性没有某宝的自动化工具好，但是MCP挺适合小白练手的我感觉。

比如现在AI迷们也可以**通过魔搭社区的小红书自动发布MCP，加上CherryStudio的可视化界面**，体验一把拼积木乐趣！

🤔来练练吧！搞起！

#### **安装CherryStudio**

首先，我们安装cherrystudio以更好地使用小红书MCP。具体安装方法如下：

地址：https://cherry-ai.com/

傻瓜式安装，直接下载就完事儿了。

![图片](https://i-blog.csdnimg.cn/direct/5dd4736fc17348eaa3e9a749c910ceb0.png)

#### **小红书发布器MCP**

打开魔搭主页，找到mcp广场

![图片](https://i-blog.csdnimg.cn/direct/f04fc709af704f3a93eefde184791828.png)

找到小红书发布器MCP，就可以看到详细配置信息

![图片](https://i-blog.csdnimg.cn/direct/a82123c04fce4df79d482c7ca70841ba.png)

这些罗列出来的都是命令行，我们要做的就是按照说明执行代码。

![图片](https://i-blog.csdnimg.cn/direct/c91ece2bb8e0479595370f2b0bdc20a5.png)

不要头大，一行行来就好了。

#### **构建环境**

首先在本地新建一个文件夹，如图。

![图片](https://i-blog.csdnimg.cn/direct/441022ff07a84dc2a4d629bfe4fa48be.png)

找个纯英文路径下面自己新建一个就行了。

![图片](https://i-blog.csdnimg.cn/direct/4eefd99b568945478a47c911f3ff590c.png)

获取一个路径，如果卡住了，就用下面的命令行授权就可以了，实在不知道可以问deepseek。

`chmod +x /Users/xingyang/Downloads/codecode/xhs`

如果你电脑上_没_有node.js,直接自己傻瓜式安装下

网址:https://nodejs.org/zh-cn

![图片](https://i-blog.csdnimg.cn/direct/c56463d2f76748e884d6dd47f8d67ca3.png)

#### **安装谷歌驱动**

首先确认自己的chrome版本号。

查询到你的 Chrome 版本后，例如 "134.0.6998.166"，然后下载对应的版本

比如我的版本是135.0.7049.96

那么我就把和这个代码的末尾换成我的版本号就行了

```
npx @puppeteer/browsers install chromedriver@135.0.7049.96
```

如果运行中间让你选yes和no，直接填入y，然后回车即可。

然后安装小红书mcp服务

```
pip install xhs-mcp-server
```

记得你的验证码一定要在终端里输入，不要在红薯前端输入！！！！

![图片](https://i-blog.csdnimg.cn/direct/8b71a2efe9c847c3a0c43b8e8251c0ac.png)

**看到cookies登陆成功，才是真的成功，其他的都不对！！！！**

```
env phone=YOUR_PHONE_NUMBER python -m xhs_mcp_server.__login__
```

接着，你可以看到chrome自动启动了一个后台，并且已经填写好了手机号（我这里把自己的隐去了）

![图片](https://i-blog.csdnimg.cn/direct/d1bb0a07645b466b91d3a09066c2391f.png)

此刻你能在终端看到等待输入验证码👇🏻

看下手机，其实你手机上已经有验证码发过来了，直接输入即可。

![图片](https://i-blog.csdnimg.cn/direct/6d81760aaf2e4db188fd8931feb4af0a.png)

接着启动本地上传物料用的web页面，注意这里仍然需要替换成你自己的手机号！！！👇

```
npx @modelcontextprotocol/inspector -e phone=YOUR_PHONE_NUMBER python -m xhs_mcp_server
```

你可能和我一样遇到端口冲突。

几个大红❌。

不要紧张，家常便饭，很好处理。

![图片](https://i-blog.csdnimg.cn/direct/f1bc176dcd2340cd873dfe72f7596ea4.png)

依旧查询哪个坏蛋占用了6277.**(注意端口号是随机的，你的可不一定是这个数）**

```
lsof -i :6277kill -9 <PID>替换为👇🏻kill -9 1371
```

你会得到一个端口列表，如果写的是1371占用了。那么你的PID直接替换为1371。

如果还有别的牛鬼蛇神🐂，直接按照下面这个代码替换端口杀掉。

```
kill -9 $(lsof -t -i :6274) 2>/dev/null
```

接着继续尝试启动本地web👇

```
npx @modelcontextprotocol/inspector -e phone=YOUR_PHONE_NUMBER python -m xhs_mcp_server
```

注意这里仍然需要替换成你自己的手机号。

如果你遇到报错：

No such file or directory: '/Users/bruce/xiaohongshu_cookies.json'

直接用👇下面代码自己创建一个这个名字的文件：

```
sudo mkdir -p /Users/bruce && sudo touch /Users/bruce/xiaohongshu_cookies.json && sudo chmod 777 /Users/bruce/xiaohongshu_cookies.json
```

看到这个激动人心的小火箭了吗👇🚀，这就是成功了！

赶紧复制对应的地址到你浏览器里打开![图片](https://i-blog.csdnimg.cn/direct/4ad878e7c19f4c0c93e3d59a6741bd79.png)

我把界面给大家翻译过来看下，这个就是我们上传小红书物料的工作台。

![图片](https://i-blog.csdnimg.cn/direct/b2586cbce3994a54a4fd9014fa00f1aa.png)

#### **拉起本地web上传图片**

这个界面相当于你自家做饭的灶台，所有东西都在你本地了。

现在点击左侧的连接（connect），会变成绿点，代表你的web已经链接服务成功。

![图片](https://i-blog.csdnimg.cn/direct/87def9c0baf64ff3917381613194baab.png)

点击中间的tools，就可以上传图文或者视频。

我选择的是添加图片。

![图片](https://i-blog.csdnimg.cn/direct/4daeccd7c89d42b89a3aa1ff2bca13cc.png)

点击run tool，你会看到它正在帮你拉起小红书页面。

到了这一步之后你可以直接用cherrystudio继续。

这个就是用cherrystudio发的，所以才会出现你不提供内容模型可能会插嘴代劳的情况👇

**它发了一张自己的照片——python，然后问大家它是不是天才**🤔

![图片](https://i-blog.csdnimg.cn/direct/a53a692a92a94eeca65c07434524635c.png)

#### **配置CherryStudio**

打开刚下载的CherryStudio，打开魔搭。密钥自己找，填进去后打开右上角的绿色按钮。

![图片](https://i-blog.csdnimg.cn/direct/c0e05db271a4421f99452440fe62e40c.png)

这时候其实你已经可以去cherrystudio部署mcp配置了。

点左侧的MCP服务器，然后点右上角的MCP配置👇

![图片](https://i-blog.csdnimg.cn/direct/6853de18c44d45b6a15703a25798aa4c.png)

直接往里复制👇

![图片](https://i-blog.csdnimg.cn/direct/8d479eb7f4b042659bc3d4e167066231.png)

点确定保存。

直接新建对话，给到想发的小红书。

**注意图片需要是本地路径形式。（我不是图里这样，我本人比图里好看🫣）**

![图片](https://i-blog.csdnimg.cn/direct/004330dbbaa14412b119522e00c273e6.png)

见证奇迹的时候发生了，直接就是一顿自动发送～

![图片](https://i-blog.csdnimg.cn/direct/d5f97d7727374920b8cac4457f56f3e5.png)

学废了吗朋友，我一个文科生玩下来只想说，好神奇哦～

纯纯为了体验技术，也是很有趣的哦～

**——****—****—****————**

  
往期文章：

- [扣子空间杀疯了！3分钟写出并上线小游戏「赛博木鱼」附邀请码](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247489554&idx=1&sn=c6fa14a6524fd40608a72e9e99008722&scene=21#wechat_redirect "扣子空间杀疯了！3分钟写出并上线小游戏「赛博木鱼」附邀请码")
    
- [我开发了史上最矫情MCP：偷偷记录"我想你了"](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247489373&idx=1&sn=fc1e910208dcb7e11e7901be00824ec4&scene=21#wechat_redirect "我开发了史上最矫情MCP：偷偷记录\"我想你了\"")
    
- [字节大佬真开源了！复刻Manus的AI生产力神器免费白嫖！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247489176&idx=1&sn=0801c965963dc0e7d36263a486783709&scene=21#wechat_redirect "字节大佬真开源了！复刻Manus的AI生产力神器免费白嫖！")
    
- [保姆级教程｜5分钟扣子搞定AI日报！打工人必备提效神器](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488970&idx=1&sn=0bb49af5cd8e3ca2b1b6a85904b5e704&scene=21#wechat_redirect "保姆级教程｜5分钟扣子搞定AI日报！打工人必备提效神器")
    
- [免费调用DeepSeek-R1！硅基流动注册&API密钥使用全攻略](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488280&idx=1&sn=d06a82a7146d8482e517d9b114beded1&scene=21#wechat_redirect "免费调用DeepSeek-R1！硅基流动注册&API密钥使用全攻略")
    
- [手机端部署DeepSeek-R1！手把手教你5步搞定](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488208&idx=1&sn=1651748f8e0b85809c133590acf305bc&scene=21#wechat_redirect "手机端部署DeepSeek-R1！手把手教你5步搞定")
    
- [白嫖DeepSeekR1搭建个人AI知识库！小白3步上手](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488157&idx=1&sn=5d2abbe31dfcb552e17044c65ecbd5e8&scene=21#wechat_redirect "白嫖DeepSeekR1搭建个人AI知识库！小白3步上手")
    
- [deepseekR1搭建个人AI知识库！性价比之王！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488139&idx=1&sn=7b87dd940c45eb560db7a8035f924466&scene=21#wechat_redirect "deepseekR1搭建个人AI知识库！性价比之王！")
    
- [DeepSeek梁文锋采访整理：R1大模型火出圈之前](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488021&idx=1&sn=e1b6a881bffb7433bc25f0711acbbcf1&scene=21#wechat_redirect "DeepSeek梁文锋采访整理：R1大模型火出圈之前")
    
- [横空出世的AI黑马！DeepSeekR1凭什么让巨头们坐不住了？](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488016&idx=1&sn=abf26d38993d48e684a048847b28a323&scene=21#wechat_redirect "横空出世的AI黑马！DeepSeekR1凭什么让巨头们坐不住了？")
    

- [我的圣诞帽生成器被官方推荐上首页啦！公开教程来了](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487635&idx=1&sn=7f5e598d2097ae5b9bdb405961a15321&scene=21#wechat_redirect "我的圣诞帽生成器被官方推荐上首页啦！公开教程来了")
    
- [AI小程序备案：深度合成类目保姆级避坑教程](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487710&idx=1&sn=88d72c5e6c85a8346a3e75e51c683930&scene=21#wechat_redirect "AI小程序备案：深度合成类目保姆级避坑教程")
    
- [0代码基础小白如何上架第一个Chrome AI 插件？](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487594&idx=1&sn=1bb77ce559e7016e71927fbf29d06a3d&scene=21#wechat_redirect "0代码基础小白如何上架第一个Chrome AI 插件？")
    

- [Cursor+Coze快速入门：小白也能轻松开发小程序！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487658&idx=1&sn=4875266b962d24500296fbb99d12653e&scene=21#wechat_redirect "Cursor+Coze快速入门：小白也能轻松开发小程序！")
    
- [扣子2025首次重磅更新，1分钟看完6大功能](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487729&idx=1&sn=ae936a1227fb752a547167f98284844d&scene=21#wechat_redirect "扣子2025首次重磅更新，1分钟看完6大功能")
    
- [好用到哭！我用AI独立开发了「豆包即梦去水印插件」，再也不用重复劳动！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247487990&idx=1&sn=db5e1442d74bfbe3b3610be84cba00ed&scene=21#wechat_redirect "好用到哭！我用AI独立开发了「豆包即梦去水印插件」，再也不用重复劳动！")
    
- [苹果ios专属🥰1分钟拼成九宫格丨快捷指令](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247488005&idx=1&sn=8e94e20ad49d1a216641ae5aa57a19b4&scene=21#wechat_redirect "苹果ios专属🥰1分钟拼成九宫格丨快捷指令")
    

p.s.

部分图片来自网络，仅供学习分享，版权归原作者所有，如有侵权，可联系我们删除。