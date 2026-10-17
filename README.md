# 素里中国福音教会 (SCEC) 官方网站 (GitHub Pages 版)

本项目为 **[scecchinese.com](https://scecchinese.com)**（素里中国福音教会 Surrey Christian Evangelical Church）官方网站工程库。网站基于现代静态 Web 标准重构，设计风格契合教会原形象（主题紫色 `#8e3be2`），针对 **GitHub Pages** 提供开箱即用的静态托管支持。

---

## 🌐 网站页面架构

* [`index.html`](file:///home/harry/git/scec-site/index.html) : 网站首页（2026年度经文、聚会时间表、活动剪影、教会异象、地图与留言表单）
* [`about.html`](file:///home/harry/git/scec-site/about.html) : 关于我们（建会历史、美南浸信会地方教会背景、各事工部架构）
* [`sunday-school.html`](file:///home/harry/git/scec-site/sunday-school.html) : 主日学教程（成人新生命/新生活/门徒之道教程，儿童主日学优质资源）
* [`bible-study.html`](file:///home/harry/git/scec-site/bible-study.html) : 圣经学习工具（旧约/新约圣经背景注释 PDF 下载、在线研经工具、灵命造就书库）
* [`youth-group.html`](file:///home/harry/git/scec-site/youth-group.html) : 青少年团契 Youth Group（聚会时间、英文崇拜、Instagram 及 Facebook 社媒）
* [`sisters-fellowship.html`](file:///home/harry/git/scec-site/sisters-fellowship.html) : 姐妹团契信息分享（每月团契动态、灵修讲座 PDF）
* [`worship.html`](file:///home/harry/git/scec-site/worship.html) : 诗歌敬拜（**内置 260 首诗歌目录带实时搜索筛选**，即点即播；诗班献诗录影）
* [`activities.html`](file:///home/harry/git/scec-site/activities.html) : 活动相册与视频（2019-2025 历年圣诞特别聚会、户外野餐崇拜、家庭夏令营回顾）
* [`contact.html`](file:///home/harry/git/scec-site/contact.html) : 联系我们（聚会地址、交通指引、Zoom 会议号、Google 地图定位与在线留言）
* [`styles.css`](file:///home/harry/git/scec-site/styles.css) : 现代响应式样式表
* [`main.js`](file:///home/harry/git/scec-site/main.js) : 移动端导航抽屉、诗歌实时搜索筛选与表单交互
* [`CNAME`](file:///home/harry/git/scec-site/CNAME) : 绑定自定义域名 `scecchinese.com`

---

## 🚀 部署上线指南 (GitHub Pages)

### 1. 推送代码至 GitHub
在 GitHub 上创建一个新的公开仓库（例如 `scec-site` 或 `scecchinese`），然后在本地终端运行：

```bash
cd /home/harry/git/scec-site

# 关联您的 GitHub 远端仓库 (请替换为您实际创建的仓库地址)
git remote add origin git@github.com:<YOUR_GITHUB_USERNAME>/<REPO_NAME>.git

# 推送代码至 main 分支
git push -u origin main
```

### 2. 启用 GitHub Pages 服务
1. 进入 GitHub 仓库页面，点击 **Settings (设置)** ➔ 左侧菜单 **Pages**。
2. 在 **Build and deployment** 下方的 **Source** 选择：`Deploy from a branch`。
3. **Branch** 选择：`main`，目录选择：`/(root)`，点击 **Save**。
4. 下方的 **Custom domain** 会自动识别到 `CNAME` 文件中的 `scecchinese.com`。
5. 勾选 **Enforce HTTPS**（几分钟后证书生成完毕即可勾选）。

### 3. 配置 DNS 解析记录 (Google DNS / GoDaddy)
前往您的 DNS 管理面板（Google Cloud DNS 或 GoDaddy DNS），添加以下记录：

#### ① 根域名 (Apex Domain: scecchinese.com) ➔ 指向 GitHub 4 个 IP (A 记录)：
* `185.199.108.153`
* `185.199.109.153`
* `185.199.110.153`
* `185.199.111.153`

#### ② 二级域名 (www.scecchinese.com) ➔ CNAME 记录：
* 主机名：`www`
* 记录值：`<YOUR_GITHUB_USERNAME>.github.io.`

#### ③ ⚠️ 邮箱记录 (MX Records) 保护：
* **切勿删除原有的 MX 记录与 SPF TXT 记录**，确保教会邮箱 `contactus@scecchinese.com` 正常无缝收发邮件。

---

## 📦 媒体文件存储与刷新策略

1. **当前阶段（GoDaddy 运行中）：**
   * 目前网页中的 260 首诗歌视频、聚会录像及书籍 PDF 均直接引用原 GoDaddy 服务器链接，**立刻上线即可正常播放与下载**。
2. **第二阶段（转存 Google Drive 后批量刷新）：**
   * 本仓库内置了 [`media_migration_manifest.csv`](file:///home/harry/git/scec-site/media_migration_manifest.csv)（833 个媒体文件完整归类清单）。
   * 当您把视频和 PDF 上传到 Google Drive 并设置为“知道链接者可查看”后，可以通过批量替换脚本一键将 URL 刷新为 Google Drive 或 YouTube 链接，并 `git push` 即时生效。
