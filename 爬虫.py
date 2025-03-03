import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ============== 配置区域 ==============
BASE_URL = "https://commons.wikimedia.org"
SEARCH_URL = "https://commons.wikimedia.org/w/index.php?search={}&title=Special:MediaSearch&go=Go&type=image"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
SAVE_DIR = "D:/photos"  # 
MAX_IMAGES = 5            # 
# =====================================

def download_images(search_term):
    # 创建保存目录
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"已创建目录：{SAVE_DIR}")
    
    # 构造搜索URL
    full_url = SEARCH_URL.format(search_term)
    print("正在访问:", full_url)
    
    try:
        search_page = requests.get(full_url, headers=HEADERS)
        search_page.raise_for_status()  #
    except Exception as e:
        print(f"访问失败：{str(e)}")
        return

    soup = BeautifulSoup(search_page.content, "lxml")
    
    # 查找图片链接
    img_links = []
    for img_tag in soup.select("img.sd-image"):
        if len(img_links) >= MAX_IMAGES:
            break
        img_url = urljoin(BASE_URL, img_tag["src"])
        img_links.append(img_url)
        print("发现图片：", img_url)
    
    # 下载图片和元数据
    for i, img_url in enumerate(img_links):
        try:
            print(f"\n正在下载第 {i+1}/{len(img_links)} 张图片...")
            
            # 下载图片
            img_data = requests.get(img_url, headers=HEADERS).content
            filename = os.path.join(SAVE_DIR, f"{search_term}_{i+1}.jpg")
            
            with open(filename, "wb") as f:
                f.write(img_data)
            
            print(f"图片已保存到：{filename}")
            
            # 获取描述信息
            time.sleep(1)  # 延迟
            clean_url = img_url.replace("/thumb/", "/").split("/revision/")[0]
            detail_page = requests.get(clean_url, headers=HEADERS)
            detail_soup = BeautifulSoup(detail_page.content, "lxml")
            
            # 提取描述
            description_div = detail_soup.find("div", class_="wbmi-entityview-description")
            description = description_div.get_text(strip=True) if description_div else "无描述"
            
            # 保存元数据
            with open(filename.replace(".jpg", ".txt"), "w", encoding="utf-8") as f:
                f.write(f"物品名称：{search_term}\n")
                f.write(f"图片地址：{img_url}\n")
                f.write(f"描述信息：{description}\n")
                
        except Exception as e:
            print(f"下载失败：{str(e)}")

if __name__ == "__main__":
    print("=== Wikimedia Commons图片下载器 ===")
    search_term = input("请输入要搜索的英文物品名称：").strip()
    download_images(search_term)
    print("\n所有任务已完成！请检查保存目录。")