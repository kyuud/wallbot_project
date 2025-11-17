import pyautogui
import time

print("Posicione o mouse no local desejado. A posição será exibida em 5 segundos...")
time.sleep(5)
x, y = pyautogui.position()
print(f"Coordenadas do mouse: X={x}, Y={y}")