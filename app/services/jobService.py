# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from datetime import datetime

# myFilters = ['react', 'javascript', 'nodejs', 'docker', 'strapi', 'automatisation', 'python', 'next.js']
# jobs_cache = []

# async def start_scrape():
#     global jobs_cache
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--ignore-ssl-errors')
#     options.add_argument("--disable-dev-shm-usage")

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
    
#     try:
#         counter = 1
#         data = []   
#         isNotToday = False
        
#         while not isNotToday:
#             url = f'https://www.free-work.com/fr/tech-it/jobs?page={counter}'
#             driver.get(url)
#             isNotToday = scrape_jobs(driver, data) 
#             counter += 1
             
#         jobs_cache = data
#     except Exception as e:
#         print('Error :', e)

#     finally:
#         print('Finished scraping')
#         driver.quit()

#     return jobs_cache

# def scrape_jobs(driver, data: list) -> bool:
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[1]/div[1]/div/div/div/div/div[1]/strong"))
#     )

#     missions = driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div/div/div[1]/div/div[1]/following-sibling::div')

#     for mission in missions[:-1]:
#         try: 
#             date_publish = mission.find_element(By.CSS_SELECTOR, "time").text.strip()
#             if date_publish != datetime.today().strftime('%d/%m/%Y'):
#                 return True
            
#             title = mission.find_element(By.CSS_SELECTOR, "h2 a").text.strip()
#             company = mission.find_element(By.CSS_SELECTOR, "div.font-bold").text.strip()
#             type = mission.find_element(By.CSS_SELECTOR, "span div.truncate").text.strip()
#             languages = mission.find_elements(By.CSS_SELECTOR, ".tag.bg-brand-75 div.truncate")

#             isFound = False
#             for language in languages:
#                 if language.text.strip().lower() in myFilters:
#                     isFound = True
#                     break
                
#             if type != 'Freelance' or not isFound:
#                 continue
        
#             data.append({
#                 'type': type,
#                 'job': title,
#                 'client': company,
#                 'date': date_publish,
#                 'languages': [language.text.strip() for language in languages[:3]]
#             })
            
#         except Exception as e:
#             print('Error :', e)
#             continue
        
#     return False

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from utils.settings import FILTERS

class JobScraper:
    def __init__(self):
        self.driver = self._init_driver()
        self.jobs_cache = []

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def start_scrape(self):
        try:
            data, counter, isNotToday = [], 1, False

            while not isNotToday:
                url = f'https://www.free-work.com/fr/tech-it/jobs?page={counter}'
                self.driver.get(url)
                isNotToday = self._scrape_jobs(data)
                counter += 1

            self.jobs_cache = data

        except Exception as e:
            print('Error:', e)

        finally:
            print('Finished scraping')
            self.driver.quit()

        return self.jobs_cache

    def _scrape_jobs(self, data: list) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[1]/div[1]/div/div/div/div/div[1]/strong"))
            )
            missions = self.driver.find_elements(By.XPATH, '//*[@id="content"]/div[1]/div[2]/div/div/div[1]/div/div[1]/following-sibling::div')

            for mission in missions[:-1]:
                job = self._extract_job_data(mission)
                if job:
                    data.append(job)

            return any(job['date'] != datetime.today().strftime('%d/%m/%Y') for job in data)

        except Exception as e:
            print('Scraping error:', e)
            return False

    def _extract_job_data(self, mission) -> dict:
        try:
            date_publish = mission.find_element(By.CSS_SELECTOR, "time").text.strip()
            title = mission.find_element(By.CSS_SELECTOR, "h2 a").text.strip()
            company = mission.find_element(By.CSS_SELECTOR, "div.font-bold").text.strip()
            type = mission.find_element(By.CSS_SELECTOR, "span div.truncate").text.strip()
            languages = [lang.text.strip().lower() for lang in mission.find_elements(By.CSS_SELECTOR, ".tag.bg-brand-75 div.truncate")]

            if type != 'Freelance' or not any(lang in FILTERS for lang in languages):
                return None

            return {
                'type': type,
                'job': title,
                'client': company,
                'date': date_publish,
                'languages': languages[:3]
            }

        except Exception as e:
            print('Extraction error:', e)
            return None
