from playwright.async_api import async_playwright
import asyncio
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage

# 保存ディレクトリ作成
screenshot_dir = "screenshotsmilk"
os.makedirs(screenshot_dir, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://t-kyn-git.github.io/t_kyn_communal_the_test/subdir/development/tools_babytest001.html"
        await page.goto(url)

        # スクショリスト
        screenshot_files = []

        # 1回目アクセス直後
        path0 = os.path.join(screenshot_dir, "0_before_click.png")
        await page.screenshot(path=path0, full_page=True)
        screenshot_files.append(path0)

        # 「ミルク」ボタンを3回クリックしてスクショ取得
        for i in range(1, 4):
            await page.wait_for_selector("button[onclick*=\"addLog('ミルク')\"]")
            await page.click("button[onclick*=\"addLog('ミルク')\"]")
            await asyncio.sleep(0.5)  # UI更新待ち
            path = os.path.join(screenshot_dir, f"{i}_after_click.png")
            await page.screenshot(path=path, full_page=True)
            screenshot_files.append(path)

        await browser.close()

    # ===== Excel 作成 =====
    wb = Workbook()
    ws = wb.active
    ws.title = "ミルクボタンログ"

    row = 1
    for img_path in screenshot_files:
        if os.path.exists(img_path):
            img = XLImage(img_path)
            img.width = 600
            img.height = 800
            ws.add_image(img, f"A{row}")
            row += 40  # 次の画像の行
        else:
            print(f"画像が存在しません: {img_path}")

    excel_path = "milkbuttonscreenshot_v2.xlsx"
    wb.save(excel_path)
    print(f"Excel 保存完了: {excel_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())