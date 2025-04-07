from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
import time

user = 'myuser'
password = 'mypassword'

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='myuser',
    password='mypassword',
    database='car_data',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()

# Selenium 설정
driver = webdriver.Chrome()
driver.get("https://auto.danawa.com/newcar/")
time.sleep(3)

car_elements = driver.find_elements(By.CSS_SELECTOR, "li > div.info")

for car in car_elements:
    try:
        # 공통 정보 추출
        img_tag = car.find_element(By.CSS_SELECTOR, "a.image > img")
        img_url = img_tag.get_attribute("src")
        name = img_tag.get_attribute("alt")
        model_id = int(car.find_element(By.CSS_SELECTOR, "a.image").get_attribute("model"))
        brand = name.split()[0]

        # 상세 페이지 URL과 가격 추출
        detail_url = price = None
        try:
            right_box = car.find_element(By.XPATH, "../div[@class='right']")
            price_tag = right_box.find_element(By.CSS_SELECTOR, ".text__price")
            price = price_tag.text.strip() + " 만원" if price_tag else None

            detail_url_tag = right_box.find_element(By.CSS_SELECTOR, ".action > a")
            detail_url = detail_url_tag.get_attribute("href") if detail_url_tag else None
        except:
            pass

        # 스펙 처리
        specs = car.find_elements(By.CSS_SELECTOR, ".spec span")
        car_type = fuel_type = release_date = engine_displacement = efficiency = delivery_period = None
        efficiency_km_per_kwh = total_range_km = battery_capacity_kwh = battery_manufacturer = None

        for spec in specs:
            text = spec.text.strip()

            if "출시" in text:
                release_date = text.replace("출시", "").strip()
            elif "㎞/ℓ" in text:
                efficiency = text
            elif "cc" in text:
                engine_displacement = text
            elif any(x in text for x in ["경차", "SUV", "MPV", "소형", "중형", "준중형", "대형", "상용", "스포츠카"]):
                car_type = text
            elif any(x in text for x in ["가솔린", "디젤", "하이브리드", "전기", "LPG", "수소", "바이퓨얼"]):
                fuel_type = text
            elif "㎞/kWh" in text:
                efficiency_km_per_kwh = text
            elif "총주행거리" in text:
                total_range_km = text
            elif "배터리 용량" in text:
                battery_capacity_kwh = text
            elif "배터리 제조사" in text:
                battery_manufacturer = text
            elif "출고 대기기간" in text:
                delivery_period = text.replace("출고 대기기간 :", "").strip()

        # cars 테이블 삽입
        cursor.execute("""
            INSERT INTO cars (model_id, name, brand, car_type, fuel_type, release_date, image_url, detail_url, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=VALUES(name), brand=VALUES(brand), car_type=VALUES(car_type),
                fuel_type=VALUES(fuel_type), release_date=VALUES(release_date),
                image_url=VALUES(image_url), detail_url=VALUES(detail_url), price=VALUES(price)
        """, (model_id, name, brand, car_type, fuel_type, release_date, img_url, detail_url, price))

        # 전기차 or 일반차
        if fuel_type and "전기" in fuel_type:
            cursor.execute("""
                INSERT INTO ev_specs (model_id, efficiency_km_per_kwh, total_range_km, battery_capacity_kwh, battery_manufacturer)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    efficiency_km_per_kwh=VALUES(efficiency_km_per_kwh),
                    total_range_km=VALUES(total_range_km),
                    battery_capacity_kwh=VALUES(battery_capacity_kwh),
                    battery_manufacturer=VALUES(battery_manufacturer)
            """, (model_id, efficiency_km_per_kwh, total_range_km, battery_capacity_kwh, battery_manufacturer))
        else:
            cursor.execute("""
                INSERT INTO engine_specs (model_id, engine_displacement, efficiency, delivery_period)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    engine_displacement=VALUES(engine_displacement),
                    efficiency=VALUES(efficiency),
                    delivery_period=VALUES(delivery_period)
            """, (model_id, engine_displacement, efficiency, delivery_period))

        print(f"✅ 저장 완료: {name} ({model_id})")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

# 종료 처리
driver.quit()
conn.close()
