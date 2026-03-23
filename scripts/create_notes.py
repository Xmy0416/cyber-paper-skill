#!/usr/bin/env python3
import os
import json
from datetime import datetime

inbox_dir = "/root/.openclaw/workspace/paper-research/inbox"
queue_file = "/root/.openclaw/workspace/paper-research/paper_queue.json"

# 加载论文队列
with open(queue_file, 'r') as f:
    papers = json.load(f)

os.makedirs(inbox_dir, exist_ok=True)

print(f"📝 生成 {len(papers)} 篇 Obsidian 笔记...")

for i, paper in enumerate(papers[:10], 1):  # 先处理前10篇
    # 清理文件名
    safe_title = paper['title'][:50].replace("/", "-").replace(":", "-").replace("?", "").replace("*", "")
    filename = f"{paper['published']}_{safe_title}.md"
    filepath = os.path.join(inbox_dir, filename)
    
    content = f"""---
title: "{paper['title']}"
authors: {json.dumps(paper['authors'])}
published: {paper['published']}
keyword: "{paper.get('keyword', '')}"
date_added: "{datetime.now().strftime('%Y-%m-%d')}"
status: inbox
tags: [arxiv, {paper.get('keyword', 'paper').replace(' ', '-')}]
---

# {paper['title']}

> 由 OpenClaw 自动生成

## 📋 论文信息
- **作者**: {', '.join(paper['authors'][:3])}{' 等' if len(paper['authors']) > 3 else ''}
- **发表日期**: {paper['published']}
- **关键词**: {paper.get('keyword', '')}

## 📝 摘要
{paper['summary'][:600]}...

## 🎯 核心贡献

- [ ] 贡献点 1
- [ ] 贡献点 2  
- [ ] 贡献点 3

## 💡 相关工作

- [ ]

## 🔗 链接
- **PDF**: [Arxiv]({paper['pdf']})

## 📌 阅读决策

- [ ] 精读
- [ ] 略读
- [ ] 跳过

---
*🕐 添加于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ {filename}")

print(f"\n✨ 完成！前 {min(10, len(papers))} 篇笔记已生成")
