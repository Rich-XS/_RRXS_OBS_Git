---
title: "Colab使用教程（超级详细版）及Colab Pro/Pro+评测"
source: "https://blog.csdn.net/javastart/article/details/138094086?ops_request_misc=%257B%2522request%255Fid%2522%253A%25224b0a03dd336342d8e2c5d6988949f325%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=4b0a03dd336342d8e2c5d6988949f325&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-138094086-null-null.142^v102^pc_search_result_base4&utm_term=colab&spm=1018.2226.3001.4187"
author:
  - "[[javastart]]"
published: 2024-04-22
created: 2025-09-13
description: "文章浏览阅读3.7w次，点赞110次，收藏331次。Pro+增加到了3个高RAM会话和3个标准会话，在Pro基础上又翻了2.5倍，相当于免费版算力的9倍，Pro+的52GB的高RAM和Pro的25GB的高RAM相比也略有提升（10分钟的epoch能快2分钟左右）。在打开笔记本后，我们默认的文件路径是\"/content\"，这个路径也是执行笔记本时的路径，同时我们一般把用到的各种文件也保存在这个路径下。如果在有代码块执行的情况下继续点击其他代码块的“播放”按钮，则这些代码块进入“等待执行”的状态，按钮也就会进入转圈的状态，但外部的圆圈是虚线。_colab"
tags:
  - "Colab"
