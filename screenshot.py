import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://localhost:8000")
    time.sleep(5)
    
    with open('china_gis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    driver.save_screenshot('screenshots/全国.png')
    print("已截图：全国")
    
    for province in data:
        province_name = province['fence_name']
        try:
            script = f"""
                const provinceName = '{province_name}';
                const province = provinceLayers[provinceName];
                if (province) {{
                    Object.values(provinceLayers).forEach(item => {{
                        map.removeLayer(item.layer);
                    }});
                    map.addLayer(province.layer);
                    map.setView(province.centroid, 6);
                }}
            """
            driver.execute_script(script)
            time.sleep(3)
            driver.save_screenshot(f'screenshots/{province_name}.png')
            print(f"已截图：{province_name}")
        except Exception as e:
            print(f"截图{province_name}失败: {e}")
    
    print("\n所有截图已完成！")
    
finally:
    driver.quit()
