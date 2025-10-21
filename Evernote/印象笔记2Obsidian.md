```bash
# 1. 安装（需 Python≥3.7）
pip install -U evernote-backup

# 2. 初始化并登录（国内版加 --backend china）
evernote-backup init-db --backend china
:rrxs@qq.com
:1234wert
# 按提示输入账号密码；若遇 2FA/登录失败，可先取「开发者 Token」再
evernote-backup init-db --backend china -t <Token>

# 3. 全量同步到本地
evernote-backup sync

# 4. 一次性导出全部笔记本为 .enex
evernote-backup export output_dir/
evernote-backup export D:/OneDrive_RRXS/OneDrive/_MyNote/

```

`output_dir` 里每个 `.enex` 对应一个笔记本，随后即可用 Yarle、Joplin 或 `evernote2md` 批量转 Markdown[](https://blog.csdn.net/qq_42973562/article/details/144538067)。