import re
import sys
import time
from loguru import logger
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from django.db.utils import IntegrityError
from core.models import LinkedInSession, JobApplication


class UltilityMethods:

    def remove_html_tags(html_content):

        return re.compile(r"<[^>]+>").sub("", html_content)

    def find_dates_using_regex(lst):
        # Define a regex pattern for dates in "Month Day, Year" format
        date_pattern = re.compile(r"\b(?:\w{3,9} \d{1,2}, \d{4})\b")

        for item in lst:
            if date_pattern.search(item):
                return True
        return False


class LinkedinJobSearchServiceAutomation:
    def __init__(self, email, password, keyword):
        self.email = email
        self.password = password
        self.keyword = keyword
        self.applications = []
        # Initialize WebDriver with Chrome options
        self.options = uc.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        # self.options.add_argument('--headless')  # Run in headless mode for production
        self.driver = uc.Chrome(options=self.options)

    def save_cookies(self):
        """Save session cookies to the database"""
        cookies = self.driver.get_cookies()
        LinkedInSession.objects.update_or_create(
            email=self.email, defaults={"cookies": cookies}
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
            sys.stdout.write("No cookies found in the database for this email\n")

    def login_linkedin(self):
        """Login to LinkedIn or reuse saved session"""
        self.driver.get("https://www.linkedin.com/")
        self.load_cookies()
        self.driver.get(
            "https://www.linkedin.com/"
        )  # Apply cookies and check if logged in

        # Wait for a moment to allow any redirects
        time.sleep(5)

        # Check if redirected to the LinkedIn feed, indicating an active session
        current_url = self.driver.current_url
        if "feed" in current_url or "jobs" in current_url:
            sys.stdout.write("[INFORMATION] Logged in using saved session \n")
            return  # Stop further execution of login flow if already logged in

        # If not redirected, proceed with the login process
        sys.stdout.write(
            "[INFORMATION] Session not found or expired, logging in with credentials \n"
        )
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

    def search_jobs(self):  # working well....
        """Search for jobs"""
        # After login, navigate to the jobs page
        self.driver.get("https://www.linkedin.com/jobs")
        try:
            keyword_search_box = self.driver.find_element(
                By.XPATH, "//*[contains(@id, 'jobs-search-box-keyword-id')]"
            )
            time.sleep(3)
            keyword_search_box.click()
            time.sleep(3)
            keyword_search_box.send_keys(self.keyword)
            keyword_search_box.send_keys(Keys.RETURN)
        except NoSuchElementException as e:
            sys.stdout.write(f"[ERROR] Error finding the search box: {e} \n")
            raise

    def apply_filters(self):
        """Apply filters to job search results"""
        try:
            time.sleep(5)
            parent_element = self.driver.find_element(
                By.CLASS_NAME, "scaffold-layout__list-container"
            )
            time.sleep(2)
            child_elements = parent_element.find_elements(
                By.CLASS_NAME, "scaffold-layout__list-item"
            )

            for child in child_elements:
                try:
                    job_card_container = child.find_element(
                        By.CLASS_NAME, "job-card-container"
                    )
                    apply_method_div = job_card_container.find_element(
                        By.CLASS_NAME, "job-card-container__apply-method"
                    )
                except NoSuchElementException:
                    child.click()
                    time.sleep(3)
                    # here you need to get the right container details bellow...
                    self.collect_job_info()

        except NoSuchElementException as e:
            sys.stdout.write(f"[ERROR] Error applying filters: {e} \n")
            raise

    def collect_job_info(self):
        """Collect job information and apply"""
        try:
            # Find job title element
            job_title_span = self.driver.find_element(
                By.CLASS_NAME, "t-24.t-bold.inline"
            )
            job_title = job_title_span.text.strip()

            # Find job description element
            job_description_span = self.driver.find_element(
                By.CLASS_NAME, "jobs-box__html-content.jobs-description-content__text"
            )
            job_description = job_description_span.get_attribute("innerHTML").strip()

            # Sleep to avoid being too fast
            time.sleep(2)

            # Wait for the apply button to be clickable
            try:
                apply_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@class, 'jobs-apply-button') and .//span[text()='Apply']]",
                        )
                    )
                )
            except NoSuchElementException:
                sys.stdout.write("[INFORMATION] Apply button not found, skipping job\n")
                return

            # Click the apply button
            apply_button.click()
            new_tab = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_tab)

            time.sleep(3)

            # Collect job URL
            job_url = self.driver.current_url

            # Log the job processing
            sys.stdout.write(
                f"[INFORMATION] Processing job: {job_title} at {job_url}\n"
            )

            # Find company name element
            try:
                company_name_span = self.driver.find_element(
                    By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name"
                )
                company_name = company_name_span.text.strip()
            except NoSuchElementException:
                sys.stdout.write(
                    "[ERROR] Company name not found, using default value 'Unknown Company'.\n"
                )
                company_name = "Unknown Company"

            # Check if the job with this URL already exists
            try:
                _, created = JobApplication.objects.update_or_create(
                    url=job_url,
                    defaults={
                        "job_title": job_title,
                        "company_name": company_name,
                        "job_description": UltilityMethods.remove_html_tags(
                            job_description
                        ),
                    },
                )
                if created:
                    sys.stdout.write(
                        "[INFORMATION] Added a new job application to the database.\n"
                    )
                else:
                    sys.stdout.write(
                        "[INFORMATION] Updated the existing job application in the database.\n"
                    )

            except IntegrityError as e:
                sys.stdout.write(
                    f"[ERROR] An integrity error occurred: {str(e)}, skipping job.\n"
                )

            # Sleep to avoid being too fast
            time.sleep(2)

            # Close the new tab and switch back to the original tab
            old_tab = self.driver.window_handles[0]
            self.driver.close()
            self.driver.switch_to.window(old_tab)

            sys.stdout.write(
                f"[INFORMATION] Successfully applied to job: {job_title}\n"
            )

        except NoSuchElementException as e:
            sys.stdout.write(
                f"[ERROR] An element was not found: {str(e)}, skipping job.\n"
            )

    def close_session(self):
        """Close the browser session"""
        self.driver.quit()
        sys.stdout.write("[INFORMATION] Browser session closed.\n\n")

    def apply_to_jobs(self):
        """Apply to job offers"""
        try:
            self.driver.maximize_window()
            sys.stdout.write("[INFORMATION] Initialized automation\n")
            self.login_linkedin()
            time.sleep(5)
            self.search_jobs()
            time.sleep(5)
            self.apply_filters()
            time.sleep(3)
            # self.collect_job_info()
        finally:
            sys.stdout.write("[INFORMATION] Automation Ended. :rocket:")

