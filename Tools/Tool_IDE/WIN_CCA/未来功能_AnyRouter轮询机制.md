# 🔄 功能需求：AnyRouter多账号轮询机制

**优先级**: 非紧急 (no-urgent)
**参考模型**: Gemini-Balance轮询系统
**状态**: 需求记录 ⏳

---

## 📋 需求描述

实现类似Gemini-Balance的多账号智能轮询机制，用于AnyRouter账号管理。

---

## 🎯 核心功能设想

### 1. 智能账号轮询
```
请求到来时自动选择：
├─ 余额最多的账号（优先使用）
├─ 最少使用的账号（负载均衡）
├─ 上次使用时间最早的账号
└─ 跳过余额不足的账号
```

### 2. 实时余额追踪
- 每次使用后更新账号余额
- 预估单次请求消耗金额
- 自动标记余额不足账号
- 触发余额预警通知

### 3. 自动故障转移
```
账号1请求失败 → 自动切换到账号2
账号2请求失败 → 自动切换到账号3
...
所有账号失败 → 触发告警
```

### 4. 使用统计分析
- 每个账号的调用次数
- 每个账号的消耗金额
- 高峰时段使用分布
- 账号效率评分

---

## 🏗️ 技术实现方案

### 方案A：本地轮询服务
```python
class AnyRouterBalancer:
    def __init__(self, accounts):
        self.accounts = accounts
        self.usage_stats = {}

    def get_best_account(self):
        """选择最佳账号"""
        # 过滤余额充足的账号
        available = [a for a in self.accounts if a['balance'] > 1.0]
        # 选择余额最多的
        return max(available, key=lambda x: x['balance'])

    def update_usage(self, account_name, cost):
        """更新使用统计"""
        self.accounts[account_name]['balance'] -= cost
        self.usage_stats[account_name] += 1
```

### 方案B：API代理服务
```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/api/anyrouter', methods=['POST'])
def proxy_request():
    # 选择最佳账号
    account = balancer.get_best_account()

    # 转发请求到AnyRouter
    response = forward_to_anyrouter(account, request.data)

    # 更新账号状态
    balancer.update_usage(account['name'], estimated_cost)

    return response
```

### 方案C：中间件集成
```python
# 作为中间件集成到现有系统
class AnyRouterMiddleware:
    def process_request(self, request):
        account = self.select_account()
        request.META['ANYROUTER_ACCOUNT'] = account
        return request
```

---

## 📊 与Gemini-Balance的对比

| 功能 | Gemini-Balance | AnyRouter轮询（拟） |
|-----|---------------|------------------|
| 多账号管理 | ✅ | ✅ |
| 自动轮询 | ✅ | ✅ |
| 余额追踪 | ✅ | ✅ |
| 故障转移 | ✅ | ✅ |
| 使用统计 | ✅ | ✅ |
| 定时刷新 | ❌ | ✅ (已实现) |
| 余额监控 | ❌ | ✅ (已实现) |

**优势**: AnyRouter系统在定时刷新和余额监控方面已有基础，添加轮询机制可形成完整闭环。

---

## 🔧 实现步骤（未来）

### 阶段1: 基础架构（1-2天）
1. ✅ 多账号配置管理（已完成）
2. ⏳ 轮询选择算法
3. ⏳ 余额实时追踪
4. ⏳ 使用日志记录

### 阶段2: 智能调度（2-3天）
1. ⏳ 负载均衡算法
2. ⏳ 故障自动转移
3. ⏳ 预测性余额管理
4. ⏳ 性能优化

### 阶段3: 监控告警（1-2天）
1. ⏳ 实时监控面板
2. ⏳ 余额预警系统
3. ⏳ 使用报告生成
4. ⏳ 异常告警通知

---

## 💡 应用场景

### 场景1: API代理服务
```
外部应用 → AnyRouter轮询器 → 多个AnyRouter账号
         ↓
      自动选择最佳账号
      余额充足 + 负载最低
```

### 场景2: 批量请求处理
```
100个请求到来
├─ 账号1处理 30个（余额最多）
├─ 账号2处理 30个（余额次之）
├─ 账号3处理 25个（余额较少）
└─ 账号4处理 15个（余额最少）
```

### 场景3: 高可用保障
```
主账号故障
├─ 立即切换到备用账号
├─ 记录故障信息
└─ 继续提供服务（零中断）
```

---

## 📈 预期收益

### 效率提升
- 🚀 请求响应速度提升（自动选择最快账号）
- 💰 成本优化（均衡使用避免单账号耗尽）
- 🛡️ 可用性提升（多账号冗余）

### 管理优化
- 📊 清晰的使用统计
- ⚡ 自动化程度提高
- 🎯 精准的余额预测

---

## 🔗 与现有系统的集成

### 现有系统组件
1. ✅ `refresh_with_monitoring.py` - 定时刷新
2. ✅ `usage_checker.py` - 余额查询
3. ⏳ `anyrouter_balancer.py` - 轮询器（待开发）

### 集成方案
```python
# 统一管理类
class AnyRouterManager:
    def __init__(self):
        self.balancer = AnyRouterBalancer()      # 轮询器
        self.monitor = UsageMonitor()            # 监控器（已有）
        self.refresher = AutoRefresher()         # 刷新器（已有）

    def handle_request(self, request_data):
        # 选择账号
        account = self.balancer.get_best_account()

        # 执行请求
        response = self.execute_with_account(account, request_data)

        # 更新监控
        self.monitor.record_usage(account, response)

        return response
```

---

## ⚠️ 技术挑战

### 挑战1: 实时余额同步
- **问题**: 多进程/多线程环境下余额一致性
- **方案**: 使用Redis或SQLite共享状态

### 挑战2: 并发控制
- **问题**: 同时有多个请求时的账号分配
- **方案**: 引入分布式锁机制

### 挑战3: 准确性估算
- **问题**: 每次请求的实际消耗难以精确预测
- **方案**: 建立消耗模型，定期校准

---

## 📝 开发计划（待定）

### 近期（不紧急）
- 记录需求，等待合适时机
- 收集更多使用场景数据
- 评估开发优先级

### 中期（如需要）
- 设计详细技术方案
- 开发基础原型
- 小规模测试验证

### 长期（可选）
- 完整功能实现
- 生产环境部署
- 持续优化迭代

---

## 🎓 参考资料

### 类似项目
- Gemini-Balance 轮询系统
- OpenAI API Key轮询
- 多CDN智能调度

### 技术栈
- Python asyncio（异步处理）
- Redis（状态共享）
- Flask/FastAPI（API服务）
- APScheduler（定时任务）

---

**状态**: 需求已记录 ✅
**下一步**: 等待明确的开发时间点
**联系**: 随时可以继续讨论此功能

---

*记录时间: 2025-01-XX*
*文档版本: V1.0*
*需求编号: FR-001*
