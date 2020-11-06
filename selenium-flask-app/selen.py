from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


def parse(license):
    res = {}
    res['error'] = False
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['setPageLoadStrategy'] = 'normal'
    opt = webdriver.ChromeOptions()
    opt.add_argument("no-sandbox")
    #opt.add_argument("--user-data-dir=/home/tgbot/yandex/data")
    opt.add_argument("--headless")
    opt.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=opt, desired_capabilities=caps)
    try:
        driver.get('https://fleet.taxi.yandex.ru/drivers/scoring?park=7f641c684ff14b6886e796747158c268&driver_license=' + license)
        body = driver.find_element_by_xpath("//body")
        with open('1.html', 'w') as f:
            text = body.get_attribute('inner_html')
            f.write(text)
        img = driver.take_screenshot()
        img = img.to_base64()
        with open('img.png', 'w') as f:
            f.write(img)
        WevDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_Name, 'main-page__content')))
        sleep(5)
        row_divs = driver.find_elements_by_xpath('//table[@class="details-table"]//tr')
        res['drivers'] = []
        for row in row_divs:
            res['drivers'].append(row['innerText'])
        return res
    except Exception as err:
        res['error'] = True
        res['reason'] = str(err)
    return res


def parse_dolgi(*args):
    return None


def parse_black(*args):
    return None
