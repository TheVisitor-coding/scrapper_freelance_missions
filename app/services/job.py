from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def scrape_job():
    try:
        url = 'https://www.free-work.com/fr/tech-it/jobs'
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[1]/div[1]/div/div/div/div/div[1]/strong"))
        )


        time.sleep(5)
        missions = driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div/div/div[1]/div/div[1]/following-sibling::div')

        data = []
        for mission in missions[:-1]:
            try: 
                title = mission.find_element(By.CSS_SELECTOR, "h2 a").text.strip()
                company = mission.find_element(By.CSS_SELECTOR, "div.font-bold").text.strip()
                date_publish = mission.find_element(By.CSS_SELECTOR, "time").text.strip()
                type = mission.find_element(By.CSS_SELECTOR, "span div.truncate").text.strip()
            except Exception as e:
                print('Error :', e)
                continue
            
            data.append({
                'type': type,
                'job': title,
                'client': company,
                'date': date_publish,
            })
            
        driver.quit()
    except Exception as e:
        print('Error :', e)

    finally:
        driver.quit()