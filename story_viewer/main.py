import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def start_new_profile(profile_id):
    req_url = f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start/?automation=1"
    response = requests.get(req_url)
    response_json = response.json()
    print(response_json)
    if 'automation' not in response_json:
        print("Помилка: відповідь не містить інформації про автоматизацію.")
        print(response_json)
        exit()

    port = str(response_json['automation']['port'])
    chrome_driver_path = Service(r'C:\Users\PC\Projects\instagram_production\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.debugger_address = f'127.0.0.1:{port}'
    bot = webdriver.Chrome(service=chrome_driver_path, options=options)
    bot.set_window_size(375, 812)  # Розмір iPhone X
    return bot


def save_credentials(username, password):
    with open("credentials.txt", "w") as file:
        file.write(f"{username}\n{password}")


def load_credentials():
    if not os.path.exists("credentials.txt"):
        return None

    with open("credentials.txt", "r") as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None


def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password


def read_usernames_from_file(file_path):
    with open(file_path, "r") as file:
        usernames = [line.strip() for line in file]
    return usernames

def remove_username_from_file(username, file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != username:
                file.write(line)

def like_stories(usernames):
    profile_id = "162085248"  # Замените на ваш ID профиля
    driver = start_new_profile(profile_id)

    for follower in usernames:
        story_url = f"https://www.instagram.com/stories/{follower}"
        driver.get(story_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        try:
            # Нажатие на первую историю пользователя
            view_story_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div/div[1]/div[1]/section/div[1]/div/div/div/div[2]/div/div[3]/div'))
            )
            view_story_button.click()
            print("[TRUE] User -> " + follower + " has story up.")

            # Переход по историям и лайк на последней
            while True:
                try:
                    next_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][descendant::svg[@aria-label='Далі']]"))
                    )
                    next_button.click()
                except TimeoutException:
                    like_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@role="button"][descendant::svg[@aria-label="Подобається"]]'))
                    )
                    like_button.click()
                    print("Лайк поставлен на последней истории.")
                    break

        except TimeoutException:
            print("[FALSE] User -> " + follower + " has no story up.")

    driver.quit()


if __name__ == "__main__":
    followers_file = "usernames_thirtythreespace.txt"
    usernames = read_usernames_from_file(followers_file)

    like_stories(usernames)