from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

def crawl_data(driver, target_count, file_name):
    data = []
    links = []
    current_count = 0
    current_page = 900

    # Tạo tệp CSV và ghi tiêu đề nếu chưa tồn tại
    try:
        pd.DataFrame(columns=[
            "Title", "Address", "District", "PostingDate", "PostType", "Price", "Area", "Direction", "Bedrooms",
            "Toilets", "Floors", "Width_meters", "Entrancewidth", "Legal", "Interior"
        ]).to_csv(file_name, index=False, mode='x', encoding='utf-8')
    except FileExistsError:
        pass

    while current_count < target_count:
        try:
            driver.set_page_load_timeout(180)  # Tăng thời gian chờ tải trang
            listings = driver.find_elements(By.CSS_SELECTOR,
                '.js__card.js__card-full-web.pr-container.re__card-full.re__vip-diamond, \
                 .js__card.js__card-full-web.pr-container.re__card-full.re__vip-gold, \
                 .js__card.js__card-full-web.pr-container.re__card-full.re__vip-silver, \
                 .js__card.js__card-full-web.pr-container.re__card-full.re__vip-normal'
            )
            print(f"Số bài đăng tìm thấy: {len(listings)}")

            # Lấy danh sách link
            for listing in listings:
                try:
                    link = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    if link:
                        links.append(link)
                except Exception as e:
                    print(f"Không thể lấy link: {e}")
                    continue

            current_count = len(links)
            print(f"Đã thu thập được {current_count} bản ghi.")

            if current_count < target_count:
                current_page += 1  # Tăng số trang hiện tại
                next_page_url = f"https://batdongsan.com.vn/nha-dat-ban-ha-noi/p{current_page}"
                print(f"Đang tải trang {current_page}: {next_page_url}")
                driver.get(next_page_url)  # Mở trang tiếp theo
                time.sleep(5)  # Chờ tải trang

        except Exception as e:
            print(f"Lỗi khi tải trang {current_page}: {e}")
            break

    # Crawl dữ liệu từ từng bài đăng
    for idx, link in enumerate(links[:target_count]):
        print(f"Xử lý bài đăng thứ {idx + 1}")
        try:
            driver.get(link)
            time.sleep(3)  # Chờ tải nội dung trang

            # Lấy tiêu đề
            try:
                title = driver.find_element(By.CLASS_NAME, 'pr-title').text
            except:
                title = "0"

            # Lấy thông tin chi tiết
            features = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')
            details = {
                "address": "0", "district": "0", "posting_date": "0", "post_type": "0", "price": "0", "area": "0", "direction": "0", "bedrooms": "0",
                "toilets": "0", "floors": "0", "width_meter": "0", "legal": "0",
                "interior": "0", "entrance_width": "0"
            }

            for feature in features:
                try:
                    key = feature.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text.strip()
                    value = feature.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text.strip()

                    if "Mức" in key:
                        details["price"] = value
                    elif "Diện tích" in key:
                        details["area"] = value
                    elif "Hướng nhà" in key:
                        details["direction"] = value
                    elif "Số phòng ngủ" in key:
                        details["bedrooms"] = value
                    elif "Số toilet" in key:
                        details["toilets"] = value
                    elif "Pháp lý" in key:
                        details["legal"] = value
                    elif "Nội thất" in key:
                        details["interior"] = value
                    elif "Số tầng" in key:
                        details["floors"] = value
                    elif "Mặt tiền" in key:
                        details["width_meter"] = value
                    elif "Đường vào" in key:
                        details["entrance_width"] = value
                except:
                    continue

            # Lấy địa chỉ
            try:
                details["address"] = driver.find_element(By.CLASS_NAME, 're__pr-short-description.js__pr-address').text.strip()
            except:
                details["address"] = "0"

            # Lấy quận/huyện
            try:
                details["district"] = driver.find_element(By.XPATH, '//a[@class="re__link-se" and @level="3"]').text.strip()
            except:
                details["district"] = "0"

            # Lấy post type
            try:
                details['post_type'] = driver.find_element(By.XPATH, '//a[@class="re__link-se" and @level="4"]').text.strip()
            except:
                details['post_type'] = "0"

            # Lấy ngày đăng
            try:
                config_items = driver.find_elements(By.CLASS_NAME, 're__pr-short-info-item.js__pr-config-item')
                for item in config_items:
                    title_element = item.find_element(By.CLASS_NAME, 'title')
                    if title_element.text.strip() == "Ngày đăng":
                        details["posting_date"] = item.find_element(By.CLASS_NAME, 'value').text.strip()
                        break
            except Exception as e:
                print(f"Lỗi khi lấy ngày đăng: {e}")
                details["posting_date"] = "0"

            # Thêm dữ liệu vào danh sách
            data.append({
                "Title": title,
                **details
            })

            # Lưu vào file sau mỗi 10 mục
            if len(data) % 10 == 0:
                pd.DataFrame(data).to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8')
                data.clear()  # Xóa dữ liệu đã lưu khỏi bộ nhớ

        except Exception as e:
            print(f"Lỗi khi xử lý bài đăng thứ {idx}: {e}")
            continue

    # Lưu dữ liệu còn lại nếu có
    if data:
        pd.DataFrame(data).to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8')

    return

# Main script
url = "https://batdongsan.com.vn/nha-dat-ban-ha-noi/p900"
driver = webdriver.Chrome(options=options)
driver.get(url)

file_name = "HNHousing_price_4.csv"
target_count = int(input("Nhập số lượng bản ghi cần crawl: "))
crawl_data(driver, target_count, file_name)
driver.quit()
print(f"Dữ liệu đã được lưu vào {file_name}")
