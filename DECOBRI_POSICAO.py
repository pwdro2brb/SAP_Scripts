import pyautogui
import time

print("=" * 45)
print("  INSTRUÇÕES:")
print("  1. Abra o SAP (deixe visível na tela)")
print("  2. Posicione o mouse SOBRE o campo")
print("     de comando do SAP (aquele grifado)")
print("  3. NÃO MEXA O MOUSE!")
print("=" * 45)
print()

for i in range(2, 0, -1):
    print(f"  Capturando posição em {i} segundos...")
    time.sleep(1)

x, y = pyautogui.position()

print()
print("=" * 45)
print(f"  ✅ POSIÇÃO CAPTURADA!")
print(f"")
print(f"     X = {x}")
print(f"     Y = {y}")
print(f"")
print(f"  Copie esta linha para o seu script:")
print(f"")
print(f"     pyautogui.click(x={x}, y={y})")
print("=" * 45)

input("\nPressione ENTER para fechar...")