class DjangoJobsSearchAutomation:

    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument('--headless')  # Run in headless mode for production
        self.driver = uc.Chrome(options=self.options)

    def scrape_djangojobs(self):
        sys.stdout.write("[INFORMATION] Initiated DjangoJobs automation \n")

        page_number = 1
        base_url = "https://djangojobs.net"

        while True:
            url = f"{base_url}/jobs/?page={page_number}"
            self.driver.get(url)

            # get full page html
            full_html = self.driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(full_html, "html.parser")

            # Find all anchor tags with href attributes
            all_links = soup.find_all("a", href=True)

            # Filter out job-related URLs and exclude unwanted URLs
            job_urls = {link["href"] for link in all_links if "/jobs/" in link["href"] and "rss" not in link["href"]}

            if not job_urls:
                sys.stdout.write("[INFORMATION] No more job URLs found, exiting pagination loop.\n")
                break  # Exit the loop if no job URLs are found

            # Construct full URLs correctly
            full_job_urls = [
                base_url + url if url.startswith("/") else url for url in job_urls
            ]

            original_window = self.driver.current_window_handle
            for link in full_job_urls:
                # Open a new tab and switch to it
                self.driver.switch_to.new_window("tab")
                self.driver.get(link)
                sys.stdout.write("[INFORMATION] Switched to job detail in a new tab \n")
                
                check_for_date = self.driver.find_elements(By.CLASS_NAME, "float-right")
                dates = [date.text for date in check_for_date]
                is_date = UltilityMethods.find_dates_using_regex(dates)
                if is_date:
                    sys.stdout.write("[INFORMATION] Scrapping the page\n")
                    
                    # get full page html
                    full_html = self.driver.page_source

                    # Parse the HTML with BeautifulSoup
                    soup = BeautifulSoup(full_html, "html.parser")

                    # Extract Job Title
                    job_title_element = soup.find('h2')
                    job_title = job_title_element.get_text(strip=True) if job_title_element else 'Not found'

                    # Extract Company Name
                    company_name = 'Not found'
                    if job_title_element:
                        company_name_element = job_title_element.find('strong')
                        if company_name_element:
                            company_name = company_name_element.get_text(strip=True)

                    # Extract Job Description
                    job_description_elements = soup.find_all('p')
                    job_description_html = ' '.join([str(p) for p in job_description_elements if p.get_text(strip=True)])
                    job_description = UltilityMethods.remove_html_tags(job_description_html)

                    try:
                        _, created = JobApplication.objects.update_or_create(
                            url=link,
                            defaults={
                                "job_title": job_title,
                                "company_name": company_name,
                                "job_description": job_description,
                            },
                        )
                        if created:
                            sys.stdout.write(
                                "[INFORMATION] Added a new job application to the database.\n"
                            )
                        else:
                            sys.stdout.write(
                                "[INFORMATION] Updated the existing job application in the database.\n"
                            )

                    except IntegrityError as e:
                        sys.stdout.write(
                            f"[ERROR] An integrity error occurred: {str(e)}, skipping job.\n"
                        )

                else:
                    sys.stdout.write("[INFORMATION] No job information to scrape\n")

                time.sleep(5)
                sys.stdout.write("[INFORMATION] Closing the tab\n")
                self.driver.close()
                self.driver.switch_to.window(original_window)

            # Increment the page number for the next iteration
            page_number += 1
            sys.stdout.write(f"[INFORMATION] Moving to the next page: {page_number}.\n")