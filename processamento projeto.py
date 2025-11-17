import pyautogui
import pyperclip
import time
import tkinter as tk
import random
from threading import Thread

# Mensagens aleatórias
messages = [
    "The ad should contain more information about the product, or have a more detailed description to spark more interest.",
    "Nothing very interesting in the ad.",
    "Nothing very interesting, but it may be of interest to some people. There's not much to talk about.",
    "Indifferent. It's not something that interests me and I don't think it would interest many other people.",
    "I liked this ad. It would interest other people."
]

teclas_list = [("1", "1", "1", "1", "4"), ("1", "1", "1", "1", "3")]

# Constantes
COORD_X, COORD_Y = 160, 720
WAIT_PAGE_LOAD = 10
WAIT_BETWEEN_ROUTINES = 65

# Flag de controle
stop_flag = False

# Função para clicar e colar mensagem
def click_and_paste_message(x, y, message):
    pyautogui.click(x, y)
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("tab")
    pyautogui.hotkey("space")

# Enviar sequência de números
def send_number(teclas):
    pyautogui.press(teclas, interval=0.3)

# Finalizar a rotina (ex: enviar formulário)
def finalize_routine():
    pyautogui.hotkey("space")

# Função principal com controle de parada
def execute_routine(iterations):
    global stop_flag
    for contador in range(iterations):
        if stop_flag:
            print("⏹️ Execução interrompida pelo usuário.")
            break
        message = random.choice(messages)
        teclas = random.choice(teclas_list)
        print(f"▶️ Iteração {contador+1}/{iterations}")
        print(f"   > Teclas: {teclas}")
        print(f"   > Mensagem: {message}")
        time.sleep(WAIT_PAGE_LOAD)
        send_number(teclas)
        time.sleep(5)
        click_and_paste_message(COORD_X, COORD_Y, message)
        time.sleep(WAIT_BETWEEN_ROUTINES)
        finalize_routine()
    print("✅ Rotina finalizada.")

# Iniciar envio (em uma thread)
def start_sending():
    global stop_flag
    stop_flag = False
    iterations = int(entry_iterations.get())
    Thread(target=execute_routine, args=(iterations,)).start()

# Parar execução
def stop_sending():
    global stop_flag
    stop_flag = True

# Interface gráfica
root = tk.Tk()
root.title("Message Sender")
root.geometry("200x120")

label = tk.Label(root, text="Número de Iterações:")
label.pack()

entry_iterations = tk.Entry(root)
entry_iterations.pack()

start_button = tk.Button(root, text="Iniciar", command=start_sending)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Parar", command=stop_sending)
stop_button.pack(pady=5)

root.mainloop()
