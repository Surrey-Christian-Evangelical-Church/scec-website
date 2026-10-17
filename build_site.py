#!/usr/bin/env python3
"""
SCEC Chinese Website Subpage Generator for GitHub Pages
Generates complete, responsive, styled subpages matching index.html,
with song page numbers preserved for church members' printed hymnals.
"""

import os
import json
import re

OUTPUT_DIR = "/home/harry/git/scec-site"

def get_header(active_nav=""):
    nav_links = [
        ("index.html", "首页", active_nav == "home"),
        ("about.html", "关于我们", active_nav == "about"),
        ("bible", "圣经学习", active_nav in ["sunday-school", "bible-study"], [
            ("sunday-school.html", "主日学教程"),
            ("bible-study.html", "圣经工具与典籍")
        ]),
        ("fellowship", "团契事工", active_nav in ["youth-group", "sisters-fellowship"], [
            ("youth-group.html", "青少年团契 (Youth)"),
            ("sisters-fellowship.html", "姐妹团契信息")
        ]),
        ("worship", "诗歌敬拜", active_nav == "worship", [
            ("worship.html", "教会敬拜诗歌 (2023)"),
            ("worship.html#choir", "唱诗班献唱与资料")
        ]),
        ("activities.html", "活动相册与视频", active_nav == "activities"),
        ("contact.html", "联系我们", active_nav == "contact"),
    ]

    nav_items_html = []
    for item in nav_links:
        if len(item) == 3:
            url, label, is_active = item
            cls = "nav-link active" if is_active else "nav-link"
            nav_items_html.append(f'''
          <li class="nav-item">
            <a href="{url}" class="{cls}">{label}</a>
          </li>''')
        else:
            _, label, is_active, submenus = item
            cls = "nav-link active" if is_active else "nav-link"
            sub_html = "\n".join([f'              <li class="submenu-item"><a href="{s_url}" class="submenu-link">{s_lbl}</a></li>' for s_url, s_lbl in submenus])
            nav_items_html.append(f'''
          <li class="nav-item has-submenu">
            <a href="#" class="{cls}">
              {label}
              <svg class="arrow-icon" viewBox="0 0 24 24"><path fill="currentColor" d="M7 10l5 5 5-5z"/></svg>
            </a>
            <ul class="submenu">
{sub_html}
            </ul>
          </li>''')

    nav_rendered = "\n".join(nav_items_html)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}} – 素里中国福音教会 SCEC</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <link rel="icon" type="image/png" href="assets/favicon.png">
  <link rel="stylesheet" href="styles.css">
</head>
<body>

  <!-- Top Announcement / Contact Bar -->
  <aside class="top-bar" aria-label="顶部联络信息">
    <div class="container">
      <div class="top-bar-left">
        <span class="top-bar-item">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          实体聚会地址：16870 80 AVE, Surrey, BC, Canada
        </span>
      </div>
      <div class="top-bar-right">
        <a href="tel:604-961-8357" class="top-bar-item">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          604-961-8357
        </a>
        <a href="mailto:contactus@scecchinese.com" class="top-bar-item">
          <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
          contactus@scecchinese.com
        </a>
      </div>
    </div>
  </aside>

  <!-- Sticky Main Header & Navigation -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="index.html" class="brand-wrapper" aria-label="素里中国福音教会 首页">
        <img src="assets/logo.png" alt="素里中国福音教会 徽标" class="brand-logo" width="48" height="48">
        <div class="brand-text">
          <span class="brand-title">素里中国福音教会</span>
          <span class="brand-subtitle">Surrey Christian Evangelical Church</span>
        </div>
      </a>

      <!-- Mobile Hamburger Button -->
      <button class="mobile-toggle" aria-label="切换导航菜单" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>

      <!-- Main Navigation Menu -->
      <nav class="main-nav" aria-label="主导航">
        <ul class="nav-list">
{nav_rendered}
        </ul>
      </nav>
    </div>
  </header>
'''

def get_footer():
    return '''
  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <h4>素里中国福音教会</h4>
          <p class="sub">Surrey Christian Evangelical Church</p>
          <p class="desc">
            我们是一个在美南浸信会下独立注册、自我管理的地方教会。致力于建立一个对外宣教、对内关爱、人人皆事奉、让神得荣耀的属灵大家庭。
          </p>
        </div>

        <div class="footer-col">
          <h5>站内导航</h5>
          <ul class="footer-links">
            <li><a href="index.html">网站首页</a></li>
            <li><a href="about.html">关于我们</a></li>
            <li><a href="worship.html">敬拜赞美诗歌</a></li>
            <li><a href="activities.html">活动相册与视频</a></li>
            <li><a href="contact.html">联系我们</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>团契与学习</h5>
          <ul class="footer-links">
            <li><a href="sunday-school.html">主日学教程</a></li>
            <li><a href="bible-study.html">圣经工具与典籍</a></li>
            <li><a href="youth-group.html">青少年团契 (Youth)</a></li>
            <li><a href="sisters-fellowship.html">姐妹团契信息</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h5>聚会与联络</h5>
          <p style="color: var(--color-gray-400); margin-bottom: 0.75rem; font-size: 0.88rem;">
            <strong>实体地点：</strong> 16870 80 AVE, Surrey, BC (inside SPA Church)
          </p>
          <p style="color: var(--color-gray-400); margin-bottom: 0.75rem; font-size: 0.88rem;">
            <strong>主日崇拜：</strong> 每周日下午 2:15 – 3:45
          </p>
          <p style="color: var(--color-gray-400); margin-bottom: 0.75rem; font-size: 0.88rem;">
            <strong>线上 Zoom ID：</strong> 324 568 6634
          </p>
          <p style="color: var(--color-gray-400); font-size: 0.88rem;">
            <strong>邮箱：</strong> contactus@scecchinese.com
          </p>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 素里中国福音教会 Surrey Christian Evangelical Church. All rights reserved.</div>
        <div style="color: var(--color-gray-500);">基于 GitHub Pages 托管 · 扎根真道，壮大教会</div>
      </div>
    </div>
  </footer>

  <!-- Back to Top Button -->
  <button class="back-to-top" aria-label="返回顶部">
    <svg viewBox="0 0 24 24"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
  </button>

  <script src="main.js"></script>
