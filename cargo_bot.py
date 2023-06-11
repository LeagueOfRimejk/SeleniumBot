import time

import sys

from selenium import webdriver

from selenium.webdriver.common.by import By


DEFAULT_BROWSER = webdriver.Chrome
ORIGIN_URL = "https://e-cargo.edu.pl"

COURSE_SELECTOR = "div.tab-content table.tablelist tr.row1 td a"
TOPIC_SELECTOR = "table.tablelist tbody tr"
TOPIC_NUMBER = 0

INTERMEDIARY_DELAY = 3.0
STATE = {
    "login": None,      	# Type in login
    "password": "None", 	# Type in password
    "logged_in": False,
    "course_selected": False,
    "topic_selected": False,
}

def try_login(browser: DEFAULT_BROWSER):
    # Login input field
    login_field = browser.find_element(by=By.ID, value="inputLogin")
    
    # Password input field
    password_field = browser.find_element(by=By.ID, value="inputPassword")

    # Fill Credentials
    login_field.send_keys(STATE["login"])
    password_field.send_keys(STATE["password"])

    # Try to LogIn
    login_button = browser.find_element(
        by=By.CSS_SELECTOR,
        value="form button.btn.btn-default"
        )

    # Simulate delay
    time.sleep(INTERMEDIARY_DELAY)

    # Proceed for LogIn
    login_button.click()

    # Change logged_in state
    STATE["logged_in"] = True

    # If LogIn was successful, type in login code manually
    input("> Provide LogIn Code, then\n\t\tPress any key to continue..")

def browse_courses(browser: DEFAULT_BROWSER):
    # Course <a> Tag
    course_anchor = browser.find_element(
        by=By.CSS_SELECTOR, value=COURSE_SELECTOR
        )
    
    # Simulate delay
    time.sleep(INTERMEDIARY_DELAY)

    # Select desired course and proceed further
    course_anchor.click()

    # Change course_selected state
    STATE["course_selected"] = True

def pick_topic(browser: DEFAULT_BROWSER):
    # Search for all available topics
    topics = browser.find_elements(by=By.CSS_SELECTOR, value=TOPIC_SELECTOR)

    # Choose one desired from available topics 
    selected_topic = topics[TOPIC_NUMBER]

    # Find anchor to proceed further
    topic_anchor = selected_topic.find_element(by=By.CSS_SELECTOR, value="td a")

    # Simulate delay
    time.sleep(INTERMEDIARY_DELAY)

    # Select desired topic
    topic_anchor.click()

    # Change topic_selected state
    STATE["topic_selected"] = True

def browse_slides(browser: DEFAULT_BROWSER):
    buttons_selector = "div.buttons.course_buttons"

    # Find Buttons interface
    buttons_interface = browser.find_element(
        by=By.CSS_SELECTOR,
        value=buttons_selector
        )
    
    # Unpack current slide and slides count from string e.g 123/620
    curr_slide, _, slides_count = buttons_interface.find_element(
        by=By.CSS_SELECTOR,
        value="span.position"
        ).text.partition("/")
    
    # Ensure Integer
    curr_slide = int(curr_slide)
    slides_count = int(slides_count)

    # Find next button for looping purpose
    next_button = buttons_interface.find_element(by=By.CSS_SELECTOR, value="button.button.right")

    # Main browsing Loop
    while curr_slide < slides_count:
        # Wait for progress bar to finish
        time.sleep(INTERMEDIARY_DELAY + 4.0)

        # Proceed further
        next_button.click()

        # Update current slide
        curr_slide += 1
        print("Current Slide: ", curr_slide)
        print("Slides Count: ", slides_count)

    # Ensure last slide to be included
    time.sleep(INTERMEDIARY_DELAY + 4.0)

def main(browser: DEFAULT_BROWSER):
    # Instantiate default browser
    running_browser = browser()
    running_browser.get(ORIGIN_URL)

    # Try to login
    try_login(running_browser)

    # If User in not logged in, exit
    if not STATE["logged_in"]:
        sys.exit(1)

    # Select course
    browse_courses(running_browser)

    # If User did not select course, exit
    if not STATE["course_selected"]:
        sys.exit(1)

    # Select topic
    pick_topic(running_browser)

    # If User did not select topic, exit
    if not STATE["topic_selected"]:
        sys.exit(1)

    # Browse slides
    browse_slides(running_browser)
    
if __name__ == "__main__":
    main(DEFAULT_BROWSER)
    sys.exit(0)


