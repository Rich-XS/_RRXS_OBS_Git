## 💻 Ubuntu 常用命令一览

### 1. 文件与目录操作 (File & Directory Management)

|命令|作用|示例|
|---|---|---|
|**`ls`**|**列出**当前目录下的文件和目录。|`ls -l` (显示详细信息)|
|**`cd`**|**切换目录** (Change Directory)。|`cd Documents` (进入子目录); `cd ..` (返回上一级); `cd ~` (返回主目录)|
|**`pwd`**|**显示当前所在目录**的完整路径 (Print Working Directory)。|`pwd`|
|**`mkdir`**|**创建新目录**。|`mkdir new_folder`|
|**`touch`**|**创建新空文件**，或更新文件的时间戳。|`touch my_file.txt`|
|**`cp`**|**复制**文件或目录。|`cp file1.txt file2.txt` (复制文件); `cp -r dir1 dir2` (递归复制目录)|
|**`mv`**|**移动**或**重命名**文件/目录。|`mv old_name.txt new_name.txt` (重命名); `mv file.txt /path/to/new/location` (移动)|
|**`rm`**|**删除**文件。|`rm file.txt`|
|**`rm -r`**|**递归删除目录**及其所有内容 (请谨慎使用)。|`rm -r old_folder`|

导出到 Google 表格

---

### 2. 文件内容查看与编辑 (Viewing & Editing)

|命令|作用|示例|
|---|---|---|
|**`cat`**|**查看**整个文件的内容。|`cat my_file.txt`|
|**`less`**|分页查看文件内容，适合大文件。|`less logfile.log` (使用 空格键 翻页，q 退出)|
|**`head`**|仅查看文件**头部**的默认前10行。|`head my_file.txt`|
|**`tail`**|仅查看文件**尾部**的默认后10行。|`tail -f logfile.log` (实时跟踪文件末尾新增内容，用于查看日志)|
|**`grep`**|在文件中**搜索**匹配指定模式的文本行。|`grep "error" logfile.log`|
|**  <br>`VI` / `虚拟`**|强大的**文本编辑器**。|`vim file.txt` (编辑后保存退出请用 :wq )|

导出到 Google 表格

---

### 3. 系统与用户管理 (System & User Management)

|命令|作用|示例|
|---|---|---|
|**`sudo`**|以**超级用户权限**执行命令 (Super User Do)。|`sudo apt update`|
|**`whoami`**|**显示当前用户的名称**。|`whoami`|
|**`ps`**|**查看当前运行的进程**。|`ps aux` (查看所有进程的详细信息)|
|**`top`**|**实时查看**系统资源占用情况 (CPU、内存、进程等)。|`top` (q 退出)|
|**`kill`**|终止指定的进程。|`kill 1234` (1234为进程ID)|
|**`df`**|**查看磁盘空间使用情况** (Disk Free)。|`df -h` (以人类可读格式显示)|
|**`du`**|**查看目录或文件占用的空间大小** (Disk Usage)。|`du -sh /path/to/folder` (查看目录总大小)|

导出到 Google 表格

---

### 4. 软件管理 (Package Management)

在 Ubuntu 中，通常使用 **APT**（Advanced Package Tool）进行软件管理。

|命令|作用|示例|
|---|---|---|
|**`sudo apt update`**|**更新**本地软件源列表 (必要的第一步)。||
|**`sudo apt upgrade`**|**升级**所有已安装的软件包。||
|**`sudo apt install`**|**安装**新的软件包。|`sudo apt install net-tools`|
|**`sudo apt remove`**|**移除**已安装的软件包。|`sudo apt remove firefox`|
|**`sudo apt search`**|**搜索**软件仓库中的软件包。|`sudo apt search vlc`|

导出到 Google 表格

---

### 5. 网络连接 (Networking)

|命令|作用|示例|
|---|---|---|
|**`ping`**|**测试**网络连接状态和延迟。|`ping google.com` (Ctrl+C 停止)|
|**`ssh`**|**安全地远程登录**到另一台计算机。|`ssh user@192.168.1.100`|
|**`wget`**|**从网络下载**文件。|`wget https://example.com/file.zip`|
|**`curl`**|用于与服务器**交互**，获取或发送数据。|`curl https://ipinfo.io/ip` (查看公网 IP)|

导出到 Google 表格

### 💡 技巧与提示

- **万能帮助**：如果你不知道一个命令如何使用，可以输入 `man <命令名称>` 来查看其手册页 (Manual Page)。例如：`man ls`。
    
- **自动补全**：在输入命令或文件/目录名时，按 **Tab** 键可以自动补全，按两次 **Tab** 可以查看所有可能的选项。
    
- **历史命令**：按 ↑ (上箭头) 键可以查看并重复执行历史命令。