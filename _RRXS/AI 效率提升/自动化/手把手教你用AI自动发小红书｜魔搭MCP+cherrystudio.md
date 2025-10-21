---
title: "手把手教你用AI自动发小红书｜魔搭MCP+cherrystudio"
source: "https://blog.csdn.net/seeyouintokyo/article/details/147470874?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%B0%8F%E7%BA%A2%E4%B9%A6%E8%87%AA%E5%8A%A8%E5%8F%91%E5%B8%83&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-7-147470874.142^v102^pc_search_result_base4&spm=1018.2226.3001.4187"
author:
  - "[[seeyouintokyo]]"
published: 2025-04-24
created: 2025-09-09
description: "文章浏览阅读1.5k次，点赞26次，收藏24次。现在AI迷们也可以通过魔搭社区的小红书自动发布MCP，加上CherryStudio的可视化界面，体验一把拼积木乐趣！_搭建自己的小红书mcp服务器"
tags:
  - "clippings"
---
AI 搜索

[会员中心 ![](https://i-operation.csdnimg.cn/images/19298ac6b9144b47885f0c5cece639d9.gif)](https://mall.csdn.net/vip) 

[历史](https://i.csdn.net/#/user-center/history)

[阿星AI工作室](https://blog.csdn.net/seeyouintokyo "阿星AI工作室") 于 2025-04-24 10:33:53 发布

CC 4.0 BY-SA版权

版权声明：本文为博主原创文章，遵循 [CC 4.0 BY-SA](http://creativecommons.org/licenses/by-sa/4.0/) 版权协议，转载请附上原文出处链接和本声明。

本文链接： [https://blog.csdn.net/seeyouintokyo/article/details/147470874](https://blog.csdn.net/seeyouintokyo/article/details/147470874)

#### 背景

最近很多开发者弄了各种 MCP

（可以延伸阅读 [飞书文档秒变高颜值网站！扣子空间MCP杀疯了，小白3步生成商务风主页！](https://mp.weixin.qq.com/s?__biz=MzU3NTE2NjIxMQ==&mid=2247489583&idx=1&sn=51b1fe0ceb1a4905754dc5a6c5753c65&scene=21#wechat_redirect "飞书文档秒变高颜值网站！扣子空间MCP杀疯了，小白3步生成商务风主页！") ）， [小红书](https://so.csdn.net/so/search?q=%E5%B0%8F%E7%BA%A2%E4%B9%A6&spm=1001.2101.3001.7020) 的、高德地图的、点餐的……

可能有人会说实用性没有某宝的自动化工具好，但是MCP挺适合小白练手的我感觉。

比如现在AI迷们也可以 **通过魔搭社区的小红书自动发布MCP，加上CherryStudio的可视化界面** ，体验一把拼积木乐趣！

🤔来练练吧！搞起！

#### 安装CherryStudio

首先，我们安装cherrystudio以更好地使用小红书MCP。具体安装方法如下：

地址：https://cherry-ai.com/

傻瓜式安装，直接下载就完事儿了。

![图片](https://i-blog.csdnimg.cn/direct/5dd4736fc17348eaa3e9a749c910ceb0.png)

#### 小红书发布器MCP

打开魔搭主页，找到mcp广场

![图片](https://i-blog.csdnimg.cn/direct/f04fc709af704f3a93eefde184791828.png)

找到小红书发布器MCP，就可以看到详细配置信息

![图片](https://i-blog.csdnimg.cn/direct/a82123c04fce4df79d482c7ca70841ba.png)

这些罗列出来的都是命令行，我们要做的就是按照说明执行代码。

![图片](https://i-blog.csdnimg.cn/direct/c91ece2bb8e0479595370f2b0bdc20a5.png)

不要头大，一行行来就好了。

#### 构建环境

首先在本地新建一个文件夹，如图。

![图片](https://i-blog.csdnimg.cn/direct/441022ff07a84dc2a4d629bfe4fa48be.png)

找个纯英文路径下面自己新建一个就行了。

![图片](https://i-blog.csdnimg.cn/direct/4eefd99b568945478a47c911f3ff590c.png)

获取一个路径，如果卡住了，就用下面的命令行授权就可以了，实在不知道可以问deepseek。

`chmod +x /Users/xingyang/Downloads/codecode/xhs`

如果你电脑上 *没* 有no de.js,直接自己傻瓜式安装下

网址:https://nodejs.org/zh-cn

![图片](https://i-blog.csdnimg.cn/direct/c56463d2f76748e884d6dd47f8d67ca3.png)

#### 安装谷歌驱动

首先确认自己的 chrome 版本号。

查询到你的 Chrome 版本后，例如 "134.0.6998.166"，然后下载对应的版本

比如我的版本是135.0.7049.96

那么我就把和这个代码的末尾换成我的版本号就行了

```crystal
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

接着，你可以看到chrome自动启动了一个后台，并且已经填写好了手机号（我这里把自己的隐去了）

![图片](https://i-blog.csdnimg.cn/direct/d1bb0a07645b466b91d3a09066c2391f.png)

此刻你能在终端看到等待输入验证码👇🏻

看下手机，其实你手机上已经有验证码发过来了，直接输入即可。

![图片](https://i-blog.csdnimg.cn/direct/6d81760aaf2e4db188fd8931feb4af0a.png)

接着启动本地上传物料用的web页面，注意这里仍然需要替换成你自己的手机号！！！👇

```cobol
npx @modelcontextprotocol/inspector -e phone=YOUR_PHONE_NUMBER python -m xhs_mcp_server
```

你可能和我一样遇到端口冲突。

几个大红❌。

不要紧张，家常便饭，很好处理。

![图片](https://i-blog.csdnimg.cn/direct/f1bc176dcd2340cd873dfe72f7596ea4.png)

依旧查询哪个坏蛋占用了6277.**(注意端口号是随机的，你的可不一定是这个数）**

```cobol
lsof -i :6277

kill -9 <PID>

替换为👇🏻

kill -9 1371
```

你会得到一个端口列表，如果写的是1371占用了。那么你的PID直接替换为1371。

如果还有别的牛鬼蛇神🐂，直接按照下面这个代码替换端口杀掉。

```cobol
kill -9 $(lsof -t -i :6274) 2>/dev/null
```

接着继续尝试启动本地web👇

```cobol
npx @modelcontextprotocol/inspector -e phone=YOUR_PHONE_NUMBER python -m xhs_mcp_server
```

注意这里仍然需要替换成你自己的手机号。

如果你遇到报错：

No such file or directory: '/Users/bruce/xiaohongshu\_cookies.json'

直接用👇下面代码自己创建一个这个名字的文件：

```cobol
sudo mkdir -p /Users/bruce && sudo touch /Users/bruce/xiaohongshu_cookies.json && sudo chmod 777 /Users/bruce/xiaohongshu_cookies.json
```

看到这个激动人心的小火箭了吗👇🚀，这就是成功了！

赶紧复制对应的地址到你浏览器里打开 ![图片](https://i-blog.csdnimg.cn/direct/4ad878e7c19f4c0c93e3d59a6741bd79.png)

我把界面给大家翻译过来看下，这个就是我们上传小红书物料的工作台。

![图片](https://i-blog.csdnimg.cn/direct/b2586cbce3994a54a4fd9014fa00f1aa.png)

#### 拉起本地web上传图片

这个界面相当于你自家做饭的灶台，所有东西都在你本地了。

现在点击左侧的连接（connect），会变成绿点，代表你的web已经链接服务成功。

![图片](https://i-blog.csdnimg.cn/direct/87def9c0baf64ff3917381613194baab.png)

点击中间的tools，就可以上传图文或者视频。

我选择的是添加图片。

![图片](https://i-blog.csdnimg.cn/direct/4daeccd7c89d42b89a3aa1ff2bca13cc.png)

点击run tool，你会看到它正在帮你拉起小红书页面。

到了这一步之后你可以直接用cherrystudio继续。

这个就是用cherrystudio发的，所以才会出现你不提供内容模型可能会插嘴代劳的情况👇

**它发了一张自己的照片——python，然后问大家它是不是天才** 🤔

![图片](https://i-blog.csdnimg.cn/direct/a53a692a92a94eeca65c07434524635c.png)

#### 配置CherryStudio

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

**——** **—** **—** **————**

  
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

![](https://kunyu.csdn.net/1.png?p=58&adBlockFlag=1&adId=1073999&a=1073999&c=3264858&k=%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E7%94%A8AI%E8%87%AA%E5%8A%A8%E5%8F%91%E5%B0%8F%E7%BA%A2%E4%B9%A6%EF%BD%9C%E9%AD%94%E6%90%ADMCP+cherrystudio&spm=1001.2101.3001.5002&articleId=147470874&d=1&t=3&u=8b120ad8e1854cf4b4696b9bc4df0b4c)[*小红书* 封面 *MCP* 智能体工作流全流程拆解！](https://blog.csdn.net/ice_99/article/details/148637050)

[

最新发布

](https://blog.csdn.net/ice_99/article/details/148637050)

[ice\_99的博客](https://blog.csdn.net/ice_99)

06-13 1306[*AI* 开 *发* 范式正在 *发* 生深刻变化，越来越多业务场景正在通过智能体 *+* *自动* 化工作流实现真正的“全流程 *AI* 赋能”。 借着这股趋势，我最近也拆解了一批典型实战案例。今天先拆一套高频且实用的场景——\*\* *小红书* 封面自由生成工作流\*\*，实现从内容输入 → 智能拆解 → 风格生成 → 网页封面 → *自动* 下载的全流程闭环。](https://blog.csdn.net/ice_99/article/details/148637050)[影刀PRA做 *小红书* *自动* *发* 布视频\_影刀 *自动* *发* 布 *小红书*](https://blog.csdn.net/weixin_38249775/article/details/147953998)

9-5[1、准备好你要 *发* 布的视频,流程参数里面添加上你的标题以及内容 2、打开网址 *小红书* 创作服务平台 3、捕获元素 4、进行视频上传操作 5、等到出现替换视频的时候,表示视频上传成功 6、录入标题以及文本 输入的内容直接从流程参数拿 7、点击 *发* 布按钮 操作目标都是捕获元素,添加到元素库的 大家自己下载软件,注册一下,然后自己体验一下,超级简单的一个流程,玩...](https://blog.csdn.net/weixin_38249775/article/details/147953998)[释放你的时间:*自动* *发* 布 *小红书* 的全面指南\_ *小红书* *自动* *发* 布](https://blog.csdn.net/m0_52535283/article/details/139115194)

9-3[选择“延迟”,设置为10s 选择“点击元素”,模拟点击“ *发* 布”按钮 点击“执行”操作,*自动* 完成 *小红书* 图文信息](https://blog.csdn.net/m0_52535283/article/details/139115194)[【亲测免费】 twitter- *mcp* ：让Client轻松互动Twitter，实现 *发* 文与搜索](https://blog.csdn.net/gitblog_01008/article/details/146802148)

[gitblog\_01008的博客](https://blog.csdn.net/gitblog_01008)

03-31 817[twitter- *mcp* ：让Client轻松互动Twitter，实现 *发* 文与搜索 Twitter *MCP* Server 是一款功能强大的开源项目，旨在让Client能够便捷地与Twitter进行互动，包括 *发* 送推文和搜索推文。 项目介绍 Twitter *MCP* Server 是一款基于Node.js的中间件服务，允许Client通过API与Twitter平台进行交互。用户可以借助这个服务在Twitter...](https://blog.csdn.net/gitblog_01008/article/details/146802148)[*AI* 赋能内容创作:一键生成图片视频并 *自动* *发* 布至 *小红书*](https://blog.csdn.net/lbh73/article/details/147753879)

8-21[素材生成:调用图像生成模型制作分镜头画面 *自动* 剪辑:使用开源工具(如 moviepy)实现画面拼接、转场效果添加 音频匹配:通过语音合成或版权音乐库添加背景音效 三、 *小红书* *自动* 化 *发* 布的实现路径 (一)平台API对接策略 *小红书* 开放平台提供有限的 *自动* 化接口,可通过以下组合实现高效 *发* 布: 图片优化:使用智能压缩算法将图片大小控制在...](https://blog.csdn.net/lbh73/article/details/147753879)[智能博客小助手（二）利用 *MCP* 我可以一键轰炸各个平台—— *小红书* ，知乎](https://blog.csdn.net/qq_61302385/article/details/147540250)

[qq\_61302385的博客](https://blog.csdn.net/qq_61302385)

04-26 2001[*MCP* 协议（Model Context Protocol）是一种协议，旨在为大型语言模型（LLM）提供标准化的外部数据源与工具连接方式，其核心目的是充当 *大模型* 与外部工具、数据源和行为（Actions）之间的交互“桥梁”。大型语言模型在精确计算、实时信息获取（如天气）、与特定系统交互（如数据库、本地文件、API）等等方面存在局限性。而 *MCP* 协议可以为 *大模型* 提供统一接口。](https://blog.csdn.net/qq_61302385/article/details/147540250)[解放双手!*MCP* 服务 *自动* *发* 布 *小红书* 笔记(含源码)](https://blog.csdn.net/nccbpm/article/details/148437264)

9-2[*MCP* 服务 *自动* *发* 布 *小红书* 笔记(含源码) 一、背景与需求分析 目标用户痛点 内容团队:需同时管理多个品牌账号,手动 *发* 布易错且难以统计效果; 电商卖家:商品笔记需高频更新,但 *小红书* 后台缺乏批量上传工具; 个人IP:希望定时 *发* 布内容以维持活跃度,但受限于平台功能。 商业场景延伸...](https://blog.csdn.net/nccbpm/article/details/148437264)[*AI* 赚钱新思路 利用RPA *+* KIMI实现 *小红书* 全 *自动* 制作 *发* 布(详细攻略)](https://blog.csdn.net/weixin_42172073/article/details/140288793)

9-8[三:*小红书* 笔记的 *发* 布流程: 首先登录到 *小红书* 的创作平台。 接着上传我们之前生成的治愈系图文图片。 填写笔记的标题和文案内容。标题可以自己创作,或者让Kimi在生成治愈文案的同时,也生成一个吸引人的标题。 确保文案内容吸引人,可以使用Kimi生成的长文案,以增加笔记的感染力。](https://blog.csdn.net/weixin_42172073/article/details/140288793)[【随缘更新，免积分下载】Selenium chromedriver驱动下载（最新版136.0.7103.49）](https://blog.csdn.net/qq_42771102/article/details/142853514)

[

热门推荐

](https://blog.csdn.net/qq_42771102/article/details/142853514)

[python探索](https://blog.csdn.net/qq_42771102)

10-11 2万+[chromedriver.exe是一款与Chrome浏览器结合的驱动工具，支持 *自动* 化测试、网络爬虫及其他需要浏览器 *自动* 化的场景。它可以与Selenium等流行的 *自动* 化测试框架集成，执行 *自动* 访问、输入、点击等操作。应用场景:*自动* 化测试：与测试框架结合，进行网页元素的 *自动* 化测试。网络爬虫：实现页面抓取和数据采集。Web *自动* 化操作：诸如 *自动* 登录、表单提交等常规操作。](https://blog.csdn.net/qq_42771102/article/details/142853514)[...抓取爆款笔记(一)\_chapbox 在 *小红书* *自动* *发* 布信息](https://blog.csdn.net/u014534808/article/details/138890075)

9-9[\[*小红书* 写文 *发* 文机器人.mp4\] 完整步骤: 1、新建应用 点击新建按钮,新建一个PC *自动* 化应用 2.设定浏览网页 新建一个【打开选择文件夹对话框】,这样我们可以自定义图片保存目录 再使用【打开网页】指令 浏览器类型这里我使用的是谷歌Chrome浏览器 在网址中输入我们要打开的地址,我们要打开网址是 *小红书* 的推荐页...](https://blog.csdn.net/u014534808/article/details/138890075)[使用 *小红书* *MCP* *服务器* ，智能批量导出数据进行 *AI* 分析！](https://devpress.csdn.net/v1/article/detail/147684471)

[Aicu\_icu的博客](https://blog.csdn.net/Aicu_icu)

05-03 1155[*小红书* *MCP* *服务器* 是一款高效的 *小红书* 数据处理工具，通过 *MCP* 协议与主流 *AI* 客户端无缝对接，支持多平台运行。它具备极速纯接口操作、安全合规的网络环境以及智能任务执行能力，可实现笔记、用户、评论等数据的搜索、获取、分析与导出。其功能丰富，包括文案创作、数据导出、用户分析等，能大幅提升 *小红书* 数据处理效率，助力用户高效运营。](https://devpress.csdn.net/v1/article/detail/147684471)[Cherry Studio *搭建* 个人知识库，太好用了！（按头收藏）](https://devpress.csdn.net/v1/article/detail/145606716)

[2401\_84494441的博客](https://blog.csdn.net/2401_84494441)

02-13 1万+[今天我就再给大家推荐一款非常适合我们国人的 *AI* 助手神器 – Cherry Studio。这款工具使用简单，自带大量提示词模板，省掉了我们需要针对不同场景优化提示词的时间；还支持生成图片、翻译、 *搭建* 个人知识库等诸多功能。总而言之，Cherry Studio 上手简单，功能强大，可以说重新定义了 *AI* 工具，如果只推荐一款 *AI* 终端应用的话，那么我推荐它，赶紧用起来吧！！本文详细介绍如何使用 Cherry Studio，阅读之前先加个关注吧～](https://devpress.csdn.net/v1/article/detail/145606716)[从零成本到零门槛：如何用某 *魔* *搭* 社区 *MCP* 服务解锁Cherry Studio新玩法](https://malijinkuang.blog.csdn.net/article/details/147851747)

[分享平时的学习心得和笔记](https://blog.csdn.net/lbh73)

05-10 592[某 *魔* *搭* 社区 *MCP* 广场作为国内最大的 *AI* 模型开源平台，提供了近1500款服务，涵盖网页抓取、地图查询、支付集成等高频场景。通过其托管的Hosted服务，用户无需自建云主机即可享受零成本、高安全性和开箱即用的便利。 *MCP* 支持两种主流接入方式：手动配置SSE和同步 *服务器* 功能，后者操作简单、安全性高且零成本。同步 *服务器* 功能的实战教程包括 *魔* *搭* 端准备、Cherry Studio配置和实战应用。进阶技巧涉及服务权限控制、性能优化和常见问题解决。真实案例展示了如何通过同步「Fetch *+* 本地文件系统」双服务 *搭建* 智能笔记助手。](https://malijinkuang.blog.csdn.net/article/details/147851747)[Chromedriver 下载地址—70.0.3538.16-140.0.7339.80（不定时持续更新中）](https://blog.csdn.net/qq_30607843/article/details/140947472)

[qq\_30607843的博客](https://blog.csdn.net/qq_30607843)

08-06 1万+[整理自 https://googlechromelabs.github.io/chrome-for-testing](https://blog.csdn.net/qq_30607843/article/details/140947472)[coze *小红书* *自动* *发* 布](https://wenku.csdn.net/answer/3f4hvwdefv)

03-10[好的，我现在需要帮助用户寻找关于 *小红书* *自动* *发* 布的工具或方法。首先，我得仔细看看用户提供的引用内容，里面有几个相关的项目和信息。用户提到了四个引用，其中引用1到4都涉及 *小红书* *自动* 化工具，特别是引用3和4详细...](https://wenku.csdn.net/answer/3f4hvwdefv)

评论

被折叠的 0 条评论 [为什么被折叠?](https://blogdev.blog.csdn.net/article/details/122245662)[到【灌水乐园】发言](https://bbs.csdn.net/forums/FreeZone)

添加红包

实付 元

[使用余额支付](https://blog.csdn.net/seeyouintokyo/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

 [![](https://csdnimg.cn/release/blogv2/dist/pc/img/toolbar/Group.png) 点击体验  
DeepSeekR1满血版](https://ai.csdn.net/?utm_source=cknow_pc_blogdetail&spm=1001.2101.3001.10583) 隐藏侧栏 搜索

此内容解决你搜索的问题？ 否 是

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部

![](https://i-blog.csdnimg.cn/direct/5dd4736fc17348eaa3e9a749c910ceb0.png) ![](https://i-blog.csdnimg.cn/direct/f04fc709af704f3a93eefde184791828.png) ![](https://i-blog.csdnimg.cn/direct/a82123c04fce4df79d482c7ca70841ba.png) ![](https://i-blog.csdnimg.cn/direct/c91ece2bb8e0479595370f2b0bdc20a5.png) ![](https://i-blog.csdnimg.cn/direct/441022ff07a84dc2a4d629bfe4fa48be.png) ![](https://i-blog.csdnimg.cn/direct/4eefd99b568945478a47c911f3ff590c.png) ![](https://i-blog.csdnimg.cn/direct/c56463d2f76748e884d6dd47f8d67ca3.png) ![](https://i-blog.csdnimg.cn/direct/8b71a2efe9c847c3a0c43b8e8251c0ac.png) ![](https://i-blog.csdnimg.cn/direct/d1bb0a07645b466b91d3a09066c2391f.png) ![](https://i-blog.csdnimg.cn/direct/6d81760aaf2e4db188fd8931feb4af0a.png) ![](https://i-blog.csdnimg.cn/direct/f1bc176dcd2340cd873dfe72f7596ea4.png) ![](https://i-blog.csdnimg.cn/direct/4ad878e7c19f4c0c93e3d59a6741bd79.png) ![](https://i-blog.csdnimg.cn/direct/b2586cbce3994a54a4fd9014fa00f1aa.png) ![](https://i-blog.csdnimg.cn/direct/87def9c0baf64ff3917381613194baab.png) ![](https://i-blog.csdnimg.cn/direct/4daeccd7c89d42b89a3aa1ff2bca13cc.png) ![](https://i-blog.csdnimg.cn/direct/a53a692a92a94eeca65c07434524635c.png) ![](https://i-blog.csdnimg.cn/direct/c0e05db271a4421f99452440fe62e40c.png) ![](https://i-blog.csdnimg.cn/direct/6853de18c44d45b6a15703a25798aa4c.png) ![](https://i-blog.csdnimg.cn/direct/8d479eb7f4b042659bc3d4e167066231.png) ![](https://i-blog.csdnimg.cn/direct/004330dbbaa14412b119522e00c273e6.png) ![](https://i-blog.csdnimg.cn/direct/d5f97d7727374920b8cac4457f56f3e5.png)