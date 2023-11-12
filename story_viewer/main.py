import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from tqdm import tqdm


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
    chrome_driver_path = Service('/Users/a111/Projects/instagram_production/chromedriver')
    options = webdriver.ChromeOptions()
    options.debugger_address = f'127.0.0.1:{port}'
    bot = webdriver.Chrome(service=chrome_driver_path, options=options)
    bot.set_window_size(375, 812)  # Розмір iPhone X
    return bot

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

def check_next_button(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Далі']")
        print("Кнопка 'Далі' найдена.")
        return next_button
    except NoSuchElementException:
        print("Кнопка 'Далі' не найдена.")
        return None


def like_stories(usernames):
    profile_id = "162085248"
    driver = start_new_profile(profile_id)

    for follower in tqdm(usernames, desc="Прогресс"):
        story_url = f"https://www.instagram.com/stories/{follower}"
        driver.get(story_url)
        print(f"Переход к истории пользователя {follower}.")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        try:
            view_story_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@id, "mount_")]/div/div/div[2]/div/div/div/div[1]/div[1]/section/div[1]/div/div/div/div[2]/div/div[3]/div'))
            )
            view_story_button.click()
            print(f"[TRUE] User -> {follower} has story up.")

            # Ставим лайк на первую историю
            try:
                like_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Подобається']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
                time.sleep(1.5)
                actions = ActionChains(driver)
                actions.move_to_element(like_button).click().perform()
                print(f"Лайк поставлен на первой истории пользователя {follower}.")
            except Exception as e:
                print(f"[ERROR] Не удалось поставить лайк на первой истории пользователя {follower}: {e}")

            # Пролистываем остальные истории
            while check_next_button(driver):
                try:
                    next_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Далі']"))
                    )
                    next_button.click()
                    print("Переход к следующей истории.")
                except StaleElementReferenceException:
                    next_button = check_next_button(driver)
                    if next_button:
                        time.sleep(1)
                        next_button.click()
                    else:
                        print("Не удалось найти кнопку 'Далі' после обработки исключения.")
                time.sleep(0.5)

        except TimeoutException:
            print(f"[FALSE] User -> {follower} has no story up.")

    driver.quit()


if __name__ == "__main__":
    followers_file = "usernames_thirtythreespace.txt"
    usernames = read_usernames_from_file(followers_file)

    like_stories(usernames)