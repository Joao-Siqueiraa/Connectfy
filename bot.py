# bot.py
import asyncio
import random
from playwright.async_api import async_playwright

async def run(total_conexoes=10, min_delay=5, max_delay=10, log=print, running_flag=lambda: True):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state="estado.json")
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/mynetwork/")
        await page.wait_for_timeout(5000)
        log("Acessando sugestões de conexão...")

        enviados = 0

        while enviados < total_conexoes:
            buttons = await page.query_selector_all("button:has-text('Conectar')")
            valid_buttons = []

            for btn in buttons:
                try:
                    if await btn.is_visible() and await btn.is_enabled():
                        valid_buttons.append(btn)
                except:
                    continue

            log(f"✅ Botões válidos encontrados: {len(valid_buttons)}")

            for btn in valid_buttons:
                if not running_flag():
                    log("🛑 Bot interrompido pelo usuário.")
                    await browser.close()
                    return

                if enviados >= total_conexoes:
                    break
                try:
                    await btn.scroll_into_view_if_needed()
                    await btn.click()
                    log("👉 Clicou em 'Conectar'.")

                    cancelar = await page.query_selector("span:has-text('Cancelar')")
                    if cancelar:
                        await cancelar.click()
                        log("⚠️ Convite já pendente. Cancelado.")
                        continue

                    try:
                        enviar = await page.wait_for_selector("button:has-text('Enviar agora')", timeout=800)
                        await enviar.click()
                        log("📩 Clicou em 'Enviar agora'.")
                    except:
                        log("✅ Conexão enviada direto (sem janela).")

                    enviados += 1
                    log(f"📊 Total enviados: {enviados}/{total_conexoes}")

                    delay = random.uniform(min_delay, max_delay)
                    log(f"⏳ Aguardando {delay:.1f} segundos...")
                    await page.wait_for_timeout(delay * 1000)

                except Exception as e:
                    log(f"❌ Erro ao clicar: {e}")

            await page.reload()
            await page.wait_for_load_state("load")
            await page.wait_for_timeout(4000)

        await browser.close()
        log("\n🏁 Execução finalizada.")


if __name__ == "__main__":
    # Teste isolado no terminal
    asyncio.run(run(10, 5, 10))
