
[!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)

## 🔎 差异分析：WSL2 vs. Windows (PS)

| 特征                                | WSL Ubuntu (Ping/Curl)                           | Windows PowerShell (Node.js/JS)                                                                                  | 结论                             |
| --------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **网络环境**                          | 独立于 Windows 的虚拟网络接口，**不继承** Windows 的 VPN 或代理设置。 | 直接使用 Windows 主机的网络栈，**继承** 所有系统级代理和证书。                                                                           | **网络环境完全不同**                   |
| **测试方式**                          | **Ping**：ICMP 协议，只测试 IP 级连通性。                    | **Node.js/HTTP 客户端**：HTTP/HTTPS 协议，测试应用层连通性、证书和状态码。                                                              | **测试层次和准确性不同**                 |
| **`anyrouter.top`**               | **0% 丢包 (成功)**：WSL2 可以 ping 到 IP。                | **`✗ write EPROTO... handshake failure` (失败)**：Windows 的 Node.js 客户端在尝试 SSL 握手时失败，可能是 Node.js 版本、证书或中间代理干扰了 SSL。 | **WSL2 网络更“干净”**               |
| **`pmpjfbhq.cn-nb1.rainapp.top`** | **100% 丢包 (失败)**：WSL2 无法 ping 通 IP。              | **✓ 114ms (成功)**：Windows 主机可以访问。                                                                                 | **Windows 主机使用了你未知的系统级代理/加速！** |
| **`7a61fbe1b5f3.d93a09b6.top/`**  | 33% 丢包 (不稳定)                                     | **✓ 6341ms (成功)**：能连接，但延迟极高 (6秒!)。                                                                               | **该地址不稳定且慢。**                  |
### 差异解读：

1. **WSL2 是“裸奔”的：** `ping google.com` 失败证明 WSL2 没有 VPN 保护。它能连通 `anyrouter.top`（0% 丢包）是因为该 IP 位于 Cloudflare，可能在中国有边缘节点，能直连。
    
2. **Windows 是“全副武装”的：** Windows 主机能够成功连接 **`pmpjfbhq.cn-nb1.rainapp.top`**（WSL2 无法 ping 通的地址），并且延迟仅 114ms，这几乎 **100% 确定 Windows 正在使用一个系统级代理或加速工具** 来访问这个地址。

## 🎯 行动方案：选择最佳地址并配置 WSL2 代理

现在你有两条清晰的高效路径：

### 路径 A：优先使用 Windows 连通性最好的地址 (推荐)

既然 **`https://pmpjfbhq.cn-nb1.rainapp.top`** 在 Windows 下响应最快（**114ms**），我们应该把这个地址作为目标，然后**配置 WSL2 代理**来访问它。

1. **配置 `config.toml`：** 将 `~/.codex/config.toml` 中的 `base_url` 改为：
    
    Ini, TOML
    
    ```
    base_url = "https://pmpjfbhq.cn-nb1.rainapp.top/v1"
    ```
    
2. **设置 WSL2 代理环境变量：** 这是最关键的一步。在 **WSL Ubuntu 终端** 中，重复以下命令：
    
    Bash
    
    ```
    # 查找 Windows 主机 IP
    export WINDOWS_HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
    
    # 设置代理端口 (请务必确认你的 Windows 代理端口号！例如：7890 或 10809)
    # 我这里假设端口是 7890
    export http_proxy="http://$WINDOWS_HOST_IP:7890"
    export https_proxy="http://$WINDOWS_HOST_IP:7890"
    ```
    
3. **启动 Codex 测试：**
    
    Bash
    
    ```
    codex
    ```
    

### 路径 B：使用 WSL2 可直连的地址 (备份)

如果路径 A 失败，我们回退到 **`anyrouter.top`**：

1. 将 `~/.codex/config.toml` 中的 `base_url` 改为 `https://anyrouter.top/v1`。
    
2. **移除代理环境变量：** `unset http_proxy; unset https_proxy`
    
3. 启动 Codex 测试。
    

**请先执行 Path A。** 解决 WSL2 的代理问题（即使是临时的环境变量）是你在中国使用 Codex 的一个必须步骤。请确认你的 Windows 代理端口号并进行测试！