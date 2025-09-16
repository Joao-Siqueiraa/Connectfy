import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
import asyncio
from bot import run  # importa a função async do bot.py

running = False

def log(msg):
    txt_log.configure(state='normal')
    txt_log.insert(tk.END, f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")
    txt_log.see(tk.END)
    txt_log.configure(state='disabled')

def worker(total, min_delay, max_delay):
    global running
    try:
        asyncio.run(run(total, min_delay, max_delay, log=log, running_flag=lambda: running))
        log("Execução do bot finalizada com sucesso.")
    except Exception as e:
        log(f"Erro no bot: {e}")
    finally:
        running = False
        btn_start.config(state='normal')
        btn_stop.config(state='disabled')

def start_bot():
    global running
    if running:
        return
    try:
        total = int(ent_total.get())
        min_delay = float(ent_min_delay.get())
        max_delay = float(ent_max_delay.get())
    except ValueError:
        messagebox.showerror("Erro", "Verifique os valores numéricos.")
        return

    running = True
    btn_start.config(state='disabled')
    btn_stop.config(state='normal')
    log("Iniciando automação...")

    t = threading.Thread(target=worker, args=(total, min_delay, max_delay), daemon=True)
    t.start()

def stop_bot():
    global running
    running = False
    log("🛑 Automação interrompida pelo usuário.")

root = tk.Tk()
root.title("Connectify")
root.geometry("480x420")
root.iconbitmap("midia/icone.ico")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill='both', expand=True)

tk.Label(frm, text="Total de convites:").grid(row=0, column=0, sticky='w')
ent_total = tk.Entry(frm)
ent_total.grid(row=0, column=1, sticky='ew')
ent_total.insert(0, "10")

tk.Label(frm, text="Delay mínimo (s):").grid(row=1, column=0, sticky='w')
ent_min_delay = tk.Entry(frm)
ent_min_delay.grid(row=1, column=1, sticky='ew')
ent_min_delay.insert(0, "5")

tk.Label(frm, text="Delay máximo (s):").grid(row=2, column=0, sticky='w')
ent_max_delay = tk.Entry(frm)
ent_max_delay.grid(row=2, column=1, sticky='ew')
ent_max_delay.insert(0, "10")

btn_start = tk.Button(frm, text="Start", width=12, command=start_bot)
btn_start.grid(row=3, column=0, pady=8)

btn_stop = tk.Button(frm, text="Stop", width=12, command=stop_bot, state='disabled')
btn_stop.grid(row=3, column=1, pady=8)

tk.Label(frm, text="Logs:").grid(row=4, column=0, columnspan=2, sticky='w')
txt_log = scrolledtext.ScrolledText(frm, height=12, state='disabled')
txt_log.grid(row=5, column=0, columnspan=2, sticky='nsew')

frm.columnconfigure(1, weight=1)
frm.rowconfigure(5, weight=1)

root.mainloop()
