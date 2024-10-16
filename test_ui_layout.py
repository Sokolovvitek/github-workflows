import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import pytest
from selenium.common.exceptions import TimeoutException

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_log.log'),  # Запись логов в файл
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)
logger = logging.getLogger()

# Вспомогательная функция для поиска элемента с ожиданием
def find_element_with_wait(driver, by, value, wait_time=10):
    try:
        return WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        logger.warning(f"Элемент {value} не найден в течение {wait_time} секунд.")
        return None  # Возвращаем None, если элемент не найден

@pytest.fixture(scope="module")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Открытие браузера в максимизированном режиме
    options.add_experimental_option("detach", True)  # Оставляем браузер открытым после теста

    # Инициализация драйвера с ChromeDriverManager
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    yield driver
    # driver.quit()  # Закомментировано для того, чтобы не закрывать браузер

def test_full_page_coverage(browser):
    logger.info("Тест запускается.")
    page_url = "https://kamrad33.github.io/index.html"
    browser.get(page_url)

    # Ожидание полной загрузки страницы
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    # === Проверка всех ссылок ===
    all_links = browser.find_elements(By.TAG_NAME, "a")
    logger.info(f"Найдено {len(all_links)} ссылок для проверки.")
    
    unique_links = {}
    repeated_links = {}

    for link in all_links:
        href = link.get_attribute("href")
        location = link.location
        size = link.size

        if href:
            parsed_url = urlparse(href)
            if parsed_url.scheme and parsed_url.netloc:
                logger.info(f"Корректная ссылка: {href} (позиция: {location}, размер: {size})")

                if href in unique_links:
                    repeated_links[href] = repeated_links.get(href, []) + [link]
                else:
                    unique_links[href] = link
                browser.execute_script("arguments[0].style.border='3px solid green'", link)
            else:
                logger.warning(f"Некорректная ссылка: {href}")
                browser.execute_script("arguments[0].style.border='3px solid red'", link)
        else:
            logger.warning("Пустая ссылка.")
            browser.execute_script("arguments[0].style.border='3px solid red'", link)

    # === Логирование повторяющихся ссылок ===
    for url, links_list in repeated_links.items():
        logger.info(f"Повторяющиеся ссылки на: {url}")
        for link in links_list:
            browser.execute_script("arguments[0].style.border='3px solid orange'", link)

    # === Проверка всех кнопок ===
    buttons = browser.find_elements(By.TAG_NAME, "button")
    logger.info(f"Найдено {len(buttons)} кнопок для проверки.")

    button_logs = []

    for button in buttons:
        button_location = button.location
        button_size = button.size
        button_log = {
            'text': button.text,
            'location': button_location,
            'size': button_size,
            'displayed': button.is_displayed(),
            'enabled': button.is_enabled()
        }
        button_logs.append(button_log)

        # Получение координат с помощью JavaScript
        button_coords = browser.execute_script("var rect = arguments[0].getBoundingClientRect(); return {'x': rect.left, 'y': rect.top};", button)

        if button.is_displayed() and button.text:
            browser.execute_script("arguments[0].style.border='3px solid green'", button)
        else:
            browser.execute_script("arguments[0].style.border='3px solid red'", button)
            if not button.is_displayed():
                logger.warning(f"Скрытая кнопка: {button.text} (координаты: {button_coords})")
            if button.text == "":
                logger.warning("Кнопка без текста")

        # Логирование координат кнопки
        logger.info(f"Кнопка: {button.text}, координаты: {button_coords}, размер: {button_size}, отображаемая: {button.is_displayed()}, доступная: {button.is_enabled()}")

    # === Логирование кнопок ===
    logger.info("Лог кнопок и их состояние:")
    for log in button_logs:
        logger.info(log)

    # === Проверка всех контейнеров ===
    all_containers = browser.find_elements(By.XPATH, "//div | //section | //article")
    logger.info(f"Найдено {len(all_containers)} контейнеров для проверки.")

    for index, container in enumerate(all_containers):
        container_class = container.get_attribute("class")
        container_location = container.location
        container_size = container.size

        logger.info(f"[{index}] Контейнер (класс: {container_class}): позиция {container_location}, размер {container_size}")
        
        # Подсвечиваем контейнер
        browser.execute_script("arguments[0].style.border='2px solid green'", container)

    # === Проверка всех div элементов (включая карусели и main) ===
    all_divs = browser.find_elements(By.XPATH, "//div[contains(@class, '')]")  # Проверка всех div
    logger.info(f"Найдено {len(all_divs)} div элементов для проверки.")

    for div in all_divs:
        links_in_div = div.find_elements(By.TAG_NAME, "a")
        if links_in_div:
            logger.info(f"Внутри div (класс: {div.get_attribute('class')}) найдено {len(links_in_div)} ссылок.")
            for link in links_in_div:
                browser.execute_script("arguments[0].style.border='2px dashed blue'", link)

    # === Проверка div.content ===
    content_divs = browser.find_elements(By.CSS_SELECTOR, "div.content")
    logger.info(f"Найдено {len(content_divs)} div.content для проверки.")

    for content_div in content_divs:
        content_class = content_div.get_attribute("class")
        content_location = content_div.location
        content_size = content_div.size

        logger.info(f"div.content (класс: {content_class}): позиция {content_location}, размер {content_size}")
        browser.execute_script("arguments[0].style.border='2px solid purple'", content_div)

    # === Проверка раздела "Новости" ===
    news_section = find_element_with_wait(browser, By.ID, "news")
    if news_section is None:
        logger.warning("Элемент с ID 'news' не найден. Поиск элемента по классу.")
        news_section = find_element_with_wait(browser, By.CLASS_NAME, "news-section")

    if news_section:
        logger.info("Проверка раздела 'Новости'.")
        news_items = news_section.find_elements(By.CLASS_NAME, "news-item")
        logger.info(f"Найдено {len(news_items)} элементов новостей.")

        for item in news_items:
            # Проверка всех ссылок внутри новостных элементов
            links_in_news = item.find_elements(By.TAG_NAME, "a")
            for link in links_in_news:
                href = link.get_attribute("href")
                if href:
                    logger.info(f"Корректная ссылка в разделе 'Новости': {href}")
                    browser.execute_script("arguments[0].style.border='3px solid green'", link)
                else:
                    logger.warning("Найдена пустая ссылка в разделе 'Новости'.")
                    browser.execute_script("arguments[0].style.border='3px solid yellow'", link)
    else:
        logger.warning("Раздел 'Новости' не найден.")

    # === Проверка фреймов ===
    frames = browser.find_elements(By.TAG_NAME, "iframe")
    logger.info(f"Найдено {len(frames)} фреймов на странице.")

    for index, frame in enumerate(frames):
        browser.switch_to.frame(frame)
        logger.info(f"Фрейм {index + 1}: успешно переключен.")
        try:
            buttons_in_frame = browser.find_elements(By.TAG_NAME, "button")
            if buttons_in_frame:
                logger.info(f"В фрейме {index + 1} найдено {len(buttons_in_frame)} кнопок.")
            else:
                logger.info(f"Фрейм {index + 1}: кнопки не найдены.")
        finally:
            browser.switch_to.default_content()

    # === Проверка выпадающих списков ===
    dropdowns = browser.find_elements(By.TAG_NAME, "select")
    logger.info(f"Найдено {len(dropdowns)} выпадающих списков.")

    for dropdown in dropdowns:
        logger.info(f"Выпадающий список: {dropdown.get_attribute('name')}.")
        try:
            select = Select(dropdown)
            options = select.options
            logger.info(f"Количество опций: {len(options)}.")
        except Exception as e:
            logger.error(f"Ошибка при обработке выпадающего списка: {e}")

    logger.info("Тест завершен.")

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
