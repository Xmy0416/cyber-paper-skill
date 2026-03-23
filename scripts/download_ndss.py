#!/usr/bin/env python3
import os
import subprocess
import time
import re
import urllib.request
import urllib.error

BASE_URL = "https://www.ndss-symposium.org"
PAPER_LIST_URL = f"{BASE_URL}/ndss2026/accepted-papers/"
OUTPUT_DIR = "/home/ubuntu/paper/NDSS_2026"

MAX_RETRIES = 10
REQUEST_DELAY = 2

def get_paper_slugs():
    result = subprocess.run(
        ["curl", "-sL", "--retry", "5", "--connect-timeout", "60", PAPER_LIST_URL],
        capture_output=True, text=True
    )
    urls = re.findall(r'href="(https://www\.ndss-symposium\.org/ndss-paper/[^"]+/)"', result.stdout)
    slugs = [url.split('/')[-2] for url in urls]
    return list(set(slugs))

def get_pdf_url(slug, retries=MAX_RETRIES):
    url = f"{BASE_URL}/ndss-paper/{slug}/"
    
    for attempt in range(retries):
        try:
            result = subprocess.run(
                ["curl", "-sL", "--retry", "3", "--connect-timeout", "60", url],
                capture_output=True, text=True, timeout=120
            )
            
            matches = re.findall(r'wp-content/uploads/([^"]+\.pdf)', result.stdout)
            
            if matches:
                for match in matches:
                    if 'paper' in match.lower():
                        return f"{BASE_URL}/wp-content/uploads/{match}"
                return f"{BASE_URL}/wp-content/uploads/{matches[0]}"
            
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                continue
            return None
            
        except subprocess.TimeoutExpired:
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                continue
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                continue
            return None
    return None

def download_pdf(slug, pdf_url, retries=MAX_RETRIES):
    filename = slug[:100]
    filename = re.sub(r'[^a-zA-Z0-9\-]', '-', filename)
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.pdf")
    
    if os.path.exists(filepath):
        print(f"  跳过: {filename}.pdf (已存在)")
        return True
    
    for attempt in range(retries):
        try:
            print(f"  下载: {filename}.pdf (尝试 {attempt + 1}/{retries})")
            result = subprocess.run(
                ["curl", "-sL", "-o", filepath, "--retry", "3", "--connect-timeout", "60", pdf_url],
                capture_output=True, timeout=300
            )
            
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                if size > 1024:
                    return True
                else:
                    os.remove(filepath)
                    print(f"  重试: {filename}.pdf (文件太小)")
            
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                
        except subprocess.TimeoutExpired:
            print(f"  重试: {filename}.pdf (超时)")
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                continue
        except Exception as e:
            print(f"  重试: {filename}.pdf - {e}")
            if attempt < retries - 1:
                time.sleep(REQUEST_DELAY)
                continue
    
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("获取 NDSS 2026 论文列表...")
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
            for retry in range(5):
                time.sleep(REQUEST_DELAY)
                pdf_url = get_pdf_url(slug, retries=3)
                if pdf_url:
                    if download_pdf(slug, pdf_url):
                        success += 1
                        break
            else:
                failed += 1
        
        time.sleep(REQUEST_DELAY)
    
    print(f"\n完成! 成功: {success}, 失败: {failed}")
    print(f"PDF 保存位置: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
