# -*- coding: utf-8 -*-
import os
import logging
import time
from playwright.sync_api import Playwright, sync_playwright

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尝试使用给定的密码列表登录网站，并在登录失败时尝试多次，直到达到最大尝试次数为止
def run(playwright: Playwright, passwords, max_attempts=3) -> None:
    # 启动 Chromium 浏览器，设置为无头模式（headless=True）
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_timeout(3000)

    for password in passwords:
        attempt = 0  # 当前尝试次数

        while attempt < max_attempts:
            try:
                # 记录开始执行的日志
                logger.info(f"Trying to log in with password: {password}")

                # 访问页面，并等待页面完全加载
                page.goto("https://shell.segfault.net/#/login")
                page.wait_for_timeout(10000)  # 适当调整等待时间

                # 查找按钮并点击
                button_selector = 'span.mdc-button__label:has-text("I\'ve Been Here")'
                page.click(button_selector)
                page.wait_for_timeout(8000)

                # 等待登录框出现
                login_box_selector = 'input[placeholder="Secret..."]'
                page.wait_for_selector(login_box_selector)

                # 填充密码
                page.fill(login_box_selector, password)
                page.wait_for_timeout(6000)

                # 模拟按下回车键
                page.press(login_box_selector, "Enter")
                page.wait_for_timeout(10000)


                # 记录成功登录的日志
                logger.info(f"Successfully logged in with password: {password}")

                # 退出循环
                break
            except Exception as e:
                # 记录异常信息
                logger.error(f"Error during login attempt: {str(e)}")
                
                # 增加尝试次数
                attempt += 1
                
                # 等待一段时间后重试
                time.sleep(2)

        # 记录登录尝试次数
        logger.info(f"Login attempts for password {password}: {attempt}")

        # 如果达到最大尝试次数仍然失败，记录错误信息
        if attempt == max_attempts:
            logger.warning(f"Max login attempts reached for password: {password}")

        # 退出浏览器，准备尝试下一个密码
        browser.close()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.wait_for_timeout(5000)

        # 从环境变量中获取登录凭证，然后调用run函数执行操作
with sync_playwright() as p:
    SEG_LOGIN = os.environ.get("SEG_LOGIN", "").split(",") 
    run(p, SEG_LOGIN)
