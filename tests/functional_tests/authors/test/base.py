from utils.browser import make_chrome_browser
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By


class AuthorBaseTest(StaticLiveServerTestCase):
    # Primeira coisa a ser executada
    # Cria a base do selenium
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    # Última coisa a ser executada
    # Fecha o navegador
    def tearDown(self):
        self.browser.quit()

    def get_by_placeholder(self, web_element, placeholder: str):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