---
原文： [Colab使用教程（超级详细版）及Colab Pro/Pro+评测 - 知乎](https://zhuanlan.zhihu.com/p/666938608 "Colab使用教程（超级详细版）及Colab Pro/Pro+评测 - 知乎")

在下半年选修了 [机器学习](https://so.csdn.net/so/search?q=%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&spm=1001.2101.3001.7020) 的关键课程Machine learning and deep learning，但由于Macbook Pro显卡不支持 cuda ，因此无法使用GPU来训练网络。教授推荐使用Google [Colab](https://so.csdn.net/so/search?q=Colab&spm=1001.2101.3001.7020) 作为训练神经网络的平台。在高强度的使用了Colab一段时间后，我把自己的个人感受和使用心得与大家分享，同时也给想要尝试的同学详细介绍Colab具体的上手方法。

### 一、Colab介绍

在第一次使用Colab时，最大的困难无疑是对整个平台的陌生而导致无从下手，因此我首先介绍与Colab相关的基础概念，以帮助大家更快地熟悉Colab平台。

### Colab是什么？

Colab = Colaboratory（即合作实验室），是谷歌提供的一个在线工作平台，用户可以直接通过浏览器执行python代码并与他人分享合作。Colab的主要功能当然不止于此，它还为我们提供免费的GPU。熟悉深度学习的同学们都知道：CPU计算力高但核数量少，善于处理线性序列，而GPU计算力低但核数量多，善于处理并行计算。在深度学习中使用GPU进行计算的速度要远快于CPU，因此有高算力的GPU是深度学习的重要保证。由于不是所有GPU都支持深度计算（大部分的Macbook自带的显卡都不支持），同时显卡配置的高低也决定了计算力的大小，因此Colab最大的优势在于我们可以“借用”谷歌免费提供的GPU来进行深度学习。

综上：Colab = "python版"Google doc + 免费GPU

### Colab相关的概念

Jupyter Notebook ：在Colab中，python代码的执行是基于.ipynb文件，也就是Jupyter Notebook格式的python文件。这种笔记本文件与普通.py文件的区别是可以分块执行代码并立刻得到输出，同时也可以很方便地添加注释，这种互动式操作十分适合一些轻量的任务。

具体关于Jupyter Notebook的信息可以查看下面官网的链接： [https://jupyter.org/](https://link.zhihu.com/?target=https%3A//jupyter.org/ "https://jupyter.org/")

代码执行程序：代码执行程序就是Colab在云端的"服务器"。简单来说，我们先在笔记本写好需要运行的代码，连接到代码执行程序，然后Colab会在云端执行代码，最后把结果传回浏览器。

实例空间：连接到代码执行程序后，Colab需要为其分配实例空间(Instance)，可以简单理解为运行笔记本而创建的"虚拟机"，其中包含了执行ipynb文件时的默认配置、环境变量、自带的库等等。

### 二、Colab工作流程

介绍完了基本概念，下面我们来演示具体如何使用Colab

### 准备工作

首先我们需要创建一个谷歌账户，申请谷歌账户需要能接受短信的手机号码。作者在写这篇文章时亲自进行了一次测试，发现目前不能通过中国手机来创建账户，但是账号在创建后可以改绑中国手机。由于跃墙、如何申请谷歌账户不是本文的写作目的，因此这里就不作展开了，我个人猜测万能的某宝之类应该有解决办法。

![](https://i-blog.csdnimg.cn/blog_migrate/ac331d6f7fb459665b96269f637a6b28.png)

Colab一般配合Google Drive使用（下文会提到这一点）。因此如有必要，我建议拓展谷歌云端硬盘的储存空间，个人认为性价比较高的是基本版或标准版。在购买完额外的空间后，头像外部会出现一个四色光环，就像作者一样。

![](https://i-blog.csdnimg.cn/blog_migrate/a28d399dbc89a9ada54e74cdb3d81885.png)

  
**新建笔记本**

有两种方法可以新建一个笔记本，第一种是在在云端硬盘中右键创建。

![](https://i-blog.csdnimg.cn/blog_migrate/5e32a286ac9bb4c0f28297e91b219023.png)

如果右键后没有发现有这一个选项，那是因为云端硬盘还没有安装Colab。这时在右击后选择“关联更多应用”，然后搜索colab并下载，之后就可以通过右键创建了。

![](https://i-blog.csdnimg.cn/blog_migrate/69ed9140388c9f41ffbe6b9447cb55d4.png)

![](https://i-blog.csdnimg.cn/blog_migrate/c1b76d089bf2209ebd6120bc95e9b134.png)

第二种方法是直接在浏览器中输入 [https://colab.research.google.com](https://link.zhihu.com/?target=https%3A//colab.research.google.com/ "https://colab.research.google.com") ，进入Colab的页面后点击新建笔记本即可。使用这种方法新建的笔记本时，会在云端硬盘的根目录自动创建一个叫Colab Notebook的文件夹，新创建的笔记本就保存在这个文件夹中。

![](https://i-blog.csdnimg.cn/blog_migrate/426cdd50b6e5d8b137d381d007d6682f.png)

![](https://i-blog.csdnimg.cn/blog_migrate/93c8bd8fab44898b6f2bc1cd86306e65.png)

**载入笔记本**

可以打开云端硬盘中的已经存在的笔记本，还可以从Github中导入笔记本。如果关联了Github账户，可以选择一个账户中的Project，如果其中有ipynb文件就可以在Colab中打开。注意：关联Github不是把Github中的项目文件夹加载到实例空间！

![](https://i-blog.csdnimg.cn/blog_migrate/c2df505a534c12561e96df6a157150b1.png)

![](https://i-blog.csdnimg.cn/blog_migrate/7150f742c417492de49f47f8fc9bea67.png)

### 笔记本界面

![](https://i-blog.csdnimg.cn/blog_migrate/5d4f1688d725296a6a58fcc1267c9d4a.png)

**标题** ：笔记本的名称

**代码块** ：分块执行的代码

**文件浏览** ：Colab为笔记本分配的实例空间

**代码执行程序** ：用于执行笔记本程序的服务器

**代码段** ：常用的代码段，比如装载云端硬盘

**命令面板** ：常用的命令，比如查找/替换

**终端** ：文件浏览下的终端（非常卡，不建议使用）

### 连接代码执行程序

点击连接按钮即可在5s左右的时间内连接到代码执行程序，此时可以看到消耗的RAM和磁盘

**RAM** ：虚拟机运行内存，更大内存意味着更大的算力（之后会在Colab Pro中介绍）

**磁盘** ：虚拟机文件的储存空间，要注意的是购买更多云端硬盘存储空间不能增加可用磁盘空间

在打开笔记本后，我们默认的文件路径是"/content"，这个路径也是执行笔记本时的路径，同时我们一般把用到的各种文件也保存在这个路径下。在点击".."后即可返回查看根目录"/"（如下图），可以看到根目录中保存的是一些虚拟机的环境变量和预装的库等等。不要随意修改根目录中的内容，以避免运行出错，我们所有的操作都应在"/content"中进行。

### 执行代码块

.ipynb文件通过的代码块来执行代码，同时支持通过"!<command>"的方式来执行UNIX终端命令（比如"!ls"可以查看当前目录下的文件）。Colab已经预装了大多数常见的深度学习库，比如pytorch，tensorflow等等，如果有需要额外安装的库可以通过"!pip3 install <package>"命令来安装。下面是一些常见的命令。

```cobol
# 加载云端硬盘 

from google.colab import drive 

drive.mount('/content/drive') 

 

# 查看分配到的GPU 

gpu_info = !nvidia-smi 

gpu_info = '\n'.join(gpu_info) 

if gpu_info.find('failed') >= 0: 

    print('Not connected to a GPU') 

else: 

    print(gpu_info) 

 

# 安装python包 

!pip3 install <package>
```

点击“播放”按钮执行代码块。代码块开始执行后，按钮就会进入转圈的状态，表示“正在执行”，外部的圆圈是实线。如果在有代码块执行的情况下继续点击其他代码块的“播放”按钮，则这些代码块进入“等待执行”的状态，按钮也就会进入转圈的状态，但外部的圆圈是虚线。在当前代码块结束后，会之前按照点击的顺序依次执行这些代码块。

![](https://i-blog.csdnimg.cn/blog_migrate/c94f8205bdd8288710cb1926535a7c6c.png)

### 设置笔记本的运行时类型

笔记本在打开时的默认硬件加速器是None，运行规格是标准。在深度学习中，我们希望使用GPU来进行深度计算，同时如果购买了pro，我们希望使用高内存模式。点击代码执行程序，然后点击“更改运行时类型即可”。由于免费的用户所能使用的GPU运行时有限，由于免费的用户所能使用的GPU运行时有限，因此建议在模型训练结束后调回None模式或直接结束会话。

![](https://i-blog.csdnimg.cn/blog_migrate/c2d75dcd1f1387237e6308e2a192c637.png)

如果希望主动断开代码执行程序，则点击代码执行程序后选择“断开连接并删除运行时”即可。

### 管理会话Session

会话就是当前连接到代码执行程序的笔记本，通过点击“管理会话”即可查看当前的所有会话，点击“终止”即可断开代码执行程序。用户所能连接的会话数量是有限的，因此到达上限时再开启新会话需要主动断开之前的会话。

![](https://i-blog.csdnimg.cn/blog_migrate/d74ab788149d8cb55e2bc1a2f499a90c.png)

### 三、Colab重要特性

在这一部分，我们进一步了解Colab平台的一些重要特性和使用Colab训练模型时的一些策略

### 资源使用的限制

Google Colab为用户提供免费的GPU，因此资源使用必然会受到限制（即使是Colab Pro+用户也不例外），而这种限制无处不在。

**有限的实例空间** ：实例空间的内存和磁盘都是有限制的，如果模型训练的过程中超过了内存或磁盘的限制，那么程序运行就会中断并报错。实例空间内的文件保存不是永久的，当代码执行程序被断开时，实例空间内的所有资源都会被释放（我们在"/content"目录下上传的文件也会全部消失）。

![](https://i-blog.csdnimg.cn/blog_migrate/65cec7939efa6a23d13f8a2453d0f39f.png)

**有限的连接时间** ：笔记本连接到代码执行程序的时长是有限制的，这体现在三个方面：如果关闭浏览器，代码执行程序会在短时间内断开而不是在后台继续执行（这个“短时间”大概在几分钟左右，如果只是切换一下wifi之类是不会有影响的）；如果空闲状态过长（无互动操作或正在执行的代码块），则会立即断开连接；如果连接时长到达上限（免费用户最长连接12小时），也会立刻断开连接。

![](https://i-blog.csdnimg.cn/blog_migrate/5e8a3f246a08a842d8360157747a31b7.png)

**有限的GPU运行时** ：无论是免费用户还是colab pro用户，每天所能使用的GPU运行时间都是有限的。到达时间上限后，代码执行程序将被立刻断开且用户将被限制在当天继续使用任何形式的GPU（无论是否为高RAM形式）。在这种情况下我们只能等待第二天重置。

**频繁的互动检测** ：当一段时间没有检测到活动时，Colab就会进行互动检测，如果长时间不点击人机身份验证，代码执行程序就会断开。此外，如果频繁地执行“断开-连接”代码执行程序，也会出现人机身份验证。

**有限的会话数量** ：每个用户所能开启的会话数量都是有限的，免费用户只能开启1个会话，Pro用户则可以开启多个会话。不同的用户可以在一个笔记本上可以进行多个会话，但只能有一个代码块开始执行。如果某个代码块已经开始执行，另一个用户连接到笔记本的会话会显示“忙碌状态”，需要等待代码块执行完后才能执行其他的代码块。注意：掉线重连、切换网络、刷新页面等操作也会使笔记本进入“忙碌状态”。

![](https://i-blog.csdnimg.cn/blog_migrate/eccd56be8c6add74e200085a56b1405b.png)

  
正常情况

![](https://i-blog.csdnimg.cn/blog_migrate/e03f5b80a231a94e9c39307696637bad.png)

忙碌状态

### 如何合理使用资源？

1. 将训练过后的模型日志和其他重要的文件保存到谷歌云盘，而不是本地的实例空间
2. 运行的代码必须支持“断点续传”能力，简单来说就是必须定义类似checkpoint功能的函数；假设我们一共需要训练40个epochs，在第30个epoch掉线了之后模型能够从第30个epoch开始训练而不是从头再来
3. 仅在模型训练时开启GPU模式，在构建模型或其他非必要情况下使用None模式
4. 在网络稳定的情况下开始训练，每隔一段时间查看一下训练的情况
5. 注册多个免费的谷歌账号交替使用

### 四、Colab项目组织

在正式进入实例演示之前，最后简单介绍一下在Colab上组织项目的方法

### 加载数据集

深度学习中，数据集一般由超大量的数据组成，如何在Colab上快速加载数据集？  
1\. 将整个数据集从本地上传到实例空间

理论可行但实际不可取。经过作者实测，无论是上传压缩包还是文件夹，这种方法都是非常的慢，对于较大的数据集完全不具备可操作性。

2\. 将整个数据集上传到谷歌硬盘，挂载谷歌云盘的之后直接读取云盘内的数据集

理论可行但风险较大。根据谷歌的说明，Colab读取云盘的I/O次数也是有限制的，太琐碎的I/O会导致出现“配额限制”。如果数据集包含大量的子文件夹，也很容易出现挂载错误。

3\. 将数据集以压缩包形式上传到谷歌云盘，然后解压到Colab实例空间

实测可行。挂载云盘不消耗时间，解压所需的时间远远小于上传数据集的时间

此外，由于实例空间会定期释放，因此模型训练完成后的日志也应该存放在谷歌云盘上。综上所述，谷歌云盘是使用Colab必不可少的一环，由于免费的云盘只有15个G，因此个人建议至少拓展到基本版。

### 运行Github项目

Colab的基本运行单位是Jupyter Notebook，如何在一个notebook上运行一个复杂的Github项目呢？

首先创建多个笔记本来对应多个py模块是肯定不行的，因为不同的笔记本会对应不同实例空间，而同一个项目的不同模块应放在同一个实例空间中。为解决这个问题，可以考虑以下几种方法。  
1\. 克隆git仓库到实例空间或云盘，通过脚本的方式直接执行项目的主程序

\# 克隆仓库到/content/my-repo目录下!git clone [https://github.com/my-github-username/my-git-repo.git](https://link.zhihu.com/?target=https%3A//github.com/my-github-username/my-git-repo.git "https://github.com/my-github-username/my-git-repo.git") %cd my-git-repo!./train.py --logdir /my/log/path --data\_root /my/data/root --resume

2\. 克隆git仓库到实例空间或云盘，把主程序中的代码用函数封装，然后在notebook中调用这些函数

from train import my\_training\_method my\_training\_method(arg1, arg2,...)

由于笔记本默认的路径是"/content"，因此可能需要修改系统路径后才能直接导入

import sys sys.path.append('/content/my-git-repo') # 把git仓库的目录添加到系统目录

3\. 克隆git仓库到实例空间或云盘，把原来的主程序模块直接复制到笔记本中

类似于第二种方法，需要将git仓库路径添加到系统路径，否则会找不到导入的模块

### 如何处理简单项目？

如果只有几个轻量的模块，也不打算使用git进行版本管理，则直接上传到实例空间即可

### 五、实例演示

下面以我在这个学期完成的项目为例，向大家完整展示Colab的使用过程。PS：真不是推销自己的项目，而是目前我只做了这一个项目(ಥ\_ಥ)

云盘链接： [https://drive.google.com/drive/folders/1-4z\_Y38jMmIZNe5sNzbF1Le1Kv\_ugFcd?usp=sharing](https://link.zhihu.com/?target=https%3A//drive.google.com/drive/folders/1-4z_Y38jMmIZNe5sNzbF1Le1Kv_ugFcd%3Fusp%3Dsharing "https://drive.google.com/drive/folders/1-4z_Y38jMmIZNe5sNzbF1Le1Kv_ugFcd?usp=sharing")

点击以后就可以在谷歌云盘的“与我共享”看到这个文件夹"zhihu\_colab"，将这个文件夹的快捷方式添加到自己的云盘即可（右键文件夹“将快捷方式添加到云盘”，选择“我的云端硬盘”）

文件夹"zhihu\_colab"中包含了数据集"ROD-synROD.tar"和代码"mldl\_project"（以及这部分我写的notebook）

首先加载自己的谷歌云盘

```typescript
from google.colab import drive 

drive.mount('/content/drive')
```

加载成功以后（可以点一下刷新按钮）就可以看到云盘在实例空间中出现了

谷歌云盘默认的加载路径是"/content/drive/MyDrive"

在当前目录下("/content")创建一个叫datasets的文件夹，并将"zhihu\_colab"中的数据集解压到这个文件夹

```cobol
!mkdir /content/datasets 

!tar -xvf "/content/drive/MyDrive/zhihu_colab/ROD-synROD.tar" -C "/content/datasets"
```

查看一下自己分到的GPU是什么，具体的信息很长，只要看中间显卡部分就行了。

```cobol
gpu_info = !nvidia-smi 

gpu_info = '\n'.join(gpu_info) 

if gpu_info.find('failed') >= 0: 

    print('Not connected to a GPU') 

else: 

    print(gpu_info)
```

![](https://i-blog.csdnimg.cn/blog_migrate/0dbd826c4fd44daafdfdc28232088a0b.png)

哇哦，我们作为高贵的Pro用户果然分到了最好的P100 。去网上一查这个显卡买7000多欧，折合人民币好几万。

查看一下帮助文档（主程序是train.py）

!python3 /content/drive/MyDrive/zhihu\_colab/mldl\_project/code/train\_eval.py -h

最后就是训练模型了（大家不需要理解这个项目在干什么，只是给大家做个示范）

```cobol
!python3 /content/drive/MyDrive/zhihu_colab/mldl_project/code/train_eval.py \ 

--data_root /content/datasets/ROD-synROD \ 

--logdir /content/drive/MyDrive/ \ --

resume \ 

| tee /content/drive/MyDrive/synRODtoROD.txt -a
```

![](https://i-blog.csdnimg.cn/blog_migrate/1b2484919ca2b9795e3a31dc228f4309.png)

\--data\_root 用于指定数据集的根目录

\--logdir 用于指定保持模型日志(checkpoint + tensorboard)的路径，注意一定要保存到云盘里

\--resume 表示如果有checkpoint就加载checkpoint

| 是表示流式输入输出（前一个命令的输出作为后一个命令的输入）

tee 命令用于将输出保存到文件同时也输出到屏幕，-a表示add模式（如果文件已存在会添加而不是覆盖）

可以看到训练一个epoch大概是17分钟左右（显示训练进度是因为代码里用了tqdm模块），如果是高RAM模式的话大概只要一半的时间左右。

这就是在Colab上模型训练的所有过程了，总的来说还是非常的简单的，不需要进行任何额外的配置。

### 六、Colab Pro / Pro+

因为担心项目完不成，我买了好几个Colab Pro和Colab Pro+的账号，在经过了一周的使用后，和大家分享一下使用感受。

由于谷歌只给出了不同会员的大致功能区别而没有给出详细的区别，我把我个人测试的结果放在下方供大家参考（三种配置下的标准RAM没有区别，都是12GB）。

### RAM-磁盘

|  | 高RAM | 磁盘 | 后台运行 |
| --- | --- | --- | --- |
| 免费 | ❌ | 66GB? | ❌ |
| Pro | 25GB | 166GB | ❌ |
| Pro+ | 52GB | 225GB | ✅ |

坏了，把所有账号都升级成PRO以后，现在反而不知道免费版的磁盘大小是多少了

### GPU模式下会话数量

|  | 标准RAM | 高RAM | 后台运行 |
| --- | --- | --- | --- |
| 免费 | 1 | ❌ | ❌ |
| Pro | 2 | 1 | ❌ |
| Pro+ | 3 | 3 | 2（无论是否高RAM） |

高RAM会话的计算速度大致是标准RAM会话的两倍

### 使用Pro/Pro+的个人感受

免费版没有高RAM，且需要频繁地互动否则会掉线，我用了很少的时间就升级了，因此个人的体验不是很多  
Pro增加了一个高RAM会话和标准会话，和免费版比相当于算力翻了4倍，效率有了飞跃式提升，而且最大连接时长到了24小时，最大闲置时长也增加了不少，磁盘空间的拓展倒是基本用不上  
Pro+增加到了3个高RAM会话和3个标准会话，在Pro基础上又翻了2.5倍，相当于免费版算力的9倍，Pro+的52GB的高RAM和Pro的25GB的高RAM相比也略有提升（10分钟的epoch能快2分钟左右）。此外还多了后台运行功能，但是在后台运行的笔记本最多只能存在2个，且笔记本在后台的运行并没有持续24小时（这一点有待测试，可能只是我网络不佳）。  
今天测试时，Pro+只能开启一个后台会话。

![](https://i-blog.csdnimg.cn/blog_migrate/42e59e56dc816dad203b72fcd703707e.png)

即使是Pro/Pro+也要受到连接时长的限制，如果多个会话从早上开始不间断地进行训练，一般到深夜就会提示Colab使用限额，这时需要等到第二天下午1点左右才会重置。Pro+比起Pro贵了4倍但是算力却只提升了2.5倍左右，也就是说如果不怕麻烦，也不依赖后台功能的话多买几个Pro性价比是高于Pro+的。如果不想在多个账号间来回切换或者比较喜欢能够在关闭浏览器情况下后台运行的话，Pro+也可以考虑。

最后说几个支付相关的细节，首先付款的话只要在谷歌账户绑定银行卡就行，留学生肯定有外国银行卡比如MasterCard等等就不说了，如果是中国卡的话必须要有Visa才能支付。其次就是如果买了Pro之后再买Pro+，中间的差价也会退还，不用担心重复购买的问题。如果没有Visa的话推荐某宝购买，亲测可用，推荐搜店铺 [遇上野鱼工作室](https://link.zhihu.com/?target=https%3A//s.tb.cn/c.0vQUrD "遇上野鱼工作室") 。

综上，我个人认为性价比较高的组合是：每月2欧的谷歌云盘 + 每月9欧的ColabPro。

### 七、补充内容

### 如何让代码有“断点续传”的能力？

虽然这个话题超出了本文的范围，但是由于在Colab训练模型时代码必须要有可恢复性(resumption)，因此这里也简单提一下。我把教授写的两个分别实现保存和加载checkpoint的函数贴在下方，给大家作参考。

在主程序train.py正式开始训练前，添加下面的语句：

```python
def save_checkpoint(path: Text,

                    epoch: int,

                    modules: Union[nn.Module, Sequence[nn.Module]],

                    optimizers: Union[opt.Optimizer, Sequence[opt.Optimizer]],

                    safe_replacement: bool = True):

    """

    Save a checkpoint of the current state of the training, so it can be resumed.

    This checkpointing function assumes that there are no learning rate schedulers or gradient scalers for automatic

    mixed precision.

    :param path:

        Path for your checkpoint file

    :param epoch:

        Current (completed) epoch

    :param modules:

        nn.Module containing the model or a list of nn.Module objects

    :param optimizers:

        Optimizer or list of optimizers

    :param safe_replacement:

        Keep old checkpoint until the new one has been completed

    :return:

    """

 

    # This function can be called both as

    # save_checkpoint('/my/checkpoint/path.pth', my_epoch, my_module, my_opt)

    # or

    # save_checkpoint('/my/checkpoint/path.pth', my_epoch, [my_module1, my_module2], [my_opt1, my_opt2])

    if isinstance(modules, nn.Module):

        modules = [modules]

    if isinstance(optimizers, opt.Optimizer):

        optimizers = [optimizers]

 

    # Data dictionary to be saved

    data = {

        'epoch': epoch,

        # Current time (UNIX timestamp)

        'time': time.time(),

        # State dict for all the modules

        'modules': [m.state_dict() for m in modules],

        # State dict for all the optimizers

        'optimizers': [o.state_dict() for o in optimizers]

    }

 

    # Safe replacement of old checkpoint

    temp_file = None

    if os.path.exists(path) and safe_replacement:

        # There's an old checkpoint. Rename it!

        temp_file = path + '.old'

        os.rename(path, temp_file)

 

    # Save the new checkpoint

    with open(path, 'wb') as fp:

        torch.save(data, fp)

        # Flush and sync the FS

        fp.flush()

        os.fsync(fp.fileno())

 

    # Remove the old checkpoint

    if temp_file is not None:

        os.unlink(path + '.old')

 

 

def load_checkpoint(path: Text,

                    default_epoch: int,

                    modules: Union[nn.Module, Sequence[nn.Module]],

                    optimizers: Union[opt.Optimizer, Sequence[opt.Optimizer]],

                    verbose: bool = True):

    """

    Try to load a checkpoint to resume the training.

    :param path:

        Path for your checkpoint file

    :param default_epoch:

        Initial value for "epoch" (in case there are not snapshots)

    :param modules:

        nn.Module containing the model or a list of nn.Module objects. They are assumed to stay on the same device

    :param optimizers:

        Optimizer or list of optimizers

    :param verbose:

        Verbose mode

    :return:

        Next epoch

    """

    if isinstance(modules, nn.Module):

        modules = [modules]

    if isinstance(optimizers, opt.Optimizer):

        optimizers = [optimizers]

 

    # If there's a checkpoint

    if os.path.exists(path):

        # Load data

        data = torch.load(path, map_location=next(modules[0].parameters()).device)

 

        # Inform the user that we are loading the checkpoint

        if verbose:

            print(f"Loaded checkpoint saved at {datetime.fromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')}. "

                  f"Resuming from epoch {data['epoch']}")

 

        # Load state for all the modules

        for i, m in enumerate(modules):

            modules[i].load_state_dict(data['modules'][i])

 

        # Load state for all the optimizers

        for i, o in enumerate(optimizers):

            optimizers[i].load_state_dict(data['optimizers'][i])

 

        # Next epoch

        return data['epoch'] + 1

    else:

        return default_epoch
```

在主程序train.py正式开始训练前，添加下面的语句：

```cobol
if args.resume: # args.resume是命令行输入的参数，用于指示要不要加载上次训练的结果 

    first_epoch = load_checkpoint(checkpoint_path, first_epoch, net_list, optims_list)
```

在每个epoch训练结束后，保存checkpoint：

```cobol
# Save checkpoint 

save_checkpoint(checkpoint_path, epoch, net_list, optims_list)
```

net\_list是需要保存的网络列表，optims\_list是需要保存的优化器列表  
这里没有记录scheduler的列表，如果代码里用到了scheduler，那也要保存scheduler的列表

### 如果分到了Tesla T4怎么办？

开启了Pro/Pro+会员，大概率会分到最好的显卡P100，如果不幸分到了Tesla T4而且马上要进行高强度的训练，那只能选择反复地刷显卡。具体方法为断开运行时后再连接，不断重复直到刷出P100为止。我常用的玄学方案是先切到标准RAM刷几次，刷出P100后切回高RAM。  
这个过程可能很无聊，但是因为P100的训练速度是Tesla T4的2倍多，多花三十分钟刷一个P100出来可能会节省之后的十几个小时（实际上要不了三十分钟，一般五六分钟就刷出来了）。

### 结语：一不留神写了一万多字了！希望这个超详细的Colab教程能对大家有所帮助，大家要是发现了什么新的技巧欢迎在评论区留言～

实付 元

[使用余额支付](https://blog.csdn.net/javastart/article/details/)

点击重新获取

扫码支付

钱包余额 0

抵扣说明：

1.余额是钱包充值的虚拟货币，按照1:1的比例进行支付金额的抵扣。  
2.余额无法直接购买下载，可以购买VIP、付费专栏及课程。

[余额充值](https://i.csdn.net/#/wallet/balance/recharge)

举报

![程序员都在用的中文IT技术交流社区](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_app.png)

程序员都在用的中文IT技术交流社区

![专业的中文 IT 技术社区，与千万技术人共成长](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_wechat.png)

专业的中文 IT 技术社区，与千万技术人共成长

![关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！](https://g.csdnimg.cn/side-toolbar/3.6/images/qr_video.png)

关注【CSDN】视频号，行业资讯、技术分享精彩不断，直播好礼送不停！

客服 返回顶部