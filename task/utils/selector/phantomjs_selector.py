import ast
import warnings
from collections import OrderedDict

from playwright.sync_api import sync_playwright

from task.utils.selector.selector import SelectorABC as FatherSelector

warnings.filterwarnings("ignore")

USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'


class PhantomJSSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug


    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):

        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        context = browser.new_context()
        if headers != '':
            page = context.new_page().set_extra_http_headers(headers)
        else:
            page = context.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        playwright.stop()
        return html

    def get_by_xpath(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, xpath_ext in selector_dict.items():
            result[key] = self.xpath_parse(html, xpath_ext)

        return result

    def get_by_css(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, css_ext in selector_dict.items():
            result[key] = self.css_parse(html, css_ext)

        return result
    
    def get_by_json(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)
        html = html.replace('({"resp', '{"resp').replace('":{}}})', '":{}}}')  # .replace后的代码解决了标普出错
        result = OrderedDict()
        for key, json_ext in selector_dict.items():
            result[key] = self.json_parse(html, json_ext)
            result[key] = result[key].replace('[', '').replace(']', '').replace('"', '') #.replace后代码为了去掉jsonpath检测方式的“[]”

        return result
