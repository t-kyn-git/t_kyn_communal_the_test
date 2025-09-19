import asyncio
from playwright.async_api import async_playwright
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as PILImage
import os

OUTPUT_DIR = "screenshot_auth"
EXCEL_FILE = "screenshots.xlsx"

async def run(playwright):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(viewport={"width": 1280, "height": 800})
    page = await context.new_page()

    # 1. ログインページへアクセス
    await page.goto("https://t-kyn-git.github.io/t_kyn_communal_the_test/authcheck.html")
    await page.screenshot(path=f"{OUTPUT_DIR}/00_loggedbefore.png",full_page=True)
    await page.fill("#username", "hogehoge")
    await page.fill("#password", "mogemoge")
    await page.click("text=authcheck")
    await page.wait_for_load_state("networkidle")
    await page.screenshot(path=f"{OUTPUT_DIR}/01_loggedin.png", full_page=True)

    # 2. trial feature クリック
    await page.click("text=trial feature")
    await page.wait_for_timeout(1000)
    await page.screenshot(path=f"{OUTPUT_DIR}/02_trial_feature.png", full_page=True)

    # 3. simple todo list クリック
    await page.click("text=simple todo list")
    await page.wait_for_timeout(1000)
    await page.screenshot(path=f"{OUTPUT_DIR}/03_todo_list.png", full_page=True)

    # 4. 新しいタスク入力欄キャプチャ
    await page.click("#task")  # ← セレクタ調整要
    await page.screenshot(path=f"{OUTPUT_DIR}/04_task_input.png", full_page=True)

    # 5. タスク追加 → キャプチャ
    await page.fill("#task", "テストタスク")
    await page.screenshot(path=f"{OUTPUT_DIR}/04_2_task_input_doing.png", full_page=True)
    await page.click("#add")
    await page.wait_for_timeout(1000)
    await page.screenshot(path=f"{OUTPUT_DIR}/05_task_added.png", full_page=True)

    await browser.close()

def create_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Screenshots"

    screenshots = [
        ("ログイン後", "screenshot_auth/01_loggedin.png"),
        ("trial feature クリック後", "screenshot_auth/02_trial_feature.png"),
        ("simple todo list クリック後", "screenshot_auth/03_todo_list.png"),
        ("新しいタスク入力画面", "screenshot_auth/04_task_input.png"),
        ("追加後の画面", "screenshot_auth/05_task_added.png"),
    ]

    row = 1
    for title, img_path in screenshots:
        ws.cell(row=row, column=1, value=title)
        pil_img = PILImage.open(img_path)
        max_width = 500
        ratio = max_width / pil_img.width
        resized_img = pil_img.resize((int(pil_img.width * ratio), int(pil_img.height * ratio)))
        resized_path = img_path.replace(".png", "_resized.png")
        resized_img.save(resized_path)

        img = Image(resized_path)
        ws.add_image(img, f"B{row}")
        row += 20

    outputfile_dir="docs/publicdocs"
    os.makedirs(outputfile_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, EXCEL_FILE)
    # wb.save(EXCEL_FILE)
    wb.save(excel_path)

# Jupyter/Colab用の実行方法
async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    async with async_playwright() as playwright:
        await run(playwright)
    create_excel()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())