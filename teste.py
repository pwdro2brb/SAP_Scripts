import pyautogui
import pyperclip
import subprocess
import time

# ============================================================
# FUNÇÃO PARA TRAZER O SAP PARA FRENTE
# ============================================================
def focar_janela_sap():
    """Traz a janela do SAP para frente usando PowerShell."""
    # Tenta vários nomes possíveis da janela do SAP
    nomes = [
        "SAP Easy Access",
        "Cockpit NF",
        "SAP",
    ]
    for nome in nomes:
        try:
            cmd = f'powershell -command "(New-Object -ComObject WScript.Shell).AppActivate(\'{nome}\')"'
            resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if "True" in resultado.stdout or resultado.returncode == 0:
                print(f"✅ Janela '{nome}' focada!")
                time.sleep(0.5)
                return True
        except:
            pass
    
    print("⚠️ Não conseguiu focar automaticamente.")
    print("   Clique na janela do SAP! Você tem 3 segundos...")
    time.sleep(3)
    return False

# ============================================================
# ALTERNATIVA: Usar pygetwindow para focar a janela
# ============================================================
# pip install pygetwindow
def focar_janela_sap_v2():
    """Traz a janela do SAP para frente usando pygetwindow."""
    try:
        import pygetwindow as gw
        
        # Lista todas as janelas com "SAP" no título
        janelas = gw.getWindowsWithTitle('SAP')
        
        if janelas:
            janela_sap = janelas[0]
            janela_sap.activate()
            time.sleep(0.5)
            print(f"✅ Janela focada: {janela_sap.title}")
            return True
        else:
            print("❌ Nenhuma janela SAP encontrada!")
            return False
    except ImportError:
        print("pygetwindow não instalado. Use: pip install pygetwindow")
        return False
    
# ============================================================
# COORDENADAS (no monitor onde o SAP está)
# ============================================================

def focar_sap():
    """Traz a janela do SAP para frente."""
    nomes = ["SAP Easy Access", "Cockpit NF", "SAP"]
    for nome in nomes:
        try:
            cmd = f'powershell -command "(New-Object -ComObject WScript.Shell).AppActivate(\'{nome}\')"'
            subprocess.run(cmd, shell=True, capture_output=True)
            time.sleep(0.1)
            return
        except:
            pass


def clicar_chekbox(posicao, espera=0.1):
    """Clica em uma posição e aguarda."""
    pyautogui.click(x=posicao[0], y=posicao[1])
    time.sleep(espera)

CHECKBOX_PRIMEIRO   = (2929, 330)

print("\nPASSO teste: Selecionando primeiro registro novamente...")
focar_sap()
clicar_chekbox(CHECKBOX_PRIMEIRO)
clicar_chekbox(CHECKBOX_PRIMEIRO)


print("✅ Registro selecionado!")