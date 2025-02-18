import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
TARGET = 'https://yourdomane.com'  # Target site URL
ZAP_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxx'  # ZAP API key
ZAP_PROXY = 'http://localhost:8081'  # ZAP proxy server address
ZAP_API_URL = f'{ZAP_PROXY}/JSON'

# Function to send requests to ZAP API
def zap_request(endpoint, params=None):
    if params is None:
        params = {}
    params['apikey'] = ZAP_API_KEY  # Add API key to request parameters
    headers = {'Content-Type': 'application/json'}  # Set content type as JSON
    print(f"Sending request to ZAP API: {endpoint}, parameters: {params}")  # Debug output
    response = requests.get(f'{ZAP_API_URL}/{endpoint}', params=params, headers=headers)
    response.raise_for_status()  # Raise HTTPError if an error occurs
    print(f"Response from ZAP API: {response.text}")  # Debug output
    return response.json()

def main():
    driver = None
    try:
        # Check if OWASP ZAP is available
        try:
            zap_status = zap_request('core/view/version')
            print("ZAP is available, version:", zap_status)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error: {err}")
            return
        except Exception as e:
            print(f"Error connecting to ZAP API: {e}")
            return

        # Launch browser using Selenium
        print("Launching browser...")  # Debug output
        options = webdriver.ChromeOptions()
        options.add_argument(f'--proxy-server={ZAP_PROXY}')  # Configure Selenium to use ZAP proxy
        options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
        options.add_argument('--remote-debugging-port=9222')  # Add remote debugging port
        # Uncomment the line below to disable headless mode for testing
        # options.add_argument('--headless')  # Run in headless mode to avoid UI issues
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(TARGET)
        print("Page opened:", TARGET)  # Debug output

        # Example interaction using Selenium
        try:
            # Найти заголовок h1 на странице
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            )
            print("Заголовок страницы:", header.text)
        except Exception as e:
            print(f"Ошибка при взаимодействии с элементами на странице: {e}")

        # Wait for some time for actions to complete
        time.sleep(5)

        # Start spidering before active scanning
        print(f"Starting spider for {TARGET}")
        spider_response = zap_request('spider/action/scan', {'url': TARGET})
        spider_scan_id = spider_response.get('scan')
        while int(zap_request('spider/view/status', {'scanId': spider_scan_id})['status']) < 100:
            print(f"Spidering {TARGET} is {zap_request('spider/view/status', {'scanId': spider_scan_id})['status']}% complete")
            time.sleep(5)

        # Start passive and active security scanning with ZAP
        print(f"Starting passive and active scanning for {TARGET}")
        zap_request('core/action/accessUrl', {'url': TARGET})
        time.sleep(2)

        # Passive scanning
        print("Waiting for passive scan to complete...")
        while int(zap_request('pscan/view/recordsToScan')['recordsToScan']) > 0:
            print("Records left to scan:", zap_request('pscan/view/recordsToScan')['recordsToScan'])
            time.sleep(5)

        # Active scanning
        print("Starting active scan...")
        scan_response = zap_request('ascan/action/scan', {'url': TARGET})
        scan_id = scan_response.get('scan')
        while int(zap_request('ascan/view/status', {'scanId': scan_id})['status']) < 100:
            status = zap_request('ascan/view/status', {'scanId': scan_id})['status']
            print(f"Active scan of {TARGET}: {status}% complete")
            time.sleep(5)

        print("Scanning complete")

        # Retrieve report of detected vulnerabilities
        alerts = zap_request('core/view/alerts', {'baseurl': TARGET})['alerts']
        for alert in alerts:
            print(f"Vulnerability: {alert['alert']} - Description: {alert['description']}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting the browser: {e}")

if __name__ == "__main__":
    main()
