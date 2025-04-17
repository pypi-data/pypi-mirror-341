import asyncio
from playwright.async_api import Page
from office_assistant_mcp.log_util import log_debug, log_info, log_error

# 导入必要的函数
from office_assistant_mcp.playwright_util import get_playwright, login_sso


async def open_create_message_plan_page():
    """打开创建短信计划页面，以便创建短信计划"""
    _, _, page = await get_playwright()
    log_debug(f"open_create_customer_group_page:{page}")
    open_url = "https://portrait.yunjiglobal.com/customersystem/plan"
    # 打开客群列表页面
    await page.goto(open_url)
    
    login_result = await login_sso()
    log_debug(f"判断登录结果:{login_result}")
    if login_result == "登录成功":
        # 等待两秒
        await asyncio.sleep(2)
        log_debug(f"重新打开页面")
        await page.goto(open_url)
    elif login_result == "登录失败":
        return "登录失败，请提示用户使用飞书扫码登录"

    return "已进入短信计划列表页面"


async def fill_message_group_id(group_id):
    """创建短信计划，填写和选择指定的客群
    
    Args:
        group_id: 客群ID，格式为数字字符串，例如："1050792"
    """
    _, _, page = await get_playwright()
    
    # 搜索客群ID
    await page.get_by_placeholder("请输入人群ID搜索").click()
    await page.get_by_placeholder("请输入人群ID搜索").fill(group_id)
    # 点击搜索按钮
    await page.locator("i.el-icon-search").first.click()
    
    # 选择客群
    # await page.get_by_text("高质量用户圣牧纯牛奶").click()
    
    return f"已搜索并选择客群ID: {group_id}"


async def fill_message_plan_info(plan_name, send_date, send_time):
    """填写短信计划的标题、发送日期和时间
    
    Args:
        plan_name: 计划名称，格式为字符串，例如："0412高质量用户圣牧纯牛奶"
        send_date: 发送日期，格式为"YYYY-MM-DD"，例如："2025-04-12"
        send_time: 发送时间，格式为"HH:MM:SS"，例如："18:00:00"
    """
    _, _, page = await get_playwright()
    form = page.locator("form").first
    # 填写计划名称
    name_input = form.get_by_role("textbox").first
    log_debug(f"name_input:{name_input}, count:{await name_input.count()}")
    log_debug(f"name_input.is_visible():{await name_input.is_visible()}, is_editable:{await name_input.is_editable()}")
    await name_input.click()
    await name_input.fill(plan_name)
    
    # 设置发送日期和时间
    await page.get_by_role("textbox", name="选择日期").click()
    await page.get_by_role("textbox", name="选择日期").nth(1).click()
    await page.get_by_role("textbox", name="选择日期").nth(1).fill(send_date)
    
    await page.get_by_role("textbox", name="选择时间").click()
    await page.get_by_role("textbox", name="选择时间").press("ControlOrMeta+a")
    await page.get_by_role("textbox", name="选择时间").fill(send_time)
    
    # 点击确定按钮
    await page.get_by_role("button", name="确定").nth(1).click()
    
    # 选择无AB测
    await page.get_by_role("radio", name="无AB测").click()
    
    return f"已填写短信计划基本信息：计划名称={plan_name}，发送时间={send_date} {send_time}"


async def fill_message_content(content, product_id):
    """设置发送短信的文本内容，通过商品id生成并插入商品链接
    
    Args:
        content: 短信内容，格式为字符串，例如："哪吒联名款纯牛奶！单提装送礼优选~圣牧有机纯牛奶10包仅需28.9元＞"
        product_id: 商品ID，格式为数字字符串，例如："962956"
    """
    _, _, page = await get_playwright()
    # 取消App推送勾选
    await page.locator("span.el-checkbox__label:has-text('App推送')").nth(0).click() # 外层有button，只有使用css定位
    await page.get_by_role("button", name="App推送").click()
    await page.locator("span.el-checkbox__label:has-text('短信发送')").nth(0).click()
    
    # 选择短信发送方式
    await page.get_by_role("button", name="短信发送").click()
    await page.get_by_role("radio", name="人工营销短信").click()
    
    # 填写短信内容
    await page.get_by_role("textbox", name="请输入短信内容").click()
    await page.get_by_role("textbox", name="请输入短信内容").fill(content)
    
    # 插入商品链接
    await page.get_by_role("button", name="插入链接").click()
    await page.get_by_role("radio", name="商品详情(唤醒小程序)").click()
    await page.get_by_role("textbox", name="请输入商品id").click()
    await page.get_by_role("textbox", name="请输入商品id").fill(product_id)
    await page.get_by_role("button", name="转换").click()
    await asyncio.sleep(1)
    
    await page.get_by_role("button", name="确 定").click()
    
    return f'已设置短信内容和商品链接：短信内容={content}，商品ID={product_id}。'


async def set_department_info():
    """设置费用归属部门和执行后时间"""
    _, _, page = await get_playwright()
    # 选择费用归属部门
    await page.get_by_role("textbox", name="请选择费用归属部门").click()
    await page.get_by_role("menuitem", name="云集").first.click()
    await page.get_by_text("前台").click()
    await page.get_by_text("云集事业部").click()
    await page.get_by_text("产品运营中心").click()
    await page.get_by_role("menuitem", name="运营组").get_by_role("radio").click()
    
    # 空白地方点击一下
    await page.get_by_role("heading", name="效果追踪").click()
    
    return '已设置默认费用归属部门。请用户人工检查填写的表单，再点击“提交”执行计划！'