# X 账号关注操作指南

## 当前问题
bird CLI 工具无法自动读取 Chrome 浏览器的 Twitter/X cookies，导致无法执行关注操作。

## 手动关注步骤
1. **打开 Chrome 浏览器**：确保已登录到您的 X 账号
2. **访问以下账号并手动点击关注**：

### 财经领域权威账号
- https://x.com/LizAnnSonders
- https://x.com/paulkrugman  
- https://x.com/elerianm
- https://x.com/morganhousel
- https://x.com/RayDalio
- https://x.com/barronsonline
- https://x.com/matt_levine
- https://x.com/michaelbatnick
- https://x.com/saxena_puru
- https://x.com/AswathDamodaran

### 国际新闻权威账号
- https://x.com/nytimes
- https://x.com/CNN
- https://x.com/BBCWorld
- https://x.com/Reuters
- https://x.com/guardian
- https://x.com/washingtonpost
- https://x.com/WSJ
- https://x.com/FT

## 技术解决方案（待实施）
1. **配置 bird CLI 的 Chrome Profile 支持**
   - 需要正确设置 Chrome 用户数据目录路径
   - 可能需要手动指定 cookies 文件位置

2. **使用官方 Twitter API**
   - 申请 Twitter API v2 访问权限
   - 实现程序化关注功能
   - 需要处理 API 速率限制和认证

3. **浏览器自动化方案**
   - 使用 Playwright 或 Puppeteer 自动化 Chrome
   - 模拟用户点击关注按钮
   - 需要处理反自动化检测

## 临时监控方案
在完成手动关注之前，可以通过以下方式监控这些账号：
- 使用 `bird read <username>` 命令查看公开推文
- 设置 RSSHub 订阅这些账号的推文
- 在全球新闻日报脚本中直接调用这些账号的推文获取功能

## 验证关注状态
关注完成后，可以使用以下命令验证：
```bash
bird following --limit 50
```

这将显示您当前关注的账号列表，确认上述账号是否已成功关注。