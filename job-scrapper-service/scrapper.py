import os
import random
import time
from random import randint

import pandas as pd
import spacy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dbwrapper import DBActions


class Scrapper:
    nlp = None
    db = None

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.db = DBActions()

    def extract_skills(self, nlp_text, skills_file=None):
        noun_chunks = self.nlp(nlp_text).noun_chunks
        raw_tokens = self.nlp.tokenizer(nlp_text)
        tokens = [token.text for token in raw_tokens if not token.is_stop]
        if not skills_file:
            data = pd.read_csv(
                os.path.join(os.path.dirname(__file__), 'data/skills.csv')
            )
        else:
            data = pd.read_csv(skills_file)
        skills = list(data.columns.values)
        skillset = []
        # check for one-grams
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)

        # check for bi-grams and tri-grams
        for token in noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        return [i for i in set([i.lower() for i in skillset])]

    def scrape_skills(self, job_title: str, location: str):
        if self.db.record_exists(job_title):
            record = self.db.get_record(job_title)
            skills = record[3]
            return skills.split()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        skills = []
        skills_list = []
        cnt = 0
        for i in range(0, 2, 1):
            driver.get('https://www.indeed.com/jobs?q=' + job_title + '&l=' + location + '&start=' + str(i))
            driver.implicitly_wait(randint(10, 30))

            for job in driver.find_elements(By.CLASS_NAME, "result"):
                # driver.implicitly_wait(20)
                # time.sleep(randint(1, 4))
                soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')

                for data in soup(['style', 'script']):
                    data.decompose()
                sum_div = job.find_element(By.CLASS_NAME, "job_seen_beacon")
                try:
                    sum_div.click()
                except:
                    close_button = driver.find_element(By.CLASS_NAME, 'popover-x-button-close')[0]
                    close_button.click()
                    sum_div.click()
                job_desc = driver.find_element(By.ID, 'jobDescriptionText').text
                skills_list = self.extract_skills(job_desc)
                cnt = cnt + 1
                if cnt >= 2:
                    break
            if cnt >= 2:
                break
        if len(skills_list) != 0:
            skills.append([job_title, skills_list])
        driver.close()
        self.db.add_to_db(job_title, location, ','.join(skills[0][1]))
        return skills

    def scrape_all_jobs(self):
        job_list = []
        job_dic = {}
        with open('data/Jobs') as f:
            job_titles = f.readlines()

        random.shuffle(job_titles)
        for job_title in job_titles:
            job_title = job_title.strip().lower()
            if len(job_title) == 0:
                return job_list
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            time.sleep(randint(2, 5))
            skills_list = []
            cnt = 0
            for i in range(0, 5, 5):
                driver.get('https://www.indeed.com/jobs?q=' + job_title.strip() + '&l=United%20States&start=' + str(i))
                driver.implicitly_wait(randint(10, 30))
                if cnt > 3:
                    break
                for job in driver.find_elements(By.CLASS_NAME, "result"):
                    driver.implicitly_wait(20)
                    time.sleep(randint(1, 4))
                    soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')

                    for data in soup(['style', 'script']):
                        data.decompose()
                    sum_div = job.find_element(By.CLASS_NAME, "job_seen_beacon")
                    try:
                        sum_div.click()
                    except:
                        close_button = driver.find_element(By.CLASS_NAME, 'popover-x-button-close')[0]
                        close_button.click()
                        sum_div.click()
                    job_desc = driver.find_element(By.ID, 'jobDescriptionText').text
                    sl = self.extract_skills(job_desc)
                    if len(sl) != 0:
                        skills_list.append(sl)
                        cnt = cnt + 1
            if len(skills_list) != 0:
                job_list.append([job_title, skills_list])
            driver.close()

        for job in job_list:
            job_dic[job[0]] = list(set([item for sublist in job[1] for item in sublist]))
            print(job[0], job_dic[job[0]])
