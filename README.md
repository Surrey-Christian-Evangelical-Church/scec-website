# 素里中国福音教会 (SCEC) 网站迁移工程库

本项目用于管理 **[scecchinese.com](https://scecchinese.com)** 从 GoDaddy (WordPress) 迁移至 **Google Sites** 与 **Google Drive** 的全部备份数据与迁移实施方案。

## 📁 目录结构

* [`static_site/`](file:///home/harry/git/scec-site/static_site/) : **网站重构原型与独立静态站**
  * [`index.html`](file:///home/harry/git/scec-site/static_site/index.html) : 现代语义化 HTML5 主页结构
  * [`styles.css`](file:///home/harry/git/scec-site/static_site/styles.css) : 现代响应式样式表（主题色 `#8e3be2`）
  * [`main.js`](file:///home/harry/git/scec-site/static_site/main.js) : 移动端导航抽屉及交互脚本
  * [`assets/`](file:///home/harry/git/scec-site/static_site/assets/) : Logo、Favicon 及高清活动图库
* [`content_backup/`](file:///home/harry/git/scec-site/content_backup/) : **原 WordPress 全站离线备份**
  * `pages/` : 12 个固定页面的 Markdown 及原始 HTML 备份
  * `posts/` : 9 篇历年大型聚会文章的 Markdown 及原始 HTML 备份
  * `documents/` : 7 部核心属灵书籍与主日学教程 PDF 文件
  * `branding/` : 网站高分辨率 Logo 及 Favicon 图标
* [`media_migration_manifest.csv`](file:///home/harry/git/scec-site/media_migration_manifest.csv) : **833 个多媒体资产完整清单**（包含 274 个 MP4 视频、528 张图片、7 个 PDF 等及对应 Google Drive 建议归属目录）
* [`backup_site.py`](file:///home/harry/git/scec-site/backup_site.py) : 自动备份 WordPress 全部页面与文章为 Markdown 与 HTML 的脚本
* [`generate_manifest.py`](file:///home/harry/git/scec-site/generate_manifest.py) : 扫描全站多媒体（含外部 FTP 目录）并生成迁移清单的脚本
* [完整迁移规划与技术执行方案 (Markdown 文档)](file:///home/harry/.gemini/antigravity/brain/a24fb83d-db4b-4084-9c15-f6201d4cf2c0/scecchinese_migration_plan.md)
