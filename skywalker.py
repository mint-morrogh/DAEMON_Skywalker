from playwright.sync_api import sync_playwright
import logging
import os
import config  # store username and password here
import subprocess

print("Skywalker script started execution.")


# Ensure Playwright browsers are installed/updated
try:
    subprocess.run(["/usr/local/bin/python3", "-m", "playwright", "install"], check=True)
    print("Playwright browsers updated successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error updating Playwright browsers: {e}")
    exit(1)  # Exit if Playwright update fails

# Determine the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
skywalker_log_file_path = os.path.join(script_dir, 'skywalker.log')
mission_log_file_path = os.path.join(script_dir, 'mission.log')

# Configure logging
logging.basicConfig(
    filename=skywalker_log_file_path,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Configure mission logging
mission_logger = logging.getLogger('mission_logger')
mission_logger.setLevel(logging.INFO)
mission_handler = logging.FileHandler(mission_log_file_path)
mission_handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y-%m-%d'))
mission_logger.addHandler(mission_handler)

def logAndConsole(message):
    logging.info(message)
    print(message)

def logMission(title, sub_title):
    mission_message = f"{title}, Subtitle: {sub_title}"
    mission_logger.info(mission_message)

def run(playwright):
    logAndConsole("Launching browser.")
    browser = None  # see if the browser object exists for the finally block
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Slooh
        logAndConsole("Navigating to Slooh website.")
        page.goto("https://www.slooh.com/")
        logAndConsole("Waiting for login button selector.")
        page.wait_for_selector('li[data-data-id="dataItem-l4resz7c"]')
        logAndConsole("Clicking on login button.")
        page.click('li[data-data-id="dataItem-l4resz7c"] a')
        page.wait_for_load_state('networkidle')

        # login creds
        logAndConsole("Filling in login credentials.")
        page.fill('input[name="username"]', config.USERNAME)
        page.fill('input[name="pwd"]', config.PASSWORD)
        logAndConsole("Clicking login button.")
        page.click('button.login-btn')

        # Wait for the specific div element
        logAndConsole("Waiting for post-login indicator to be interactable.")
        page.wait_for_selector('div.jsx-3980422799.link-container:has-text("Guides")', state='visible')
        logAndConsole("Post-login indicator is interactable. Logged in successfully.")
        page.wait_for_load_state('networkidle')

        # Join all missions
        logAndConsole("Checking for join mission buttons.")
        join_buttons = page.query_selector_all('div.join-button:has-text("JOIN MISSION")')
        if not join_buttons:
            logAndConsole("All missions are already joined.")
        else:
            logAndConsole(f"Found {len(join_buttons)} join buttons. Joining missions.")
            for join_button in join_buttons:
                # Find the card parent element to get the title and sub
                card = join_button.evaluate_handle("(element) => element.closest('.time-mission-card')")
                title_element = card.query_selector('.bottom-section .title')
                title = title_element.inner_text().strip() if title_element else "No Title"
                subtitle_element = card.query_selector('.bottom-section .sub-title')
                sub_title = subtitle_element.inner_text().strip() if subtitle_element else "No Sub-title"

                # Log and console the title and sub
                logAndConsole(f"Joining mission: {title}, Subtitle: {sub_title}")
                logMission(title, sub_title)

                join_button.click()
                logAndConsole("Clicked join button, waiting for confirmation selector.")
                page.wait_for_selector('button.jsx-3596058999.button-container:has-text("JOIN MISSION")')
                page.click('button.jsx-3596058999.button-container:has-text("JOIN MISSION")')
                page.wait_for_load_state('networkidle')
                logAndConsole("Waiting for join button to be detached.")
                page.wait_for_selector('button.jsx-3596058999.button-container:has-text("JOIN MISSION")', state='detached')

            logAndConsole("All missions joined successfully.")

    finally:
        if browser:
            logAndConsole("Closing browser.")
            browser.close()

with sync_playwright() as playwright:
    logAndConsole("Starting Playwright script.")
    run(playwright)
    logAndConsole("Playwright script completed.")
