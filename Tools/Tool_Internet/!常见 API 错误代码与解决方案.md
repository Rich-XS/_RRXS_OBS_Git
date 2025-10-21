## 🛠️ OpenRouter 常见 API 错误代码与解决方案
[!!!VSC CCA&CCR&CPG 三引擎 Master](!!!VSC%20CCA&CCR&CPG%20三引擎%20Master.md)
[!!AnyRouter.Top MasterFile](!!AnyRouter.Top%20MasterFile.md)
[!!RRXS_AWS-EC2_Gemini Balance 轮询 AI善人](!!RRXS_AWS-EC2_Gemini%20Balance%20轮询%20AI善人.md)


OpenRouter API 遵循标准 HTTP 错误代码。以下是 CCR/Agent 工作流中最常遇到的 10 种错误（按常见程度排序，但会根据用户配置和使用频率有所波动）。

| 排名      | HTTP 代码     | 错误类型                  | 典型错误信息/表现                                          | 根本原因                                                                                     | 解决方案（高到低）                                                                                                 |
| ------- | ----------- | --------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **1.**  | **404**     | **模型/端点不匹配**          | `"No ==endpoints== found that support tool use."`  | Agent 要求的**特定功能**（如工具调用、Vision）在当前配置模型上不可用。                                              | 1. **修改 `config.json`**，切换到支持工具调用的模型（如 Haiku/Gemini Flash/Deepseek Chat V3.1:free）。 2. 验证模型 ID 是否拼写正确。    |
| **2.**  | **429**     | **速率限制 (Rate Limit)** | `"Too Many ==Requests=="`, `"Rate limit exceeded"` | **OpenRouter/供应商限额**：您在短时间内发送了太多请求，或免费额度已用尽（如 Qwen/Deepseek 的免费层级）。                      | 1. **等待 30-60 秒后重试。** 2. 检查 `config.json`，将高频使用的路由（`默认`/`思考`）切换到**付费/更稳定**的模型（如 Haiku/Gemini Flash Lite）。 |
| **3.**  | **500**     | **内部服务错误**            | `"Internal ==Server== Error"`                      | **供应商宕机**：模型提供商（如 Anthropic, Google）或 OpenRouter 本身服务暂时性故障。                              | 1. **立即重试**（通常可恢复）。 2. 检查 OpenRouter 状态页或切换到**其他模型供应商**（如从 Claude 换到 Gemini）。**==Key设了限制?==**             |
| **4.**  | **401**     | **授权失败**              | `"Invalid API Key"`, `"Authentication Error"`      | **API Key 错误**：您的 OpenRouter API Key 无效、过期或权限不足。                                         | 1. **检查 Key** 是否完整。 2. 在 OpenRouter 网站上**重新生成 API Key**。                                                  |
| **5.**  | **400**     | **输入/模型上下文超限**        | `"Context length exceeded"`, `"Prompt too long"`   | **模型 Token 限长**：您的输入提示词和上下文超过了模型设置的最大上下文长度（例如，超过 Haiku 的 200K 或 GLM 4.5 Air 的 32K/131K）。 | 1. **缩短提示词**或将任务分解。 2. 切换到 **`longContext`** 路由模型（如 Gemini Flash Lite，160K）。                              |
| **6.**  | **502/504** | **网关超时/连接问题**         | `"Bad Gateway"`, `"Gateway Timeout"`               | **网络不稳定**：VPN/代理连接中断或延迟过高，导致 OpenRouter 在响应之前断开连接 [cite: 2025-10-03]。                    | 1. **检查您的 VPN/代理** 稳定性。 2. 检查本地网络连接。                                                                      |
| **7.**  | **402**     | **支付失败**              | `"Payment Required"`, `"Insufficient Funds"`       | **付费模型余额不足**：您配置了付费模型（如 GLM 4.6），但 OpenRouter 账户没有余额或扣款失败。                               | 1. **充值 OpenRouter 余额。** 2. 将路由切换回 **`free`** 免费模型。                                                       |
| **8.**  | **400**     | **参数错误**              | `"Invalid parameter 'messages'"`                   | **Agent 输出格式错误**：CCR Agent 在构建请求时，参数（如 `temperature` 或 `messages` 结构）不符合 OpenRouter 的规范。 | **冷启动 CCR 进程**，确保环境纯净。                                                                                    |
| **9.**  | **503**     | **服务不可用**             | `"Service Unavailable"`                            | **模型暂时离线/维护**：供应商正在维护或临时下线了该模型。                                                          | **切换模型**，等待几小时后重试。                                                                                        |
| **10.** | **无代码**     | **`No Body` / 连接断开**  | 终端无响应，或 NodeJS 抛出 `read ECONNRESET`                | **网络突发断开**：通常是网络连接或 VPN 突然中断。                                                            | 立即检查网络/VPN，然后**冷启动 CCR**。                                                                                 |
|         | 403         | login                 |                                                    | (haiku 3.0 openrouter 上有限制了?)                                                            |                                                                                                           |

导出到 Google 表格

---

## 💡 查询 Token 限制的方法

### 1. 访问 OpenRouter 模型页面

这是最直接、最准确的方式：

- **步骤：** 访问 OpenRouter 网站的 **Models** 页面。
    
- **查找：** 在模型列表中，您可以直接看到每个模型的 **`Context (tokens)`** 字段，这就是它的最大上下文长度（Token 限制）。
    
    - 例如，GLM 4.5 Air (free) 的限制是 131,072。
        

### 2. 通过 API 接口查询

如果您需要用代码查询，可以使用 OpenRouter 的 API：

- **API EndPoint：** `GET /api/v1/models`
    
- **结果：** 返回的 JSON 结构中包含每个模型的 `id` 和 `context_length` 字段。
    

### 3. CCR 配置界面

您在 CCR 路由设置中，**`长上下文`** 模型旁边也可以看到一个 **`上下文阈值`** 字段。这个阈值通常设置为略低于模型最大的上下文限制，以便在代码执行中留出安全空间。