</body>
</html>
'''

def render_page(title, desc, active_nav, banner_title, banner_sub, breadcrumb_label, content_html):
    hdr = get_header(active_nav)
    hdr = hdr.replace("{{TITLE}}", title).replace("{{DESCRIPTION}}", desc)
    ftr = get_footer()
    
    banner = f'''
  <section class="page-banner">
    <div class="container">
      <h1 class="page-title">{banner_title}</h1>
      <p class="page-subtitle">{banner_sub}</p>
      <div class="breadcrumb-nav">
        <a href="index.html">首页</a> &gt; <span>{breadcrumb_label}</span>
      </div>
    </div>
  </section>
'''
    return hdr + banner + f'''
  <main class="subpage-container">
    <div class="container">
{content_html}
    </div>
  </main>
''' + ftr

def main():
    print("[*] Rebuilding subpages with accurate hymnal page numbers...")

    # Load songs with page numbers
    with open(os.path.join(OUTPUT_DIR, "assets/worship_songs_with_pages.json"), encoding="utf-8") as sf:
        songs = json.load(sf)

    song_items_html = []
    for s in songs:
        title = s['title']
        page = s['page']
        url = s['url']
        if url:
            song_items_html.append(f'''
          <a href="{url}" target="_blank" rel="noopener" class="song-item-wrapper" title="查看并播放 {title} ({page})">
            <div class="song-item-left">
              <span class="song-page-badge">{page}</span>
              <span class="song-name">{title}</span>
            </div>
            <svg class="song-play-icon" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          </a>''')
        else:
            song_items_html.append(f'''
          <div class="song-item-wrapper no-link" title="诗歌本目录曲目">
            <div class="song-item-left">
              <span class="song-page-badge">{page}</span>
              <span class="song-name">{title}</span>
            </div>
            <span style="font-size: 0.78rem; color: var(--color-gray-400);">诗本曲目</span>
          </div>''')

    songs_rendered = "\n".join(song_items_html)

    worship_content = f'''
      <div id="choir" class="content-card" style="border-top: 4px solid var(--primary-color);">
        <h2>诗班近期献唱录影</h2>
        <div class="resource-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
          <div class="resource-card">
            <h3 class="resource-title">2025年七月诗班献唱：《信靠顺服》</h3>
            <p class="resource-desc">自 2024 年圣诞节诗班成立以来，弟兄姐妹们练诗热情高涨，以歌声同心赞美救主。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/信靠顺服.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">2025年七月诗班献唱：《基督耶稣今复生》</h3>
            <p class="resource-desc">荣耀欢呼救主复活得胜，愿我们的歌声蒙神悦纳。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/%E5%9F%BA%E7%9D%A3%E8%80%B6%E7%A8%A3%E4%BB%8A%E5%A4%8D%E7%94%9F-202507.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;">
          <div>
            <h2 style="margin-bottom: 0.35rem;">教会敬拜赞美诗歌目录 (共 {len(songs)} 首)</h2>
            <p style="color: var(--color-gray-600); font-size: 0.95rem; margin-bottom: 0;">
              📖 <strong>保留教会诗本印刷页码</strong>：方便弟兄姊妹对照实体诗本。点击曲目即可直接播放试听伴奏：
            </p>
          </div>
        </div>

        <!-- Live Search Box with Page Number Support -->
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <input type="text" id="songSearch" class="search-input" placeholder="🔍 支持按歌名或诗本页码快速搜索（例如：26、第14页、恩典、平安、阿爸父...）" aria-label="搜索诗歌或页码">
        </div>

        <div id="songsList" class="songs-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));">
{songs_rendered}
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "worship.html"), "w", encoding="utf-8") as f:
        f.write(render_page("敬拜诗歌", f"素里中国福音教会敬拜赞美诗歌目录，完整保留教会印刷诗本页码对照及在线伴奏试听 (共 {len(songs)} 首)", "worship", "诗歌敬拜与诗本目录", "Worship Hymnal Directory & Recordings", "诗歌敬拜", worship_content))
    print("  [✓] Updated worship.html with hymnal page badges and dual search!")

if __name__ == "__main__":
    main()
