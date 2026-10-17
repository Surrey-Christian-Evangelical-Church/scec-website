#!/usr/bin/env python3
"""
SCEC Chinese Website Subpage Generator for GitHub Pages
Generates complete, responsive, styled subpages matching index.html,
with song page numbers, piano notes, and sheet music links fully preserved.
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
        ("worship", "诗歌敬拜", active_nav in ["worship", "choir"], [
            ("worship.html", "敬拜赞美诗歌 (诗本目录)"),
            ("choir.html", "诗班献唱与资料")
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
            <li><a href="choir.html">诗班献唱与资料</a></li>
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
    print("[*] Rebuilding subpages (with full piano notes and sheet music support)...")

    # 1. about.html
    about_content = '''
      <div class="content-card">
        <h2>教会历史与建会背景</h2>
        <p>素里中国福音教会（Surrey Christian Evangelical Church）由原属中国福音教会而居住在素里地区的几个家庭，在三一真神的呼召和感动下，经过长时间祷告后于 <strong>2008 年 2 月</strong> 所创建的。</p>
        <p><strong>2015 年</strong> 教会正式完成注册，现在是在<strong>美南浸信会 (Southern Baptist Convention)</strong> 联会下，独立注册、自我管理的地方教会。</p>
        <p>教会的异象和使命是：<strong>建立一个对外宣教、对内关爱、人人皆事奉、让神得荣耀的新型地方教会。</strong></p>
      </div>

      <div class="content-card">
        <h2>聚会与事工架构</h2>
        <p>教会现在固定在每周日下午分别有普通话敬拜和英文敬拜，以及成人及儿童主日学。每周有团契和小组查经学习。</p>
        <p>教会的行政结构由教会长执会以及各事工部组成。目前教会的事工主要包括：<strong>崇拜、团契、宣教、教导、关怀、儿童以及英语事工</strong>，并朝建设完善的英文堂而努力，为此我们欢迎有多种族、多语言、多地区背景的慕道友和弟兄姊妹加入到我们主爱的大家庭。</p>
      </div>

      <div class="content-card">
        <h2>我们的团契与关怀</h2>
        <p>教会是个以基督耶稣为元首，满有爱心，在耶稣基督的大使命上有份的群体。弟兄姊妹蒙召得救后互为肢体，彼此相爱，彼此祷告扶持，彼此关怀帮助，共同追求真理、生命成长、兴旺福音、同心祷告。</p>
        <p>无论您是初来此地还是长居异乡，或是寻找人生真谛，或是遭遇生活问题，我们盼望您和家人都可以在这里感受到基督里的关怀与温暖，以及神的信实与大能。<strong>素里中国福音教会所有弟兄姊妹都热烈欢迎您！</strong></p>
        
        <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
          <a href="contact.html" class="btn btn-primary" style="background-color: var(--primary-color); color: white;">联系我们与交通指引 &rarr;</a>
          <a href="index.html#schedule" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color);">查看聚会时间表</a>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(render_page("关于我们", "素里中国福音教会建会历史、事工架构与信仰异象", "about", "关于我们", "About Surrey Christian Evangelical Church", "关于我们", about_content))
    print("  -> Generated about.html")

    # 2. sunday-school.html
    sunday_content = '''
      <div class="content-card">
        <h2>成人主日学核心课程</h2>
        <p>成人主日学旨在装备信徒深刻认识神的话语，建立纯正的信仰根基，活出得胜丰盛的基督徒生命。</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg></div>
            <h3 class="resource-title">1. 新生命网络版</h3>
            <p class="resource-desc">一套能够帮助慕道友和初信者深入认识耶稣基督救恩与信仰基础的经典栽培教材。</p>
            <div class="resource-action">
              <a href="http://www.jonahome.net/files/xsm/index.htm" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">在线阅读教材 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg></div>
            <h3 class="resource-title">2. 新生活网络版</h3>
            <p class="resource-desc">教导信徒怎样在日常生活、工作与家庭中实践神的话语，过圣洁得胜的基督徒生活。</p>
            <div class="resource-action">
              <a href="http://www.jonahome.net/files/xsh/index.htm" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">在线阅读教材 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg></div>
            <h3 class="resource-title">3. 门徒之道 (PDF)</h3>
            <p class="resource-desc">系统性的栽培查经教材，既适合老师作为课堂教学课本，也适合弟兄姊妹个人研经自学。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/wp-content/uploads/2021/03/discipleship.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载 PDF 电子书 (1.3MB) &darr;</a>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2>儿童主日学优质资源</h2>
        <p>让孩子们从小在圣经真理中成长，认识神的爱与公义：</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <h3 class="resource-title">Ministry to Children</h3>
            <p class="resource-desc">提供单周独立课程与多周系统课程单元，包含丰富的儿童查经与互动材料。</p>
            <div class="resource-action">
              <a href="https://ministry-to-children.com/sunday-school-lessons/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">访问官网 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">Kids Sunday School Place</h3>
            <p class="resource-desc">涵盖学龄前与小学的儿童主日学教材，提供富有创意的经文手工、活动与教学指南。</p>
            <div class="resource-action">
              <a href="https://www.kidssundayschool.com/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">访问官网 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">Lifeway Kids Sunday School</h3>
            <p class="resource-desc">美南浸信会 Lifeway 出版的高质量圣经教学体系，帮助孩子建立整本圣经大图景。</p>
            <div class="resource-action">
              <a href="https://www.lifeway.com/en/shop/bible-studies/sunday-school" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">访问官网 &rarr;</a>
            </div>
          </div>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "sunday-school.html"), "w", encoding="utf-8") as f:
        f.write(render_page("主日学教程", "素里中国福音教会成人及儿童主日学教材推荐与下载", "sunday-school", "主日学教程", "Sunday School Curriculum & Resources", "主日学教程", sunday_content))
    print("  -> Generated sunday-school.html")

    # 3. bible-study.html
    bible_content = '''
      <div class="content-card">
        <h2>查经背景与研经典籍下载</h2>
        <p>提供深入了解圣经历史地理文化背景的重要学术注释工具书：</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <h3 class="resource-title">旧约圣经背景注释 (PDF)</h3>
            <p class="resource-desc">华尔顿 (John H. Walton) 等学者著，详细介绍旧约各卷的历史、地理、考古与文化背景。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/books/%E6%97%A7%E7%BA%A6%E5%9C%A3%E7%BB%8F%E8%83%8C%E6%99%AF%E6%B3%A8%E9%87%8A.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载 PDF (50MB) &darr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">新约圣经背景注释 (PDF)</h3>
            <p class="resource-desc">季纳 (Craig S. Keener) 著，详尽解析新约时代希腊罗马与犹太文化语境。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/books/%E6%96%B0%E7%BA%A6%E8%83%8C%E6%99%AF%E6%B3%A8%E9%87%8A.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载 PDF (35MB) &darr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">圣经年表大事记 (2021修订版)</h3>
            <p class="resource-desc">按时间线清晰梳理圣经历史事件、以色列君王与先知年代对照。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/books/%E5%9C%A3%E7%BB%8F%E5%B9%B4%E8%A1%A8%E5%A4%A7%E4%BA%8B%E8%AE%B0%E4%BF%AE%E8%AE%A2%E7%89%882021.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载 PDF (3.2MB) &darr;</a>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2>在线研经与神学文献工具</h2>
        <div class="resource-grid">
          <div class="resource-card">
            <h3 class="resource-title">信望爱圣经工具</h3>
            <p class="resource-desc">提供原文原文字典、多版本圣经对照、交互式查经注解。</p>
            <div class="resource-action">
              <a href="https://bible.fhl.net/gbdoc/NUI/#/bible/Ge/1/1" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">进入网站 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">华训研经工具</h3>
            <p class="resource-desc">华人基督徒培训供应中心提供的专业归纳法查经与培训资料。</p>
            <div class="resource-action">
              <a href="http://home.yanjinggongju.com/b/web/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">进入网站 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">BBN 圣经学院</h3>
            <p class="resource-desc">圣言广播网免费网络圣经课程，系统学习旧约、新约与教义神学。</p>
            <div class="resource-action">
              <a href="http://www.bbnradio.org/wcm4/bbnbischinese/Home/tabid/2381/Default.aspx" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">进入网站 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">中国神学研究院</h3>
            <p class="resource-desc">高质量学术文献、神学讲座录音与宣教研究成果。</p>
            <div class="resource-action">
              <a href="https://www.cgst.edu/hk/cht/Homepage/index" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">进入网站 &rarr;</a>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2>灵命造就与经典属灵书籍</h2>
        <ul style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
          <li><a href="http://shu.kyhs.net/" target="_blank" rel="noopener" style="font-weight: 600;">📖 旷野书库</a></li>
          <li><a href="http://wellsofgrace.com/index-books.htm" target="_blank" rel="noopener" style="font-weight: 600;">📖 属灵书籍书库</a></li>
          <li><a href="http://www.godoor.net/" target="_blank" rel="noopener" style="font-weight: 600;">📖 信仰之门</a></li>
          <li><a href="http://cclw.net/other/jhgrpx/index.html" target="_blank" rel="noopener" style="font-weight: 600;">📖 教会工人培训手册</a></li>
          <li><a href="http://www.blessed.org/" target="_blank" rel="noopener" style="font-weight: 600;">📖 福音的桥梁</a></li>
          <li><a href="http://cclw.net/gospel/explore/youziyin/htm/index.htm" target="_blank" rel="noopener" style="font-weight: 600;">📖 游子吟 (冯秉诚)</a></li>
          <li><a href="http://cclw.net/book/bgrs/htm/index2.html" target="_blank" rel="noopener" style="font-weight: 600;">📖 标杆人生 (华理克)</a></li>
          <li><a href="https://www.goodtv.tv/" target="_blank" rel="noopener" style="font-weight: 600;">📺 好消息 GOOD TV 影视</a></li>
        </ul>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "bible-study.html"), "w", encoding="utf-8") as f:
        f.write(render_page("圣经学习工具", "圣经注释背景、在线查经工具及属灵电子书下载", "bible-study", "圣经学习工具", "Bible Study Tools & Spiritual Resources", "圣经工具", bible_content))
    print("  -> Generated bible-study.html")

    # 4. youth-group.html
    youth_content = '''
      <div class="content-card">
        <h2>欢迎加入青少年团契 (Youth Group)</h2>
        <p>欢迎加入素里中国福音教会青少年团契。我们的青少年团契是由一群充满活力、对基督信仰有热烈追求的年轻人组成。</p>
        
        <div style="background-color: var(--primary-light); padding: 1.5rem; border-radius: var(--border-radius-md); border-left: 4px solid var(--primary-color); margin: 1.5rem 0;">
          <h3 style="margin-top: 0; color: var(--primary-dark);">聚会时间与安排：</h3>
          <ul style="list-style: disc; margin-left: 1.5rem; line-height: 1.8;">
            <li><strong>周五团契活动：</strong> 每周五晚 <strong>7:00 – 9:30 PM</strong></li>
            <li><strong>主日英文崇拜：</strong> 每周日下午 <strong>2:15 – 3:45 PM</strong></li>
            <li><strong>聚会地点：</strong> 16870 80 AVE, Surrey, BC (inside SPA Church)</li>
          </ul>
        </div>

        <p><em>Welcome to join SCEC youth group. Our youth group consists of young people who are dedicated to learning about Jesus Christ and growing in the faith. They have activities every Friday night from 7:00 pm to 9:30 pm. Their weekly worships are held every Sunday afternoon from 2:15 pm to 3:45 pm.</em></p>
      </div>

      <div class="content-card">
        <h2>关注与联系青少年团契社媒</h2>
        <p>若想了解更多青少年团契最新活动信息与精彩剪影，请关注：</p>
        
        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 1.5rem;">
          <a href="https://www.instagram.com/scecyouth/" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: #E1306C; color: white;">
            关注 Instagram @scecyouth &rarr;
          </a>
          <a href="https://www.facebook.com/groups/819364824802794" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: #1877F2; color: white;">
            加入 Facebook 群组 &rarr;
          </a>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "youth-group.html"), "w", encoding="utf-8") as f:
        f.write(render_page("青少年团契", "素里中国福音教会青少年团契(Youth Group)聚会时间与社媒动态", "youth-group", "青少年团契 (Youth Group)", "Loving God, Growing in Faith, Building Fellowship", "青少年团契", youth_content))
    print("  -> Generated youth-group.html")

    # 5. sisters-fellowship.html
    sisters_content = '''
      <div class="content-card">
        <h2>姐妹团契聚会介绍</h2>
        <p>姐妹团契每月定期相聚一次，通过诗歌赞美、灵修分享、见证交通与互相代祷，让姐妹们在基督的爱里彼此建造、彼此分担、建立深厚的属灵友谊。</p>
        <p><strong>聚会频率：</strong> 每月一次（具体时间和地点待定，提前在教会通知）。</p>
      </div>

      <div class="content-card">
        <h2>灵修信息与讲座分享</h2>
        <div class="resource-grid">
          <div class="resource-card">
            <h3 class="resource-title">活水泉源–圣经中的三段井边姻缘</h3>
            <p class="resource-desc">何文辉姊妹信息分享（2022-02-10），从创世记与福音书中的井边相遇探讨神在人生命中的恩典与信实带领。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/books/%E6%B4%BB%E6%B0%B4%E6%B3%89%E6%BA%90.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载阅读 PDF (262KB) &darr;</a>
            </div>
          </div>

          <div class="resource-card">
            <h3 class="resource-title">知识与生命：两棵树的故事</h3>
            <p class="resource-desc">何文辉姊妹信息分享（2022-05-12），探讨分辨善恶树与生命树的灵意，引导信徒选择连接于生命的源头。</p>
            <div class="resource-action">
              <a href="https://www.scecchinese.com/books/知识与生命：两棵树的故事.pdf" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">下载阅读 PDF (288KB) &darr;</a>
            </div>
          </div>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "sisters-fellowship.html"), "w", encoding="utf-8") as f:
        f.write(render_page("姐妹团契", "素里中国福音教会姐妹团契信息与属灵分享资料", "sisters-fellowship", "姐妹团契信息分享", "Sisters Fellowship Information & Resources", "姐妹团契", sisters_content))
    print("  -> Generated sisters-fellowship.html")

    # 6. worship.html (Focused on 252 songs with hymnal page numbers & sheet music/piano links)
    with open(os.path.join(OUTPUT_DIR, "assets/worship_songs_complete.json"), encoding="utf-8") as sf:
        songs = json.load(sf)

    song_items_html = []
    for s in songs:
        title = s['title']
        page = s['page']
        primary_url = s.get('primary_url')
        sheets = s.get('sheets', [])
        
        # Build action buttons
        action_btns = []
        if primary_url:
            if primary_url.startswith("http://"):
                primary_url = "https://" + primary_url[7:]
            action_btns.append(f'''<a href="{primary_url}" target="_blank" rel="noopener" class="song-btn btn-play" title="播放伴奏视频"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg> 试听</a>''')
        
        for sh in sheets:
            sh_title = sh['title']
            sh_url = sh['url']
            if sh_url.startswith("http://"):
                sh_url = "https://" + sh_url[7:]
            icon = "🎹" if "琴" in sh_title else "🎼"
            action_btns.append(f'''<a href="{sh_url}" target="_blank" rel="noopener" class="song-btn btn-sheet" title="{sh_title}">{icon} {sh_title}</a>''')

        if action_btns:
            actions_rendered = f'''<div class="song-actions">{" ".join(action_btns)}</div>'''
            song_items_html.append(f'''
          <div class="song-item-wrapper">
            <div class="song-item-left">
              <span class="song-page-badge">{page}</span>
              <span class="song-name">{title}</span>
            </div>
            {actions_rendered}
          </div>''')
        else:
            song_items_html.append(f'''
          <div class="song-item-wrapper no-link">
            <div class="song-item-left">
              <span class="song-page-badge">{page}</span>
              <span class="song-name">{title}</span>
            </div>
            <span class="song-note-muted">诗本曲目</span>
          </div>''')

    songs_rendered = "\n".join(song_items_html)

    worship_content = f'''
      <!-- Callout to dedicated Choir page -->
      <div style="background: linear-gradient(135deg, var(--primary-light) 0%, #ffffff 100%); border-radius: var(--border-radius-lg); border: 1px solid var(--primary-border); padding: 1.5rem 2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h3 style="font-size: 1.25rem; color: var(--primary-dark); margin-bottom: 0.25rem;">🎵 寻找教会诗班献唱录影与练习材料？</h3>
          <p style="color: var(--color-gray-600); font-size: 0.95rem; margin-bottom: 0;">我们已为诗班设立了专门页面，收录历次献唱录像与排练信息。</p>
        </div>
        <a href="choir.html" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.9rem; padding: 0.55rem 1.25rem;">
          前往诗班专区 &rarr;
        </a>
      </div>

      <div class="content-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem;">
          <div>
            <h2 style="margin-bottom: 0.35rem;">教会敬拜赞美诗歌目录 (共 {len(songs)} 首)</h2>
            <p style="color: var(--color-gray-600); font-size: 0.95rem; margin-bottom: 0;">
              📖 <strong>完整保留实体诗本页码与乐谱链接</strong>：包含钢琴伴奏视频、钢琴谱 (第一页/第二页)、五线谱及简谱。点击即可播放或查看高清乐谱：
            </p>
          </div>
        </div>

        <!-- Live Search Box with Page Number & Piano Notes Support -->
        <div class="search-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <input type="text" id="songSearch" class="search-input" placeholder="🔍 支持按歌名、页码或乐谱快速搜索（例如：平安、69、第71页、钢琴谱、五线谱、千万个理由...）" aria-label="搜索诗歌、页码或乐谱">
        </div>

        <div id="songsList" class="songs-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));">
{songs_rendered}
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "worship.html"), "w", encoding="utf-8") as f:
        f.write(render_page("敬拜诗歌", f"素里中国福音教会敬拜赞美诗歌目录，完整保留教会印刷诗本页码对照、钢琴谱、五线谱及在线试听 (共 {len(songs)} 首)", "worship", "诗歌敬拜与诗本目录", "Worship Hymnal Directory & Sheet Music", "敬拜诗歌", worship_content))
    print("  -> Generated worship.html (with full piano notes and sheet music links!)")

    # 7. choir.html (NEW dedicated choir page)
    choir_content = '''
      <div class="content-card" style="border-top: 4px solid var(--primary-color);">
        <h2>素里中国福音教会诗班简介</h2>
        <p>自 <strong>2024 年圣诞节诗班正式成立</strong>以来，弟兄姐妹们练诗的热情高涨。诗班以歌声在主日崇拜与重大节日特别聚会中同心赞美三一真神，传递救恩的喜乐与盼望。<strong>“愿我们以歌声赞美主，愿我们的歌唱蒙神悦纳！”</strong></p>
      </div>

      <div class="content-card">
        <h2>诗班近期献唱录影</h2>
        <p>点击下方卡片即可在线观看诗班历次献唱视频：</p>
        
        <div class="resource-grid" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div>
            <h3 class="resource-title">2025年七月献唱：《信靠顺服》</h3>
            <p class="resource-desc">2025 年诗班第二次献诗，深情颂扬在基督里坚定信靠、全然顺服的平安与福分。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/信靠顺服.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.5rem 1.1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div>
            <h3 class="resource-title">2025年七月献唱：《基督耶稣今复生》</h3>
            <p class="resource-desc">荣耀欢呼救主耶稣基督战胜死权、荣耀复活的凯歌，振奋人心。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/%E5%9F%BA%E7%9D%A3%E8%80%B6%E7%A8%A3%E4%BB%8A%E5%A4%8D%E7%94%9F-202507.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.5rem 1.1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div>
            <h3 class="resource-title">2024年圣诞诗班献唱：《平安夜》</h3>
            <p class="resource-desc">2024 年圣诞特别晚会诗班献诗，在宁静圣洁的歌声中思想救主基督道成肉身的宏恩。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/SilentNight.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.5rem 1.1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>

          <div class="resource-card">
            <div class="resource-icon"><svg viewBox="0 0 24 24"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg></div>
            <h3 class="resource-title">教会建会 15 周年庆典诗班献诗</h3>
            <p class="resource-desc">感恩神十五年来对素里中国福音教会的眷顾、保守与带领，全体同心赞美主恩。</p>
            <div class="resource-action">
              <a href="https://scecchinese.com/mp4/anniversary15.mp4" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.5rem 1.1rem;">播放视频 MP4 &rarr;</a>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2>诗班练诗与内部资料说明</h2>
        <p>为便于诗班成员排练与声部学习，各声部练习曲音频、伴奏乐谱及歌词排练表将统一归档于教会 Google Drive 内部资料库中。</p>
        <div style="background-color: var(--color-gray-50); border: 1px dashed var(--primary-border); border-radius: var(--border-radius-md); padding: 1.5rem; margin-top: 1rem;">
          <p style="margin-bottom: 0.5rem; font-weight: 600; color: var(--primary-dark);">🔒 诗班成员专属提示：</p>
          <p style="color: var(--color-gray-600); margin-bottom: 0; font-size: 0.92rem;">
            诗班分声部音频练习资料存放在教会专用共享云端中。诗班成员请使用向教会登记的 Google 邮箱查阅；如需索取新曲目乐谱或音频文件，请随时在主日练诗时与诗班长或司琴同工联络。
          </p>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "choir.html"), "w", encoding="utf-8") as f:
        f.write(render_page("诗班献唱与资料", "素里中国福音教会诗班献唱视频录影、事工介绍与诗班排练资料", "choir", "诗班献唱与敬拜资料", "SCEC Church Choir Worship & Resources", "诗班专区", choir_content))
    print("  -> Generated choir.html")

    # 8. activities.html
    activities_content = '''
      <div class="content-card">
        <h2>历年聚会活动与精彩回顾</h2>
        <p>记录素里中国福音教会历年重大庆典、户外崇拜、家庭夏令营与圣诞庆祝晚会：</p>
      </div>

      <!-- Event 1 -->
      <article class="event-card">
        <img src="assets/worship-service.jpg" alt="2025年七月诗班献唱" class="event-thumb">
        <div class="event-info">
          <span class="event-tag">2025 诗班献唱</span>
          <h3 class="event-title">2025年七月诗班献唱</h3>
          <p class="event-desc">自 2024 年圣诞节诗班成立以来，弟兄姐妹们练诗的热情高涨。此次献诗为 2025 年第二次诗班献唱，包含《信靠顺服》与《基督耶稣今复生》。</p>
          <a href="choir.html" class="btn btn-primary" style="background-color: var(--primary-color); color: white; align-self: flex-start; font-size: 0.88rem; padding: 0.45rem 1rem;">观看献唱录影 &rarr;</a>
        </div>
      </article>

      <!-- Event 2 -->
      <article class="event-card">
        <img src="assets/summer-camp.jpg" alt="2025年夏季野外崇拜" class="event-thumb">
        <div class="event-info">
          <span class="event-tag">2025 户外敬拜</span>
          <h3 class="event-title">2025年夏季野外崇拜</h3>
          <p class="event-desc">每年夏天教会在大自然中举办的户外野餐与崇拜聚会，全教会弟兄姊妹同心敬拜赞美神。</p>
          <a href="https://scecchinese.com/2025-outdoor-worship/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); align-self: flex-start; font-size: 0.88rem; padding: 0.45rem 1rem;">查看现场照片 &rarr;</a>
        </div>
      </article>

      <!-- Event 3 -->
      <article class="event-card">
        <img src="assets/christmas-highlight-1.jpg" alt="2024年圣诞晚会" class="event-thumb">
        <div class="event-info">
          <span class="event-tag">2024 圣诞庆祝</span>
          <h3 class="event-title">2024年圣诞特别聚会与晚会相册</h3>
          <p class="event-desc">圣诞晚会节目丰富多彩，包含诗班献唱《平安夜》、各个小组舞蹈短剧、儿童主日学精彩表演。现场记录了 500+ 张高清照片与全场视频。</p>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <a href="https://scecchinese.com/2024-christmas-party/" target="_blank" rel="noopener" class="btn btn-primary" style="background-color: var(--primary-color); color: white; font-size: 0.88rem; padding: 0.45rem 1rem;">晚会节目单与视频 &rarr;</a>
            <a href="https://scecchinese.com/2024-christmas-photos/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); font-size: 0.88rem; padding: 0.45rem 1rem;">浏览 500+ 张照片集锦 &rarr;</a>
          </div>
        </div>
      </article>

      <!-- Event 4 -->
      <article class="event-card">
        <img src="assets/hero-bg.jpg" alt="2023年圣诞特别聚会" class="event-thumb">
        <div class="event-info">
          <span class="event-tag">2023 圣诞聚会</span>
          <h3 class="event-title">2023年圣诞特别聚会</h3>
          <p class="event-desc">诗歌敬拜、圣诞信息分享及晚会各小组庆祝表演视频与高清相册。</p>
          <a href="https://scecchinese.com/2023-christmas-party/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); align-self: flex-start; font-size: 0.88rem; padding: 0.45rem 1rem;">查看回顾 &rarr;</a>
        </div>
      </article>

      <!-- Event 5 -->
      <article class="event-card">
        <img src="assets/summer-camp.jpg" alt="2019年夫妻家庭夏令营" class="event-thumb">
        <div class="event-info">
          <span class="event-tag">2019 家庭夏令营</span>
          <h3 class="event-title">2019年夫妻家庭夏令营</h3>
          <p class="event-desc">在美丽的 Sasamat Lake 湖边成功举办，邀请讲员深入浅出分享见证与家庭沟通，灵命身心皆大得造就。</p>
          <a href="https://scecchinese.com/2019summercamp/" target="_blank" rel="noopener" class="btn btn-outline" style="border-color: var(--primary-color); color: var(--primary-color); align-self: flex-start; font-size: 0.88rem; padding: 0.45rem 1rem;">查看夏令营剪影 &rarr;</a>
        </div>
      </article>
'''
    with open(os.path.join(OUTPUT_DIR, "activities.html"), "w", encoding="utf-8") as f:
        f.write(render_page("活动相册及视频", "素里中国福音教会历年圣诞特别聚会、户外崇拜与家庭夏令营精彩剪影", "activities", "活动相册与视频", "Church Activities, Photo Albums & Videos", "活动相册", activities_content))
    print("  -> Generated activities.html")

    # 9. contact.html
    contact_content = '''
      <div class="contact-layout" style="margin-top: 0;">
        <!-- Left: Info & Map -->
        <div>
          <h2 style="font-size: 1.5rem; color: var(--color-gray-900); margin-bottom: 0.5rem; font-weight: 700;">聚会地点与交通指引</h2>
          <p style="color: var(--color-gray-600); font-size: 0.95rem; margin-bottom: 1.5rem;">我们每周日在 Surrey Pentecostal Assembly (SPA Church) 场地举行实体崇拜，欢迎前来进行属灵交流与参与主日崇拜。</p>

          <div class="contact-info-list">
            <div class="contact-info-item">
              <div class="contact-icon-box"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg></div>
              <div>
                <div class="contact-info-title">实体崇拜聚会地址</div>
                <div class="contact-info-val">16870 80 AVE, Surrey, BC, Canada</div>
                <div style="font-size: 0.85rem; color: var(--color-gray-500); margin-top: 2px;">(Located inside Surrey Pentecostal Assembly)</div>
              </div>
            </div>

            <div class="contact-info-item">
              <div class="contact-icon-box"><svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg></div>
              <div>
                <div class="contact-info-title">电子邮箱</div>
                <div class="contact-info-val"><a href="mailto:contactus@scecchinese.com">contactus@scecchinese.com</a></div>
              </div>
            </div>

            <div class="contact-info-item">
              <div class="contact-icon-box"><svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg></div>
              <div>
                <div class="contact-info-title">联系电话</div>
                <div class="contact-info-val"><a href="tel:604-961-8357">604-961-8357</a></div>
              </div>
            </div>

            <div class="contact-info-item">
              <div class="contact-icon-box"><svg viewBox="0 0 24 24"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg></div>
              <div>
                <div class="contact-info-title">线上聚会 Zoom 会议 ID</div>
                <div class="contact-info-val"><span class="zoom-id">324 568 6634</span></div>
                <div style="font-size: 0.85rem; color: var(--color-gray-500); margin-top: 2px;">适用于周三祷告会与周二查经班</div>
              </div>
            </div>
          </div>

          <!-- Embedded Map -->
          <div class="map-card" style="height: 240px;">
            <iframe 
              title="素里中国福音教会地图定位"
              src="https://maps.google.com/maps?q=16870+80+AVE,+Surrey,+BC&t=&z=14&ie=UTF8&iwloc=&output=embed"
              loading="lazy">
            </iframe>
          </div>
        </div>

        <!-- Right: Contact Form -->
        <div>
          <h2 style="font-size: 1.5rem; color: var(--color-gray-900); margin-bottom: 0.5rem; font-weight: 700;">在线留言咨询</h2>
          <p style="color: var(--color-gray-600); font-size: 0.95rem; margin-bottom: 1.5rem;">如果您想了解更多关于教会的信息，欢迎您在线留言。同工收到后会尽快联络您：</p>

          <form id="contactForm" class="contact-form">
            <div class="form-group">
              <label for="name" class="form-label">您的姓名 <span style="color: red;">*</span></label>
              <input type="text" id="name" class="form-control" placeholder="例如：张弟兄 / 李姊妹" required>
            </div>

            <div class="form-group">
              <label for="email" class="form-label">电子邮箱 <span style="color: red;">*</span></label>
              <input type="email" id="email" class="form-control" placeholder="name@example.com" required>
            </div>

            <div class="form-group">
              <label for="phone" class="form-label">联络电话 (可选)</label>
              <input type="tel" id="phone" class="form-control" placeholder="604-xxx-xxxx">
            </div>

            <div class="form-group">
              <label for="subject" class="form-label">留言主题</label>
              <input type="text" id="subject" class="form-control" placeholder="聚会咨询 / 代祷事项 / 探访联络">
            </div>

            <div class="form-group">
              <label for="message" class="form-label">留言详细内容 <span style="color: red;">*</span></label>
              <textarea id="message" class="form-control" placeholder="请在此输入您的留言内容..." required></textarea>
            </div>

            <button type="submit" class="btn btn-primary" style="background-color: var(--primary-color); color: var(--color-white); width: 100%; border-radius: var(--border-radius-sm); padding: 0.85rem;">
              提交留言信息
            </button>
          </form>

          <div id="toastMsg" class="toast-msg" role="status" aria-live="polite">
            ✓ 您的留言已成功记录！教会同工将尽快与您联系。
          </div>
        </div>
      </div>
'''
    with open(os.path.join(OUTPUT_DIR, "contact.html"), "w", encoding="utf-8") as f:
        f.write(render_page("联系我们", "素里中国福音教会实体聚会点交通地址、联系电话、邮箱及在线留言", "contact", "联系我们与聚会地点", "Contact Surrey Christian Evangelical Church", "联系我们", contact_content))
    print("  -> Generated contact.html")

    print("[✓] All subpages generated with complete sheet music links successfully!")

if __name__ == "__main__":
    main()
