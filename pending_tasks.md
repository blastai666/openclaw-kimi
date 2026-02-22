# 未完成任务清单

## X 账号关注任务
- **状态**: 需要手动完成
- **原因**: bird CLI 工具无法自动读取 Chrome 浏览器的 X/Twitter cookies
- **待执行**: 手动关注 18 个可靠 X 账号（详见 follow_instructions.md）

## 技术优化任务
- **配置 bird CLI Chrome Profile 支持**
  - 需要正确设置 Chrome 用户数据目录路径
  - 测试 cookies 文件读取权限
- **申请 Twitter API v2 权限**
  - 实现程序化关注功能
  - 处理 API 速率限制和认证
- **浏览器自动化方案**
  - 使用 Playwright/Puppeteer 自动化 Chrome
  - 模拟用户点击关注按钮
  - 处理反自动化检测

## 持续搜索新新闻来源
- **AI 交互平台监控**
  - Hacker News 新兴账号发现
  - Reddit r/worldnews, r/finance 可靠信息源识别
  - GitHub 相关项目和工具发现
- **交叉验证机制**
  - 建立多平台信息验证流程
  - 开发可靠性评分系统
- **中文 X 账号研究**
  - 识别中文财经和新闻领域的可靠 X 账号
  - 验证账号专业性和内容质量

## 全球新闻日报系统优化
- **集成新 X 账号到监控脚本**
  - 更新 global-news-daily.py 脚本
  - 添加 X 账号推文获取功能
- **实时警报系统**
  - 对关键账号的重要发布设置即时通知
  - 开发关键词和突发新闻警报
- **性能优化**
  - 修复 CNBC RSS 源解析错误
  - 优化多源并发获取效率

## 文件位置
- 可靠 X 账号研究: `~/Desktop/openclaw-kimi/reliable_x_accounts.md`
- 关注操作指南: `~/Desktop/openclaw-kimi/follow_instructions.md`
- 最新新闻测试: `~/Desktop/openclaw-kimi/latest_news_test.md`
- GitHub 仓库: `https://github.com/blastai666/openclaw-kimi`

## 优先级建议
1. **高优先级**: 手动完成 X 账号关注（断电前可快速完成）
2. **中优先级**: 修复 CNBC RSS 源和集成 X 账号到新闻脚本
3. **低优先级**: 技术优化和自动化方案开发

---
最后更新: 2026-02-21 20:20