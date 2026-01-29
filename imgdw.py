import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import quote
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def optimized_image_download(keyword, count=100):
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        if not os.path.exists(keyword):
            os.makedirs(keyword)
        
        url = f"https://www.bing.com/images/search?q={quote(keyword)}"
        driver.get(url)
        time.sleep(3)
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for i in range(20): 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5) 
            
            if i % 5 == 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
                time.sleep(0.5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                
            last_height = new_height
        
        selectors = [
            "img.mimg",
            "img[src*='bing']",
            "img[class*='img']",
            "img[data-src]",
            "img[src^='http']"
        ]
        
        all_images = []
        for selector in selectors:
            try:
                images = driver.find_elements(By.CSS_SELECTOR, selector)
                all_images.extend(images)
            except:
                pass
        
        unique_images = []
        seen_src = set()
        for img in all_images:
            try:
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and src.startswith('http') and src not in seen_src:
                    unique_images.append(img)
                    seen_src.add(src)
            except:
                pass
        
        image_urls = []
        for img in unique_images[:count*3]: 
            try:
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and src.startswith('http'):
                    if "th?id=" in src:
                        if "&w=" in src:
                            large_src = src.split("&w=")[0] + "&w=1000"
                        else:
                            large_src = src + "&w=1000"
                    else:
                        large_src = src
                    
                    image_urls.append(large_src)
            except Exception as e:
                continue
        
        def download_image(img_url, idx):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.bing.com/',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
                }
                
                response = requests.get(img_url, headers=headers, timeout=15, stream=True)
                
                if response.status_code == 200:
                    content = response.content
                    if len(content) > 5000 or content[:3] in [b'\xff\xd8\xff', b'\x89PNG', b'GIF']:
                        filename = f"{keyword}/{keyword}_{idx:04d}.jpg"
                        with open(filename, "wb") as f:
                            f.write(content)
                        return True
                    
            except Exception as e:
                pass
            
            return False
        
        successful = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            for idx, img_url in enumerate(image_urls[:count*2], 1):
                future = executor.submit(download_image, img_url, idx)
                futures.append(future)
                time.sleep(0.05)  
            
            for future in futures:
                if future.result():
                    successful += 1
        
        
        
        return successful
        
    finally:
        driver.quit()

def download_from_duckduckgo_backup(keyword, count=50):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        url = f"https://duckduckgo.com/?q={quote(keyword)}&iax=images&ia=images"
        driver.get(url)
        time.sleep(3)
        
        for i in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        images = driver.find_elements(By.CSS_SELECTOR, "img.tile--img__img")
        
        successful = 0
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        start_idx = len([f for f in os.listdir(keyword) if f.startswith("{keyword}_")]) + 1
        
        for idx, img in enumerate(images[:count], start=start_idx):
            try:
                src = img.get_attribute("src")
                if src and src.startswith('http'):
                    response = requests.get(src, headers=headers, timeout=10)
                    if response.status_code == 200 and len(response.content) > 5000:
                        with open(f"{keyword}/{keyword}_{idx:04d}.jpg", "wb") as f:
                            f.write(response.content)
                        successful += 1
                    time.sleep(0.3)
            except Exception as e:
                continue
        
        driver.quit()
        return successful
        
    except Exception as e:
        return 0

if __name__ == "__main__":
    keyword = str(input("Nhập từ khóa: "))
    count = 100
    
    start_time = time.time()
    downloaded = optimized_image_download(keyword, count)
    end_time = time.time()
    
    print("Đã tải xong")