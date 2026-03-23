#!/usr/bin/env python3
"""
下载 NDSS 2025 论文
"""
import os
import subprocess
import time
import re

BASE_URL = "https://www.ndss-symposium.org"
PAPER_LIST_URL = f"{BASE_URL}/ndss2025/accepted-papers/"
OUTPUT_DIR = "/home/ubuntu/paper/NDSS_2025"

def get_paper_slugs():
    """从论文列表页面提取所有论文的 slug"""
    result = subprocess.run(
        ["curl", "-sL", PAPER_LIST_URL],
        capture_output=True, text=True
    )
    # 提取论文 URL 并解析 slug
    urls = re.findall(r'href="(https://www\.ndss-symposium\.org/ndss-paper/[^"]+/)"', result.stdout)
    slugs = [url.split('/')[-2] for url in urls]
    return list(set(slugs))

def get_pdf_url(slug):
    """从论文详情页获取 PDF 下载链接"""
    url = f"{BASE_URL}/ndss-paper/{slug}/"
    result = subprocess.run(
        ["curl", "-sL", url],
        capture_output=True, text=True
    )
    # 查找 PDF 链接 - 优先使用 2025-xxx-paper.pdf 格式
    matches = re.findall(r'wp-content/uploads/((?:2025-)?\d+-[^"]+\.pdf)', result.stdout)
    if matches:
        # 优先选择 2025-xxx-paper.pdf 格式
        for match in matches:
            if match.startswith('2025-'):
                return f"{BASE_URL}/wp-content/uploads/{match}"
        # 否则使用第一个
        return f"{BASE_URL}/wp-content/uploads/{matches[0]}"
    return None

def download_pdf(slug, pdf_url):
    """下载 PDF 文件"""
    # 清理 slug 作为文件名
    filename = slug[:100]  # 限制文件名长度
    filename = re.sub(r'[^a-zA-Z0-9\-]', '-', filename)
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.pdf")
    
    # 如果文件已存在，跳过
    if os.path.exists(filepath):
        print(f"  跳过: {filename}.pdf (已存在)")
        return True
    
    print(f"  下载: {filename}.pdf")
    try:
        result = subprocess.run(
            ["curl", "-sL", "-o", filepath, pdf_url],
            capture_output=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        print(f"  失败: {filename}.pdf (超时)")
        return False
    
    # 检查文件是否有效（大于 1KB）
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 1024:
            return True
        else:
            os.remove(filepath)
            print(f"  失败: {filename}.pdf (文件太小，可能是错误页面)")
            return False
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("获取论文列表...")
    slugs = get_paper_slugs()
    print(f"找到 {len(slugs)} 篇论文")
    
    success = 0
    failed = 0
    
    for i, slug in enumerate(slugs, 1):
        print(f"[{i}/{len(slugs)}] 处理: {slug[:50]}...")
        
        pdf_url = get_pdf_url(slug)
        if pdf_url:
            if download_pdf(slug, pdf_url):
                success += 1
            else:
                failed += 1
        else:
            print(f"  无法获取 PDF 链接")
            failed += 1
        
        # 避免请求过快
        time.sleep(0.3)
    
    print(f"\n完成! 成功: {success}, 失败: {failed}")

if __name__ == "__main__":
    main()
