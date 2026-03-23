#!/usr/bin/env python3
"""
Arxiv 论文监控器 - 每日自动获取最新论文
"""
import os
import re
import json
import time
import requests
from datetime import datetime, timedelta

# 配置
ARXIV_API = "http://export.arxiv.org/api/query"
KEYWORDS = ["LLM Security", "Machine Learning Security", "Adversarial ML", "AI Security"]

def search_arxiv(keyword, max_results=20):
    """搜索 Arxiv 最新论文"""
    today = datetime.now()
    date_range = (today - timedelta(days=7)).strftime("%Y%m%d")
    
    query = f"all:{keyword.strip()}+AND+submittedDate:[{date_range}+TO+{today.strftime('%Y%m%d')}]"
    
    url = f"{ARXIV_API}?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    print(f"🔍 搜索: {keyword}")
    
    try:
        response = requests.get(url, timeout=30)
        entries = []
        
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            published = entry.find('{http://www.w3.org/2005/Atom}published').text[:10]
            
            pdf_link = None
            for link in entry.findall('{http://www.w3.org/2005/Atom}link'):
                if link.get('title') == 'pdf':
                    pdf_link = link.get('href')
                    break
            
            authors = [a.find('{http://www.w3.org/2005/Atom}name').text 
                      for a in entry.findall('{http://www.w3.org/2005/Atom}author')]
            
            entries.append({
                'title': title,
                'summary': summary[:800],
                'published': published,
                'pdf': pdf_link,
                'authors': authors[:5],
                'keyword': keyword
            })
        
        print(f"   找到 {len(entries)} 篇")
        return entries
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return []

def main():
    print(f"\n📅 Arxiv 论文监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    all_papers = []
    for keyword in KEYWORDS:
        papers = search_arxiv(keyword)
        all_papers.extend(papers)
        time.sleep(2)
    
    # 去重
    seen = set()
    unique_papers = []
    for p in all_papers:
        if p['title'] not in seen:
            seen.add(p['title'])
            unique_papers.append(p)
    
    print(f"\n📊 共 {len(unique_papers)} 篇新论文")
    
    # 保存
    queue_file = "/root/.openclaw/workspace/paper-research/paper_queue.json"
    with open(queue_file, 'w') as f:
        json.dump(unique_papers, f, indent=2, ensure_ascii=False)
    
    return unique_papers

if __name__ == "__main__":
    main()
