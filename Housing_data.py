import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def fetch_page(url):
    """Tải nội dung HTML từ URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://batdongsan.com.vn/",
        "Origin": "https://batdongsan.com.vn",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Lỗi khi tải trang: {response.status_code}")
        return None


def parse_listing_page(html):
    """Phân tích danh sách bài đăng trên một trang."""
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    listings = soup.select(
        '.js__card.js__card-full-web.pr-container.re__card-full.re__vip-diamond, \
         .js__card.js__card-full-web.pr-container.re__card-full.re__vip-gold, \
         .js__card.js__card-full-web.pr-container.re__card-full.re__vip-silver, \
         .js__card.js__card-full-web.pr-container.re__card-full.re__vip-normal'
    )
    for listing in listings:
        a_tag = listing.find('a')
        if a_tag and 'href' in a_tag.attrs:
            links.append(a_tag['href'])

    return links


def parse_detail_page(html):
    """Phân tích chi tiết bài đăng."""
    soup = BeautifulSoup(html, 'html.parser')
    details = {
        "title": "0", "address": "0", "district": "0", "posting_date": "0",
        "price": "0", "area": "0", "direction": "0", "bedrooms": "0",
        "toilets": "0", "floors": "0", "width_meter": "0", "legal": "0",
        "interior": "0", "entrance_width": "0"
    }

    # Lấy tiêu đề
    title_tag = soup.find(class_='pr-title')
    if title_tag:
        details["title"] = title_tag.text.strip()

    # Lấy thông tin chi tiết
    features = soup.select('.re__pr-specs-content-item')
    for feature in features:
        key_tag = feature.find(class_='re__pr-specs-content-item-title')
        value_tag = feature.find(class_='re__pr-specs-content-item-value')
        if key_tag and value_tag:
            key = key_tag.text.strip()
            value = value_tag.text.strip()

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

    # Lấy địa chỉ
    address_tag = soup.find(class_='re__pr-short-description.js__pr-address')
    if address_tag:
        details["address"] = address_tag.text.strip()

    # Lấy quận/huyện
    district_tag = soup.find('a', class_='re__link-se', attrs={"level": "3"})
    if district_tag:
        details["district"] = district_tag.text.strip()

    # Lấy ngày đăng
    config_items = soup.select('.re__pr-short-info-item.js__pr-config-item')
    for item in config_items:
        title_tag = item.find(class_='title')
        value_tag = item.find(class_='value')
        if title_tag and value_tag and title_tag.text.strip() == "Ngày đăng":
            details["posting_date"] = value_tag.text.strip()

    return details


def crawl_data(base_url, target_count):
    data = []
    links = []
    current_count = 0
    current_page = 650

    while current_count < target_count:
        url = f"{base_url}/p{current_page}"
        print(f"Đang tải trang: {url}")
        page_html = fetch_page(url)
        if not page_html:
            break

        page_links = parse_listing_page(page_html)
        links.extend(page_links)
        current_count = len(links)

        print(f"Đã thu thập được {current_count} link bài đăng.")
        if current_count < target_count:
            current_page += 1
        else:
            break

        time.sleep(2)  # Giảm tải cho server

    # Crawl chi tiết từng bài đăng
    for idx, link in enumerate(links[:target_count]):
        print(f"Đang xử lý bài đăng thứ {idx + 1}")
        detail_html = fetch_page(link)
        if not detail_html:
            continue

        details = parse_detail_page(detail_html)
        data.append(details)
        time.sleep(1)  # Giảm tải cho server

    return data


# Sử dụng
base_url = "https://batdongsan.com.vn/nha-dat-ban-ha-noi"
target_count = int(input("Nhập số lượng bài đăng cần crawl: "))
data = crawl_data(base_url, target_count)

if data:
    df = pd.DataFrame(data)
    df.to_csv('hanoi_real_estate_bs.csv', index=False, encoding='utf-8')
    print("Dữ liệu đã được lưu vào hanoi_real_estate_bs.csv")
else:
    print("Không có dữ liệu để lưu.")
