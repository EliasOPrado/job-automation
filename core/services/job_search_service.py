# services/job_search_service.py
import time
import json
import sys
from loguru import logger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import logging
from core.models import LinkedInSession, JobApplication

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

    def save_cookies(self):
        """Save session cookies to the database"""
        cookies = self.driver.get_cookies()
        LinkedInSession.objects.update_or_create(
            email=self.email,
            defaults={'cookies': cookies}
        )
        sys.stdout.write("Cookies saved successfully in the database")

    def load_cookies(self):
        """Load session cookies from the database"""
        try:
            session = LinkedInSession.objects.get(email=self.email)
            for cookie in session.cookies:
                self.driver.add_cookie(cookie)
            logger.info("Cookies loaded successfully from the database")
        except LinkedInSession.DoesNotExist:
            logger.info("No cookies found in the database for this email")

    def login_linkedin(self):
        """Login to LinkedIn or reuse saved session"""
        self.driver.get("https://www.linkedin.com/")
        self.load_cookies()
        self.driver.get("https://www.linkedin.com/")  # Apply cookies and check if logged in

        # Wait for a moment to allow any redirects
        time.sleep(5)

        # Check if redirected to the LinkedIn feed, indicating an active session
        current_url = self.driver.current_url
        if "feed" in current_url or "jobs" in current_url:
            sys.stdout.write("Logged in using saved session \n\n")
            return  # Stop further execution of login flow if already logged in

        # If not redirected, proceed with the login process
        sys.stdout.write("Session not found or expired, logging in with credentials \n\n")
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
        self.save_cookies() 


    def search_jobs(self): # working well....
        """Search for jobs"""
        # After login, navigate to the jobs page
        self.driver.get("https://www.linkedin.com/jobs")
        try:
            keyword_search_box = self.driver.find_element(By.XPATH, "//*[contains(@id, 'jobs-search-box-keyword-id')]")
            time.sleep(3)
            keyword_search_box.click()
            time.sleep(3)
            keyword_search_box.send_keys(self.keyword)
            keyword_search_box.send_keys(Keys.RETURN)
        except NoSuchElementException as e:
            sys.stdout.write(f"Error finding the search box: {e} \n\n")
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
            sys.stdout.write(f"Error applying filters: {e} \n\n")
            raise

    def collect_job_info(self):
        """Collect job information and apply"""
        try:
            # Find job title element
            job_title_span = self.driver.find_element(By.CLASS_NAME, "t-24.t-bold.inline")
            job_title = job_title_span.text.strip()

            # Find job description element
            job_description_span = self.driver.find_element(By.CLASS_NAME, "jobs-box__html-content.jobs-description-content__text")
            job_description = job_description_span.get_attribute("innerHTML").strip()
            
            # Sleep to avoid being too fast
            time.sleep(2)
            
            # Wait for the apply button to be clickable
            try:
                apply_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button') and .//span[text()='Apply']]"))
                )
            except NoSuchElementException:
                sys.stdout.write("Apply button not found, skipping job\n\n")
                pass
            
            # Click the apply button
            apply_button.click()
            new_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_tab)

            time.sleep(3)
            # Collect job URL
            job_url = self.driver.current_url
            
            # Find company name element
            try:
                company_name_span = self.driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name")
                company_name = company_name_span.text.strip()
            except NoSuchElementException:
                sys.stdout.write("No such element, adding 'Unknow Name' as default. \n\n")
                company_name = 'Unknown name'
                pass

            # Save the collected data to the Django model
            job_application = JobApplication(
                url=job_url,
                job_title=job_title,
                company_name=company_name,
                job_description=job_description
            )
            job_application.save()
            sys.stdout.write("Added a new job application into database. \n\n")
            
            # Sleep to avoid being too fast
            time.sleep(2)
            
            # Close the new tab and switch back to the original tab
            old_tab = self.driver.window_handles[0]
            self.driver.close()
            self.driver.switch_to.window(old_tab)
            
            logger.info(f"Successfully applied to job: {job_title}")
        
        except NoSuchElementException as e:
            sys.stdout.write(f"An element was not found: {str(e)}, skipping job. \n\n")

    def close_session(self):
        """Close the browser session"""
        self.driver.quit()
        sys.stdout.write('Browser session closed.\n\n')

    def apply_to_jobs(self):
        """Apply to job offers"""
        try:
            self.driver.maximize_window()
            sys.stdout.write("***** Initialized automation ***** \n")
            self.login_linkedin()
            time.sleep(5)
            self.search_jobs()
            time.sleep(5)
            self.apply_filters()
            time.sleep(3)
            # self.collect_job_info()
        finally:
            sys.stdout.write("Automation Ended. :rocket:")