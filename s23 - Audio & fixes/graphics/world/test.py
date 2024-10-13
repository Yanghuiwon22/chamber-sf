from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def outo_screenshot_km(start_location, end_location, waypoints):
    browser = webdriver.Chrome()
    url = 'https://map.naver.com/p?c=15.00,0,0,0,dh'
    browser.get(url)

    side_var_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'btn_navbar')])[2]"))
    )
    side_var_button.click()

    car_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'btn_search_tab')])[2]"))
    )
    car_button.click()

    if len(waypoints) != 0:
        for i in range(len(waypoints)):
            waypoints_search = browser.find_element(By.CSS_SELECTOR, '.search_btn_area button:nth-of-type(2)')
            waypoints_search.click()

        search = browser.find_elements(By.CLASS_NAME, "input_search")

        for idx, waypoint in enumerate(waypoints):
            search[idx + 1].send_keys(waypoint)
            time.sleep(2)
            search[idx + 1].send_keys(Keys.RETURN)

        search[-1].send_keys(f"{end_location}")
        time.sleep(1.5)
        search[-1].send_keys(Keys.RETURN)
    else:
        search = browser.find_elements(By.CLASS_NAME, "input_search")
        search[1].send_keys(f"{end_location}")
        time.sleep(1.5)
        search[1].send_keys(Keys.RETURN)

    search[0].send_keys(f"{start_location}")
    time.sleep(2)
    search[0].send_keys(Keys.RETURN)

    time.sleep(1.5)
    load_search = browser.find_element(By.CSS_SELECTOR, '.search_btn_area button:nth-of-type(3)')
    load_search.click()

    time.sleep(3)
    distance_between_locations = browser.find_element(By.CSS_SELECTOR, ".item_distance")
    print(f"총 거리 : {distance_between_locations.text}")

    browser.find_element(By.CSS_SELECTOR, ".sc-agadnx.gzMdch").click()

    time.sleep(5)
    map_img = browser.find_element(By.CLASS_NAME, "mapboxgl-canvas")
    map_img.screenshot('./naver_map.png')

def main():
    start_location = str(input("출발지를 입력하세요. : "))
    end_location = str(input("도착지를 입력하세요. : "))
    waypoint_count = int(input("경유지의 개수는 입력하세요. 없으면 0 입력. : "))
    if waypoint_count > 0:
        waypoints = []
        for i in range(waypoint_count):
            waypoint = str(input("경유지를 입력하세요. : "))
            waypoints.append(waypoint)
    else:
        waypoints = []
    outo_screenshot_km(start_location, end_location, waypoints)

if __name__ == "__main__":
    main()