from datetime import datetime
import time
import random
from pathlib import *

import gspread
from selenium.webdriver.common.by import By
from openpyxl import load_workbook

from consts import *
from settings import *


def parser():

    while True:

        connect_json = gspread.service_account(filename=CREDENTIALS)

        sheet_google = connect_json.open_by_url(SHEET)
        list_sheet = sheet_google.worksheet(LIST_SHEET)

        shops = [SHOP_1, SHOP_2, SHOP_3, SHOP_4, SHOP_5, SHOP_6, SHOP_7, SHOP_8]

        for shop in shops:

            driver.get(SITE_URL)
            driver.implicitly_wait(40)

            driver.find_element(By.XPATH, INPUT_LOGIN).send_keys(DATA_LOGIN)
            driver.implicitly_wait(40)

            driver.find_element(By.XPATH, INPUT_PASS).send_keys(DATA_PASS)
            driver.implicitly_wait(40)

            driver.find_element(By.XPATH, BUTTON_LOGIN).click()
            driver.implicitly_wait(40)
            time.sleep(2)

            driver.get(shop)
            driver.implicitly_wait(40)

            driver.find_element(By.XPATH, BUTTON_SELECT_FORMAT).click()
            time.sleep(2)

            driver.find_element(By.CSS_SELECTOR, BUTTON_DOWNLOAD).click()

            name_shop = driver.find_element(By.XPATH, GET_NAME_SHOP).text
            time.sleep(10)

            driver.quit()

            date_now = datetime.now().strftime(TYPE_DATA_TIME).replace(DASH, DOT)

            for file in Path(FILE_PATH).rglob(TYPE_FILE):

                workbook = load_workbook(file)
                workbook.active = 0
                sheet_workbook = workbook.active

                number_rows = len(sheet_workbook[COLUMN_A]) + 1

                for i in range(2, number_rows):

                    table_id = sheet_workbook[COLUMN_A + str(i)].value
                    product_name = sheet_workbook[COLUMN_B + str(i)].value
                    product_barcode = sheet_workbook[COLUMN_C + str(i)].value
                    product_sku = sheet_workbook[COLUMN_D + str(i)].value
                    product_id = sheet_workbook[COLUMN_E + str(i)].value
                    product_shipment = float(sheet_workbook[COLUMN_F + str(i)].value.replace(DOT, COMMA))
                    product_sale = float(sheet_workbook[COLUMN_G + str(i)].value.replace(DOT, COMMA))
                    product_refund = float(sheet_workbook[COLUMN_H + str(i)].value.replace(DOT, COMMA))
                    product_defect = float(sheet_workbook[COLUMN_I + str(i)].value.replace(DASH, DOT))
                    product_cost_price = float(sheet_workbook[COLUMN_J + str(i)].value.replace(DASH, DOT))
                    product_price = float(sheet_workbook[COLUMN_K + str(i)].value)
                    product_price_sum = sheet_workbook[COLUMN_L + str(i)].value

                    print(
                        table_id,
                        product_name,
                        product_barcode,
                        product_sku,
                        product_id,
                        product_shipment,
                        product_sale,
                        product_refund,
                        product_defect,
                        product_cost_price,
                        product_price,
                        product_price_sum,
                    )

                    elements_column = list_sheet.col_values(15)
                    last_element = elements_column[-1]
                    index_last_element = elements_column.index(last_element)
                    number_row = index_last_element + 2

                    uniq_number = random.random()

                    list_sheet.update(f'{number_row}:{number_row}',
                                      [
                                          [
                                              name_shop,
                                              date_now,
                                              table_id,
                                              product_name,
                                              product_barcode,
                                              product_sku,
                                              product_id,
                                              product_shipment,
                                              product_sale,
                                              product_refund,
                                              product_defect,
                                              product_cost_price,
                                              product_price,
                                              product_price_sum,
                                              uniq_number
                                              ]
                                      ]
                                      )

                    time.sleep(2)

                os.remove(file)

        time.sleep(86400)


parser()
