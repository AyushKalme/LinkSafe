# from selenium import webdriver
# from Screenshot import Screenshot
# import time

# def screehotter(url):
#     driver = None
#     image_name = None  # Initialize image_name outside of try block
#     try:
#         # Ensure the URL starts with http:// or https://
#         if not url.startswith(('http://', 'https://')):
#             url = 'http://' + url  # Default to http if no scheme is provided

#         # Using Chrome with headless mode for Docker compatibility
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--window-size=1920,1080')

#         # Create a driver with options
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get(url)
#         time.sleep(3)  # Allow the page to fully load

#         # Take the screenshot
#         ob = Screenshot.Screenshot()
#         image_name = f"screenshot_{int(time.time())}.png"  # Assign image_name here
#         save_path = "./static/screenshots"
#         file_name = f"{save_path}/{image_name}"

#         # Try capturing the screenshot
#         ob.full_screenshot(driver, save_path=save_path, image_name=image_name, is_load_at_runtime=True, load_wait_time=3)

#         # Delay to allow the screenshot process to complete
#         time.sleep(2)
        
#     except Exception as e:
#         print(f"Error taking screenshot: {e}")
#     finally:
#         if driver:
#             try:
#                 driver.quit()  # Quit instead of close to ensure all browser windows are closed
#             except Exception as e:
#                 print(f"Error closing the browser: {e}")

#     # If an error occurred and image_name was never set, return None
#     if image_name:
#         return f"/static/screenshots/{image_name}"
#     else:
#         return None


from selenium import webdriver
from Screenshot import Screenshot
import time

def screehotter(url):
    driver = None
    image_name = None  # Initialize image_name variable

    try:
        # Ensure the URL starts with http:// or https://
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url  # Default to http if no scheme is provided

        driver = webdriver.Chrome()  # Ensure correct path for chromedriver
        driver.set_window_size(1920, 1080)  # Set window size to capture the visible area
        driver.get(url)
        time.sleep(3)  # Allow the page to load

        # Define the image name and save path
        image_name = f"screenshot_{int(time.time())}.png"
        save_path = "./static/screenshots"
        file_name = f"{save_path}/{image_name}"

        # Initialize the Screenshot object
        ob = Screenshot.Screenshot()

        # Use get_screenshot_as_file() to capture the current viewport (not full page)
        driver.save_screenshot(file_name)  # This captures only the visible part (starting view)

        time.sleep(2)  # Wait for the screenshot to be saved

    except Exception as e:
        print(f"Error taking screenshot: {e}")
    finally:
        if driver:
            try:
                driver.quit()  # Ensure the browser is closed after the process
            except Exception as e:
                print(f"Error closing the browser: {e}")

    # If image_name was set, return the screenshot path, else return None
    if image_name:
        return f"/static/screenshots/{image_name}"
    else:
        return None