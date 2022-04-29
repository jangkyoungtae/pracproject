import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}

# url_1 = 'https://www.coupang.com/vp/products/833162?itemId=4876307&vendorItemId='
# url_2 = '&isAddedCart='

values = ["5913330976", "80912914914", "70573710102", "70453801357"]
name_list = []
price_list = []
url_list = []
# for i in values:
#     url_full = url_1 + str(i) + url_2
#     url_list.append(url_full)
#
# print(url_list)
for i in range(0, 4):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 크롬창 안뜨게 해줌!!
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.implicitly_wait(3)
    url = 'https://www.coupang.com/vp/products/833162?itemId=4876307&vendorItemId=' + str(values[i]) + '&isAddedCart='
    driver.get(url)
    print(url)
    html = driver.page_source
    data = requests.get(html, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # # contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-price-container > div.prod-price > div > div.prod-sale-price.prod-major-price > span.total-price > strong
    # # contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-buy-header > h2
    trs = soup.select('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0')
    for tr in trs:
        product_name = tr.select_one('div.prod-buy-header > h2').text
        product_price = tr.select_one('div.prod-price-container > div.prod-price > div > div.prod-sale-price.prod-major-price > span.total-price > strong').text
    # product_name = soup.select_one('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-buy-header > h2').text
    # product_price = soup.select_one('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-price-container > div.prod-price > div > div.prod-sale-price.prod-major-price > span.total-price > strong').text

        name_list.append(product_name)
        price_list.append(product_price)

        print(name_list)
        print(price_list)



# excel = openpyxl.Workbook()
# sheet = excel.active
#
# sheet.title = "쿠팡 상품 정보 크롤링하기"
# sheet.append(['상품명', 'OSRP'])
#
# sheet.column_dimensions['A'].width = 60
# sheet.column_dimensions['B'].width = 12
#
# A1_cell = sheet['A1']
# A1_cell.alignment = openpyxl.styles.Alignment(horizontal='center')
# A1_cell.font = openpyxl.styles.Font(color='0055FF')
#
# B1_cell = sheet['B1']
# B1_cell.alignment = openpyxl.styles.Alignment(horizontal='center')
# B1_cell.font = openpyxl.styles.Font(color='0055FF')

# for name, price in zip(product_name, product_price):
#     p_name = name.text
#     p_price = price.text
#
#     sheet.append([p_name, p_price])
#
# excel.save('coupang_item_list.xlsx')