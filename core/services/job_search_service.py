import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import json
import logging

logger = logging.getLogger(__name__)

class JobSearchService:
    def __init__(self, email, password, keyword):
        self.email = email
        self.password = password
        self.keyword = keyword
        self.applications = []
        print(self.applications)
        # Initialize WebDriver with Chrome options
        self.options = Options()
        # self.options.add_argument('--headless')  # Run in headless mode for production
        self.driver = webdriver.Chrome(options=self.options)

    def login_linkedin(self):
        """Login to LinkedIn"""
        try:
            self.driver.get("https://www.linkedin.com/login")
            login_email = self.driver.find_element(By.ID, "username")
            login_email.clear()
            login_email.send_keys(self.email)

            time.sleep(3)
            login_pass = self.driver.find_element(By.ID, "password")
            login_pass.clear()
            login_pass.send_keys(self.password)
            login_pass.send_keys(Keys.RETURN)
            time.sleep(30)
            self.driver.get("https://www.linkedin.com/jobs")
        except Exception as e:
            logger.error(f"Error logging into LinkedIn: {e}")
            raise

    def search_jobs(self):
        """Search for jobs"""
        try:
            keyword_search_box = self.driver.find_element(By.XPATH, "//*[contains(@id, 'jobs-search-box-keyword-id')]")
            keyword_search_box.click()
            keyword_search_box.send_keys(self.keyword)
            keyword_search_box.send_keys(Keys.RETURN)
        except NoSuchElementException as e:
            logger.error(f"Error finding the search box: {e}")
            raise

    def apply_filters(self):
        """Apply filters to job search results"""
        try:
            time.sleep(5)
            parent_element = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
            time.sleep(2)
            child_elements = parent_element.find_elements(By.CLASS_NAME, "scaffold-layout__list-item")

            for child in child_elements:
                try:
                    job_card_container = child.find_element(By.CLASS_NAME, "job-card-container")
                    apply_method_div = job_card_container.find_element(By.CLASS_NAME, "job-card-container__apply-method")
                except NoSuchElementException:
                    child.click()
                    time.sleep(3)
                    # here you need to get the right container details bellow...
                    self.collect_job_info()

        except NoSuchElementException as e:
            logger.error(f"Error applying filters: {e}")
            raise

    def collect_job_info(self):
        """Collect job information and apply"""
        try:
            print("------ ISSUE HERE NOT GETTING THE HTML -------")
            job_title_span = self.driver.find_element(By.CLASS_NAME, "jobs-search__job-details--container")
            job_title = job_title_span.get_attribute("innerHTML")
            print("------------- START HERE ------------------------")
            print(job_title)
            print("------------- END HERE ------------------------")
            time.sleep(30)

            job_description_span = self.driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description-without-tagline")
            job_description = job_description_span.get_attribute("innerHTML")

            self.driver.find_element(By.CLASS_NAME, "jobs-apply-button").click()
            new_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_tab)
            data = {
                "URL": self.driver.current_url,
                "Job Title": job_title,
                "Job Description": job_description
            }
            self.applications.append(data)

            old_tab = self.driver.window_handles[0]
            self.driver.close()
            self.driver.switch_to.window(old_tab)

            with open('job_applications.json', 'a') as json_file:
                json.dump(self.applications, json_file)

            logger.info(f"Successfully applied to job: {job_title}")

        except NoSuchElementException:
            logger.warning("Apply button not found, skipping job")

    def close_session(self):
        """Close the browser session"""
        self.driver.quit()
        logger.info('Browser session closed')

    def apply_to_jobs(self):
        """Apply to job offers"""
        try:
            self.driver.maximize_window()
            self.login_linkedin()
            time.sleep(5)
            self.search_jobs()
            time.sleep(10)
            self.apply_filters()
            time.sleep(3)
            self.collect_job_info()
        finally:
            self.close_session()
