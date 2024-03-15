import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import *
from utils.constants import *
from utils.status import *
from utils.utils import build_url


def init_browser(firefox_profile_path: str) -> webdriver.Firefox:
    """
    Initializes the web browser.

    Args:
        firefox_profile_path (str): The path to the Firefox profile logged in to the YouTube account.

    Returns:
        browser (webdriver.Firefox): The initialized web browser.
    """
    # Initialize the Firefox profile
    options: Options = Options()

    # Set headless state of browser
    if get_headless():
        options.add_argument("--headless")

    # Set the profile path
    options.add_argument("-profile")
    options.add_argument(firefox_profile_path)

    # Set the service
    service: Service = Service(GeckoDriverManager().install())

    # Initialize the browser
    browser: webdriver.Firefox = webdriver.Firefox(service=service, options=options)
    return browser


def get_channel_id(browser) -> str:
    """
    Gets the Channel ID of the YouTube Account.

    Args:
        browser (webdriver.Firefox): The web browser.

    Returns:
        channel_id (str): The Channel ID.
    """
    driver = browser
    driver.get("https://studio.youtube.com")
    time.sleep(2)
    channel_id = driver.current_url.split("/")[-1]
    return channel_id


def upload_video(browser, video_path, title, description, is_for_kids) -> str:
    """
    Uploads the video to YouTube.

    Args:
        browser (webdriver.Firefox): The web browser.
        video_path (str): The path to the video file.
        title (str): The title of the video.
        description (str): The description of the video.

    Returns:
        url (str): The URL of the uploaded video.
    """
    try:

        driver = browser
        verbose = get_verbose()

        # Go to youtube.com/upload
        driver.get("https://www.youtube.com/upload")

        # Set video file
        FILE_PICKER_TAG = "ytcp-uploads-file-picker"
        file_picker = driver.find_element(By.TAG_NAME, FILE_PICKER_TAG)
        INPUT_TAG = "input"
        file_input = file_picker.find_element(By.TAG_NAME, INPUT_TAG)
        file_input.send_keys(video_path)

        # Wait for upload to finish
        time.sleep(5)

        # Set title
        textboxes = driver.find_elements(By.ID, YOUTUBE_TEXTBOX_ID)

        title_el = textboxes[0]
        description_el = textboxes[-1]

        if verbose:
            info("\t=> Setting title...")

        title_el.click()
        time.sleep(1)
        title_el.clear()
        title_el.send_keys(title)

        if verbose:
            info("\t=> Setting description...")

        # Set description
        time.sleep(10)
        description_el.click()
        time.sleep(0.5)
        description_el.clear()
        description_el.send_keys(description)

        time.sleep(0.5)

        # Set `made for kids` option
        if verbose:
            info("\t=> Setting `made for kids` option...")

        is_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_MADE_FOR_KIDS_NAME)
        is_not_for_kids_checkbox = driver.find_element(By.NAME, YOUTUBE_NOT_MADE_FOR_KIDS_NAME)

        if not is_for_kids:
            is_not_for_kids_checkbox.click()
        else:
            is_for_kids_checkbox.click()

        time.sleep(0.5)

        # Click next
        if verbose:
            info("\t=> Clicking next...")

        next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
        next_button.click()

        # Click next again
        if verbose:
            info("\t=> Clicking next again...")
        next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
        next_button.click()

        # Wait for 2 seconds
        time.sleep(2)

        # Click next again
        if verbose:
            info("\t=> Clicking next again...")
        next_button = driver.find_element(By.ID, YOUTUBE_NEXT_BUTTON_ID)
        next_button.click()

        # Set as unlisted
        if verbose:
            info("\t=> Setting as unlisted...")

        radio_button = driver.find_elements(By.XPATH, YOUTUBE_RADIO_BUTTON_XPATH)
        radio_button[2].click()

        if verbose:
            info("\t=> Clicking done button...")

        # Click done button
        done_button = driver.find_element(By.ID, YOUTUBE_DONE_BUTTON_ID)
        done_button.click()

        # Wait for 2 seconds
        time.sleep(2)

        # Get latest video
        if verbose:
            info("\t=> Getting video URL...")

        # Get the latest uploaded video URL
        driver.get(f"https://studio.youtube.com/channel/{get_channel_id(browser)}/videos/short")
        time.sleep(2)
        videos = driver.find_elements(By.TAG_NAME, "ytcp-video-row")
        first_video = videos[0]
        anchor_tag = first_video.find_element(By.TAG_NAME, "a")
        href = anchor_tag.get_attribute("href")
        if verbose:
            info(f"\t=> Extracting video ID from URL: {href}")
        video_id = href.split("/")[-2]

        # Build URL
        url = build_url(video_id)

        if verbose:
            success(f" => Uploaded Video: {url}")

        # Close the browser
        driver.quit()

        return url
    except:
        browser.quit()
        return ""
