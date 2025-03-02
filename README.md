# Web Vulnerability Testing Script

This script is used to test a target website for security vulnerabilities using Selenium for browser automation and OWASP ZAP (Zed Attack Proxy) for scanning. It performs automated spidering, passive scanning, and active scanning of the target website

## Prerequisites

- Python (latest version): [Download Python](https://www.python.org/downloads/)
- Google Chrome browser
- OWASP ZAP: [Download OWASP ZAP](https://www.zaproxy.org/download/)
- Required Python libraries:
  - `requests`
  - `selenium`
  - `webdriver-manager`

Install the required libraries by running:

```sh
pip install requests selenium webdriver-manager
```

## Script Configuration

- **TARGET**: The target website URL to scan (e.g., `https://example.com`)
- **ZAP_API_KEY**: The API key for OWASP ZAP
- **ZAP_PROXY**: The address of the ZAP proxy server (default: `http://localhost:8081`)

## How to Run the Script

1. **Launch OWASP ZAP**
   - Ensure the API is enabled and the proxy is running on `localhost:8081`.
   - Obtain the API key from OWASP ZAP and set it in the script.

2. **Configure the Script**
   - Update the `TARGET` and `ZAP_API_KEY` variables as needed.

3. **Run the Script**
   - Save the file as `test_script.py`.
   - Run the script using Python:

   ```sh
   python test_script.py
   ```

   The script will:
   - Launch a Chrome browser through Selenium.
   - Perform a spidering scan on the target website.
   - Conduct passive and active scans using OWASP ZAP.
   - Print detected vulnerabilities in the console.

## Example Output

The script will output the status of the scans and a summary of the vulnerabilities found. Each vulnerability will include its description and risk level.
