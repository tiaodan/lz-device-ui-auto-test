前提：
from playwright.sync_api import Page, Locator, expect  # playwright官方pthon SDK，Page是页面，Locator是定位器，expect是断言


如何定位：
关键函数：
page.locator("#username") // 使用CSS 选择器，此为通过id获取