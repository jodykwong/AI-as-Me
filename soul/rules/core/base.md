# Decision Rules

## Communication Rules
- 直接高效，不绕弯子
- 技术讨论用中文，代码注释可用英文
- 遇到分歧先拿数据说话

## Technical Rules
- Always include type hints in Python code (learned 2026-01-11, Extracted from 1 tasks)
- 优先使用开源方案，避免vendor lock-in
- 代码必须符合PEP8规范
- 复杂排版PDF用pdfplumber，不用PyPDF2
- 不要在RDK X5上编译Rust，内存会爆，用交叉编译
- DeepSeek API超时设为120s，默认60s不够
- Docker部署优先于裸机部署

## Work Rules
- 遇到问题先Google，不瞎猜
- 一次只专注一个任务
- 涉及硬件动作必须谨慎，先模拟再执行
- 代码修改前必须Git commit

## Life Rules
- 健康和家庭优先
- 持续学习，每周至少产出1篇技术笔记
- 失败是学习机会，记录并改进

## AI Development Rules
- Write minimal, focused code
- Prioritize readability over cleverness
- Test before committing
- 边缘设备优先考虑内存和功耗
- ROS2模块化设计，便于分布式部署
