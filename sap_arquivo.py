import pyautogui
import pyperclip
import subprocess
import time
import re
import os
from PIL import Image

pyautogui.FAILSAFE = True

# ============================================================
# FUNÇÃO PARA TRAZER O SAP PARA FRENTE
# ============================================================


def clicar_chekbox(posicao, espera=0.1):
    """Clica em uma posição e aguarda."""
    pyautogui.click(x=posicao[0], y=posicao[1])
    time.sleep(espera)

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
CAMPO_COMANDO       = (3050, 77)       # Campo de comando do SAP (onde se digita /nZMM180)
CAMPO_EQUIPE_RESP   = (3392, 440)
CAMPO_TIPO_NF       = (3419, 710)
CAMPO_LAYOUT        = (3442, 816)
CHECKBOX_PRIMEIRO   = (2917, 300)
SETA_VERDE          = (2986, 231)
SCROLLBAR_USUARIOS  = (4420, 550)
MEU_NOME            = (3903, 766)# valor original(3863, 934)
BOTAO_OK_USUARIO    = (4370, 1257)
CAMPO_PROTOCOLO     = (4105, 643)
CAMPO_NUMERO        = (4003, 778)
SCROLLBAR_LATERAL   = (4088, 1198)
BOTAO_LAPIS         = (5127, 310)
CAMPO_INPUT_EDITAR  = (4767, 371)
BOTAO_SALVAR        = (5174, 304)
BOTAO_SALVAR_NOVAMENTE = (3509, 718)
LANCAR_MIRO_POSICAO = (4060, 237)  
CAMPO_CTG_NFE       = (3154, 611)
APERTAR_SAIR_CONFERENCIA = (4306,234)  
BOTAO_INICIO_PROCESSO    = (3011, 306)
CAMPO_COLAR_VALOR_SAP    = (3164, 441)
CAMPO_COLAR_PEDIDO       = (3613, 369)
CAMPO_NUMERO_PEDIDO_SAP  = (3640, 846)   # De onde lê o número do pedido
BOTAO_CONDICIONAL_PF_PJ  = (3506, 303)
CAMPO_VERIFICAR_PF_PJ    = (3963, 849)   # Onde verifica se é PF ou PJ
CAMPO_SELECAO_INICIO     = (3151, 408)   # Início da seleção (arrastar)
CAMPO_SELECAO_FIM        = (3167, 563)   # Fim da seleção (arrastar)
BOTAO_APOS_CONDICIONAL   = (3304, 183)
BOTAO_ATUALIZAR_1        = (3267, 80)    # SAP atualiza após clicar
BOTAO_ATUALIZAR_2        = (3161, 183)   # SAP atualiza após clicar
BOTAO_ATUALIZAR_3        = (3795, 642)   # SAP atualiza após clicar
BOTAO_ATUALIZAR_4        = (4206, 1250)  # SAP atualiza após clicar

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def arrastar_scrollbar_lateral(posicao, distancia_x=310):
    """Arrasta a barra de rolagem lateral (horizontal) para a direita."""
    pyautogui.moveTo(x=posicao[0], y=posicao[1])
    time.sleep(0.2)
    pyautogui.drag(distancia_x, 0, duration=1.0)  # ← drag no eixo X, não Y
    time.sleep(0.1)

def arrastar_scrollbar_lateral_voltar(posicao, distancia_x=210):
    """Arrasta a barra de rolagem lateral (horizontal) para a esquerda."""
    pyautogui.moveTo(x=posicao[0], y=posicao[1])
    time.sleep(0.2)
    pyautogui.drag(-distancia_x, 0, duration=1.0)  # ← drag no eixo X negativo para a esquerda
    time.sleep(0.2)

def focar_sap():
    """Traz a janela do SAP para frente."""
    nomes = ["SAP Easy Access", "Cockpit NF", "SAP"]
    for nome in nomes:
        try:
            cmd = f'powershell -command "(New-Object -ComObject WScript.Shell).AppActivate(\'{nome}\')"'
            subprocess.run(cmd, shell=True, capture_output=True)
            time.sleep(0.5)
            return
        except:
            pass

def clicar_e_digitar(posicao, texto):
    """Clica em uma posição e digita o texto via clipboard."""
    pyautogui.click(x=posicao[0], y=posicao[1])
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.3)
    pyperclip.copy(texto)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)

def clicar(posicao, espera=0.3):
    """Clica em uma posição e aguarda."""
    pyautogui.click(x=posicao[0], y=posicao[1])
    time.sleep(espera)

def arrastar_scrollbar(posicao, distancia_y=500):
    """Arrasta a barra de rolagem para baixo."""
    pyautogui.moveTo(x=posicao[0], y=posicao[1])
    time.sleep(0.3)
    pyautogui.drag(0, distancia_y, duration=1.0)
    time.sleep(0.3)

# ============================================================
# INÍCIO DO PROCESSO
# ============================================================
print("=" * 50)
print("  AUTOMAÇÃO ZMM180 - INICIANDO")
print("=" * 50)
print()


# ============================================================
# PASSO 0: FOCAR NA JANELA DO SAP (MONITOR CORRETO)
# ============================================================
print("PASSO 0: Focando na janela do SAP...")
focar_sap()

# Também move o mouse para o monitor do SAP para garantir
pyautogui.moveTo(x=CAMPO_COMANDO[0], y=CAMPO_COMANDO[1])
time.sleep(0.5)
print("✅ Foco no SAP!")

# ============================================================
# PASSO 1: Abrir transação ZMM180
# ============================================================
print("\nPASSO 1: Abrindo ZMM180...")
focar_sap()
clicar(CAMPO_COMANDO)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('delete')
time.sleep(0.1)
pyperclip.copy('/nZMM180')
pyautogui.hotkey('ctrl', 'v')
time.sleep(0.1)
pyautogui.press('enter')
time.sleep(2)
print("✅ ZMM180 aberta!")

# ============================================================
# PASSO 2: Preencher Equipe Resp. com "2"
# ============================================================
print("\nPASSO 2: Preenchendo Equipe Resp....")
focar_sap()
clicar_e_digitar(CAMPO_EQUIPE_RESP, '2')
print("✅ Equipe Resp. = 2")

# ============================================================
# PASSO 3: Preencher Tipo NF com "contratos"
# ============================================================
print("\nPASSO 3: Preenchendo Tipo NF...")
clicar_e_digitar(CAMPO_TIPO_NF, 'contratos')
print("✅ Tipo NF = contratos")

# ============================================================
# PASSO 4: Preencher Layout com "/carlosa"
# ============================================================
print("\nPASSO 4: Preenchendo Layout...")
clicar_e_digitar(CAMPO_LAYOUT, '/carlosa')
print("✅ Layout = /carlosa")

# ============================================================
# PASSO 5: Pressionar F8
# ============================================================
print("\nPASSO 5: Executando relatório (F8)...")
focar_sap()
pyautogui.press('f8')
time.sleep(5)
print("✅ Relatório executado!")

# ============================================================
# PASSO 6: Clicar no checkbox do primeiro registro
# ============================================================
print("\nPASSO 6: Selecionando primeiro registro...")
focar_sap()
clicar(CHECKBOX_PRIMEIRO)
print("✅ Registro selecionado!")

# ============================================================
# PASSO 7: Clicar na seta verde
# ============================================================
print("\nPASSO 7: Clicando na seta verde...")
clicar(SETA_VERDE)
time.sleep(0.1)
print("✅ Janela de usuários aberta!")

# ============================================================
# PASSO 8: Rolar lista de usuários até o final
# ============================================================
print("\nPASSO 8: Rolando lista de usuários...")
arrastar_scrollbar(SCROLLBAR_USUARIOS, distancia_y=500)
# Tenta rolar mais uma vez para garantir
arrastar_scrollbar(
    (SCROLLBAR_USUARIOS[0], SCROLLBAR_USUARIOS[1] + 300),
    distancia_y=300
)
print("✅ Lista carregada!")

# ============================================================
# PASSO 9: Clicar no seu nome
# ============================================================
print("\nPASSO 9: Selecionando seu nome...")
clicar(MEU_NOME)
print("✅ Nome selecionado!")

# ============================================================
# PASSO 10: Confirmar (OK)
# ============================================================
print("\nPASSO 10: Confirmando...")
clicar(BOTAO_OK_USUARIO)
time.sleep(2)
print("✅ Confirmado!")

# ============================================================
# PASSO 11: Clicar no checkbox do primeiro registro (novamente)
# ============================================================
print("\nPASSO 11: Selecionando primeiro registro novamente...")
focar_sap()
clicar_chekbox(CHECKBOX_PRIMEIRO)
clicar_chekbox(CHECKBOX_PRIMEIRO)
print("✅ Registro selecionado!")

# ============================================================
# PASSO 12: Clicar no campo protocolo
# ============================================================
print("\nPASSO 12: Clicando no protocolo...")
focar_sap()
clicar(CAMPO_PROTOCOLO)
time.sleep(0.1)
print("✅ Protocolo clicado!")

# ============================================================
# PASSO 13: Copiar os 6 últimos dígitos
# ============================================================
print("\nPASSO 13: Copiando 6 últimos dígitos...")
clicar(CAMPO_NUMERO)
time.sleep(0.1)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.1)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.1)

numero_completo = pyperclip.paste().strip()
seis_digitos = numero_completo[-6:]
print(f"   Número: {numero_completo}")
print(f"   6 dígitos: {seis_digitos}")
print("✅ Dígitos copiados!")

# ============================================================
# PASSO 14: Rolar página até o final
# ============================================================
print("\nPASSO 14: Rolando página...")
focar_sap()
arrastar_scrollbar_lateral(SCROLLBAR_LATERAL, distancia_x=500)
print("✅ Página carregada!")

# ============================================================
# PASSO 15: Clicar no lápis (editar)
# ============================================================
print("\nPASSO 15: Clicando no lápis...")
clicar(BOTAO_LAPIS)
time.sleep(0.1)
print("✅ Modo edição!")

# ============================================================
# PASSO 16: Colar os 6 dígitos no campo
# ============================================================
print("\nPASSO 16: Preenchendo com 6 dígitos...")
clicar_e_digitar(CAMPO_INPUT_EDITAR, seis_digitos)
print(f"✅ Campo preenchido com '{seis_digitos}'!")

# ============================================================
# PASSO 16.5: arrastar scrollbar lateral para voltar para o final da página
# ============================================================

print("\nPASSO 16.5: Rolando página...")
focar_sap()
arrastar_scrollbar_lateral(SCROLLBAR_LATERAL, distancia_x=310)
print("✅ Página carregada!")

# ============================================================
# PASSO 17: Salvar
# ============================================================
print("\nPASSO 17: Salvando...")
clicar(BOTAO_SALVAR)
time.sleep(1)
print("✅ Salvo!")


# ============================================================
# PASSO 18: Salvar NOVAMENTE
# ============================================================
print("\nPASSO 18: Salvando NOVAMENTE...")
clicar(BOTAO_SALVAR_NOVAMENTE)
time.sleep(1)
print("✅ Salvo!")


# ============================================================
# PASSO 19: arrastar scrollbar lateral para voltar para o final da página
# ============================================================
time.sleep(0.5)
print("\nPASSO 19: Rolando página para o início...")
focar_sap()
arrastar_scrollbar_lateral_voltar(SCROLLBAR_LATERAL, distancia_x=210)
print("✅ Página carregada!")


print("\nPASSO 20: Selecionando primeiro registro novamente...")
focar_sap()
clicar_chekbox(CHECKBOX_PRIMEIRO)
clicar_chekbox(CHECKBOX_PRIMEIRO)
print("✅ Registro selecionado!")


print("\nPASSO 21: Apertando em lançar MIRO...")
focar_sap()
clicar(LANCAR_MIRO_POSICAO)
print("✅ Registro selecionado!")



print("\nPASSO 22: Preenchendo CTG...")
clicar_e_digitar(CAMPO_CTG_NFE, 'AL')
print("✅ Ctg.NF = AL")

print("\nPASSO 23: Executando dados para conferência (Enter)...")
focar_sap()
pyautogui.press('enter')
time.sleep(2)
print("✅ Relatório executado!")

# ============================================================
# CONFIGURAÇÃO DO TESSERACT - VERSÃO DEFINITIVA
# ============================================================
TESSERACT_DISPONIVEL = False
TESSERACT_LANG = 'eng'

TESSERACT_DIR = r'C:\Users\pedro.henrsilva\AppData\Local\Programs\Tesseract-OCR'
TESSERACT_EXE = os.path.join(TESSERACT_DIR, 'tesseract.exe')
TESSDATA_DIR = os.path.join(TESSERACT_DIR, 'tessdata')

os.environ['TESSDATA_PREFIX'] = TESSDATA_DIR

try:
    import pytesseract
    from PIL import Image, ImageChops

    if os.path.exists(TESSERACT_EXE):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE

        if os.path.exists(os.path.join(TESSDATA_DIR, 'por.traineddata')):
            TESSERACT_LANG = 'por'
        elif os.path.exists(os.path.join(TESSDATA_DIR, 'eng.traineddata')):
            TESSERACT_LANG = 'eng'

        img_teste = Image.new('RGB', (200, 50), color='white')
        pytesseract.image_to_string(img_teste, lang=TESSERACT_LANG)

        TESSERACT_DISPONIVEL = True
        print(f"✅ Tesseract OK! Idioma: {TESSERACT_LANG}")
    else:
        print(f"❌ tesseract.exe não encontrado em: {TESSERACT_EXE}")

except Exception as e:
    print(f"❌ Erro ao configurar Tesseract: {e}")
    try:
        os.environ['TESSDATA_PREFIX'] = TESSERACT_DIR
        img_teste = Image.new('RGB', (200, 50), color='white')
        pytesseract.image_to_string(img_teste, lang=TESSERACT_LANG)
        TESSERACT_DISPONIVEL = True
        print(f"✅ Tesseract OK (caminho alternativo)! Idioma: {TESSERACT_LANG}")
    except Exception as e2:
        print(f"❌ Falhou também com caminho alternativo: {e2}")

# ============================================================
# COORDENADAS
# ============================================================
# SAP (MONITOR)
CAMPO_CNPJ_FORNECEDOR = (4082, 315)
CAMPO_CNPJ_GRUPO_MRV  = (4052, 485)
CAMPO_VALOR_SAP       = (3201, 849)

# DOCUMENTO NO EDGE (NOTEBOOK) ← AJUSTE COM O SCRIPT DE COORDENADAS!
AREA_TEXTO_DOCUMENTO = (700, 500)
REGIAO_DOCUMENTO = (100, 150, 1300, 750)

# ============================================================
# FUNÇÕES DE NORMALIZAÇÃO
# ============================================================

def normalizar_cnpj(texto):
    """Remove TODA formatação, deixa só números."""
    if not texto:
        return ''
    return re.sub(r'\D', '', texto.strip())


def normalizar_valor(texto):
    """
    Normaliza um valor monetário para comparação.
    
    Exemplos:
        'R$ 1.234,56'  → '123456'
        '1.234,56'     → '123456'
        '1234,56'      → '123456'
        '1234.56'      → '123456'
        '1,234.56'     → '123456'
    
    Retorna os dígitos puros (centavos inclusos).
    """
    if not texto:
        return ''
    
    limpo = texto.strip()
    limpo = limpo.replace('R$', '').replace('r$', '').strip()
    
    # Formato brasileiro: 1.234,56 (vírgula seguida de 2 dígitos no final)
    if re.search(r',\d{2}$', limpo):
        limpo = limpo.replace('.', '').replace(',', '')
    # Formato americano: 1,234.56 (ponto seguido de 2 dígitos no final)
    elif re.search(r'\.\d{2}$', limpo):
        limpo = limpo.replace(',', '').replace('.', '')
    else:
        limpo = re.sub(r'\D', '', limpo)
    
    limpo = limpo.lstrip('0') or '0'
    return limpo


# ============================================================
# FUNÇÕES DE EXTRAÇÃO
# ============================================================

def extrair_todos_cnpjs(texto):
    """Extrai todos os CNPJs/CPFs de qualquer lugar do texto."""
    if not texto:
        return []

    cnpjs_encontrados = []

    padroes = [
        r'\d{2}[.\s]?\d{3}[.\s]?\d{3}[/.\s]?\d{4}[-.\s]?\d{2}',  # CNPJ
        r'\d{3}[.\s]?\d{3}[.\s]?\d{3}[-.\s]?\d{2}',               # CPF
        r'\d{14}',                                                    # CNPJ puro
        r'\d{11}',                                                    # CPF puro
    ]

    for padrao in padroes:
        matches = re.findall(padrao, texto)
        for match in matches:
            numeros = re.sub(r'\D', '', match)
            if len(numeros) in (11, 14) and numeros not in cnpjs_encontrados:
                cnpjs_encontrados.append(numeros)

    return cnpjs_encontrados


def extrair_todos_valores(texto):
    """
    Extrai todos os valores monetários de um texto.
    Retorna lista de valores normalizados (só dígitos).
    """
    if not texto:
        return []
    
    valores_encontrados = []
    
    padroes = [
        r'R\$\s*[\d.,]+',                       # R$ 1.234,56
        r'\d{1,3}(?:\.\d{3})+,\d{2}',           # 1.234,56 (brasileiro com milhar)
        r'\d+,\d{2}',                             # 1234,56 (brasileiro sem milhar)
        r'\d{1,3}(?:,\d{3})+\.\d{2}',           # 1,234.56 (americano)
        r'\d+\.\d{2}',                            # 1234.56 (americano sem milhar)
    ]
    
    for padrao in padroes:
        matches = re.findall(padrao, texto)
        for match in matches:
            valor_norm = normalizar_valor(match)
            if valor_norm and len(valor_norm) >= 3 and valor_norm not in valores_encontrados:
                valores_encontrados.append(valor_norm)
    
    return valores_encontrados


# ============================================================
# FUNÇÕES DE INTERAÇÃO COM TELAS
# ============================================================

def focar_edge_notebook():
    """Traz o Edge (notebook) para frente."""
    try:
        cmd = 'powershell -command "(New-Object -ComObject WScript.Shell).AppActivate(\'Edge\')"'
        subprocess.run(cmd, shell=True, capture_output=True)
        time.sleep(0.5)
        print("   ✅ Edge focado!")
        return True
    except:
        try:
            cmd = 'powershell -command "(New-Object -ComObject WScript.Shell).AppActivate(\'Microsoft Edge\')"'
            subprocess.run(cmd, shell=True, capture_output=True)
            time.sleep(0.5)
            return True
        except:
            print("   ⚠️ Não conseguiu focar o Edge automaticamente")
            return False


def ler_campo_sap(posicao_campo):
    """Lê um campo do SAP."""
    focar_sap()
    time.sleep(0.3)
    pyperclip.copy('')
    pyautogui.click(x=posicao_campo[0], y=posicao_campo[1])
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)
    return pyperclip.paste().strip()


def sair_transacao_sap():
    """Sai da transação atual no SAP."""
    focar_sap()
    clicar(CAMPO_COMANDO)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.1)
    pyperclip.copy('/n')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(2)
    print("   🚪 Saiu da transação!")


def ocr_com_caminho_forcado(imagem):
    """
    Faz OCR forçando o caminho do tessdata.
    Se pytesseract falhar, tenta via subprocess direto.
    """
    if not TESSERACT_DISPONIVEL:
        return ''

    try:
        config_extra = f'--tessdata-dir "{TESSDATA_DIR}"'
        texto = pytesseract.image_to_string(
            imagem,
            lang=TESSERACT_LANG,
            config=config_extra
        )
        return texto

    except Exception as e:
        print(f"   ⚠️ pytesseract falhou: {e}")
        print(f"   🔄 Tentando via subprocess...")

        try:
            caminho_img = os.path.join(os.environ.get('TEMP', '.'), 'ocr_temp.png')
            caminho_txt = os.path.join(os.environ.get('TEMP', '.'), 'ocr_temp')

            imagem.save(caminho_img)

            subprocess.run(
                [
                    TESSERACT_EXE,
                    caminho_img,
                    caminho_txt,
                    '--tessdata-dir', TESSDATA_DIR,
                    '-l', TESSERACT_LANG
                ],
                capture_output=True, text=True
            )

            with open(caminho_txt + '.txt', 'r', encoding='utf-8') as f:
                texto = f.read()

            os.remove(caminho_img)
            os.remove(caminho_txt + '.txt')

            print(f"   ✅ OCR via subprocess funcionou!")
            return texto

        except Exception as e2:
            print(f"   ❌ Falhou tudo: {e2}")
            return ''


# ============================================================
# FUNÇÃO PRINCIPAL: LER DOCUMENTO COM PARADA ANTECIPADA
# ============================================================

def rolar_e_ler_documento_edge(max_paginas=10, cnpjs_procurados=None, valor_procurado=None):
    """
    Lê documento no Edge, PARANDO assim que encontrar os dados necessários.
    
    Args:
        max_paginas: máximo de páginas para ler via OCR
        cnpjs_procurados: lista de CNPJs (só números) que precisa encontrar
        valor_procurado: valor normalizado (só números) que precisa encontrar
    
    Returns:
        tuple: (conteudo_completo, metodo_usado)
    """
    print("   📄 Focando no Edge (notebook)...")
    focar_edge_notebook()
    time.sleep(1)

    pyautogui.click(x=AREA_TEXTO_DOCUMENTO[0], y=AREA_TEXTO_DOCUMENTO[1])
    time.sleep(0.5)

    # ─── TENTATIVA 1: Texto selecionável (Ctrl+A pega TUDO) ───
    print("   📄 Tentativa 1: Ctrl+A (seleciona todas as páginas)...")
    pyperclip.copy('')

    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.8)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.8)

    conteudo = pyperclip.paste().strip()
    numeros = re.findall(r'\d', conteudo)

    if len(numeros) >= 10:
        print(f"   ✅ Texto completo lido! ({len(conteudo)} chars)")
        pyautogui.click(x=AREA_TEXTO_DOCUMENTO[0], y=AREA_TEXTO_DOCUMENTO[1])

        # Verifica se já tem tudo que precisa
        tem_dados = False
        cnpjs_doc = extrair_todos_cnpjs(conteudo)

        if cnpjs_procurados:
            if any(c in cnpjs_doc for c in cnpjs_procurados):
                tem_dados = True
        elif cnpjs_doc:
            tem_dados = True

        if valor_procurado:
            valores_doc = extrair_todos_valores(conteudo)
            if valor_procurado in valores_doc:
                tem_dados = True

        if tem_dados:
            print(f"   🎯 Dados encontrados no texto!")
            if cnpjs_doc:
                print(f"      CNPJs: {cnpjs_doc}")
            return conteudo, 'texto'
        else:
            print("   ⚠️ Texto lido mas dados não encontrados, tentando OCR...")

    # ─── TENTATIVA 2: OCR página por página com PARADA ANTECIPADA ───
    print("   ⚠️ Documento parece ser IMAGEM ou dados não encontrados no texto.")
    print(f"   📸 Tentativa 2: OCR página por página (máx {max_paginas})...")

    if not TESSERACT_DISPONIVEL:
        print("   ❌ Tesseract não disponível!")
        return conteudo if conteudo else '', 'falha'

    pyautogui.press('escape')
    time.sleep(0.3)
    pyautogui.click(x=AREA_TEXTO_DOCUMENTO[0], y=AREA_TEXTO_DOCUMENTO[1])
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'Home')
    time.sleep(1)

    conteudo_total_ocr = ""
    todos_cnpjs_encontrados = []
    todos_valores_encontrados = []

    for pagina in range(1, max_paginas + 1):
        print(f"\n   📸 Lendo página {pagina}...")
        time.sleep(0.5)

        try:
            screenshot = pyautogui.screenshot(region=REGIAO_DOCUMENTO)

            caminho_temp = os.path.join(
                os.environ.get('TEMP', '.'),
                f'documento_ocr_pag{pagina}.png'
            )
            screenshot.save(caminho_temp)

            texto_pagina = ocr_com_caminho_forcado(screenshot)
            print(f"      Página {pagina}: {len(texto_pagina)} chars extraídos")

            if texto_pagina.strip():
                conteudo_total_ocr += f"\n--- PÁGINA {pagina} ---\n"
                conteudo_total_ocr += texto_pagina

                # Extrai CNPJs desta página
                cnpjs_pagina = extrair_todos_cnpjs(texto_pagina)
                if cnpjs_pagina:
                    print(f"      ✅ CNPJs na página {pagina}: {cnpjs_pagina}")
                    for c in cnpjs_pagina:
                        if c not in todos_cnpjs_encontrados:
                            todos_cnpjs_encontrados.append(c)

                # Extrai valores desta página
                valores_pagina = extrair_todos_valores(texto_pagina)
                if valores_pagina:
                    print(f"      ✅ Valores na página {pagina}: {valores_pagina}")
                    for v in valores_pagina:
                        if v not in todos_valores_encontrados:
                            todos_valores_encontrados.append(v)

                # ════════════════════════════════════════════
                # PARADA ANTECIPADA: já encontrou tudo?
                # ════════════════════════════════════════════
                encontrou_tudo = True

                if cnpjs_procurados:
                    for cnpj in cnpjs_procurados:
                        if cnpj not in todos_cnpjs_encontrados:
                            encontrou_tudo = False
                            break

                if valor_procurado:
                    if valor_procurado not in todos_valores_encontrados:
                        encontrou_tudo = False

                if encontrou_tudo and (cnpjs_procurados or valor_procurado):
                    print(f"\n   🎯 TODOS OS DADOS ENCONTRADOS NA PÁGINA {pagina}!")
                    print(f"      Não precisa ler mais páginas.")
                    return conteudo_total_ocr, 'ocr'

        except Exception as e:
            print(f"      ❌ Erro OCR página {pagina}: {e}")

        # Rola para a próxima página
        screenshot_antes = pyautogui.screenshot(region=REGIAO_DOCUMENTO)
        pyautogui.press('pagedown')
        time.sleep(1)
        screenshot_depois = pyautogui.screenshot(region=REGIAO_DOCUMENTO)

        diff = ImageChops.difference(screenshot_antes, screenshot_depois)
        if not diff.getbbox():
            print(f"   📄 Fim do documento na página {pagina}.")
            break

    if conteudo_total_ocr:
        print(f"\n   ✅ OCR completo: {len(conteudo_total_ocr)} chars totais")
        return conteudo_total_ocr, 'ocr'
    else:
        return '', 'falha'


# ============================================================
# PASSO 20: LER CNPJs DO SAP
# ============================================================
print("\n" + "=" * 50)
print("  VALIDAÇÃO DE CNPJ")
print("=" * 50)

print("\nPASSO 20: Lendo CNPJs do SAP...")
focar_sap()

cnpj_fornecedor_sap = ler_campo_sap(CAMPO_CNPJ_FORNECEDOR)
print(f"   CNPJ Fornecedor: '{cnpj_fornecedor_sap}'")

cnpj_grupo_mrv_sap = ler_campo_sap(CAMPO_CNPJ_GRUPO_MRV)
print(f"   CNPJ Grupo MRV:  '{cnpj_grupo_mrv_sap}'")

cnpj_forn_norm = normalizar_cnpj(cnpj_fornecedor_sap)
cnpj_mrv_norm = normalizar_cnpj(cnpj_grupo_mrv_sap)

# ============================================================
# PASSO 21: LER DOCUMENTO E VALIDAR CNPJ (para na 1ª página que achar!)
# ============================================================
print("\nPASSO 21: Lendo documento no Edge (notebook)...")

conteudo_documento, metodo = rolar_e_ler_documento_edge(
    max_paginas=10,
    cnpjs_procurados=[cnpj_forn_norm, cnpj_mrv_norm],
    valor_procurado=None  # ainda não temos o valor neste passo
)

if metodo == 'falha' or not conteudo_documento:
    print("\n" + "=" * 50)
    print("  ❌ PROTOCOLO NÃO PODE SER FATURADO!")
    print("     Não foi possível ler o documento.")
    print("=" * 50)
    focar_sap()
    sair_transacao_sap()
    exit()

print(f"\n   Método usado: {metodo.upper()}")

# ============================================================
# PASSO 22: COMPARAR CNPJs
# ============================================================
print("\nPASSO 22: Comparando CNPJs...")

cnpjs_no_documento = extrair_todos_cnpjs(conteudo_documento)
print(f"   CNPJs no documento: {cnpjs_no_documento}")

fornecedor_ok = cnpj_forn_norm in cnpjs_no_documento
grupo_mrv_ok = cnpj_mrv_norm in cnpjs_no_documento

print(f"   Fornecedor {cnpj_forn_norm}: {'✅' if fornecedor_ok else '❌'}")
print(f"   Grupo MRV  {cnpj_mrv_norm}:  {'✅' if grupo_mrv_ok else '❌'}")

focar_sap()

if not (fornecedor_ok and grupo_mrv_ok):
    print("\n" + "=" * 50)
    print("  ❌ PROTOCOLO NÃO PODE SER FATURADO, CNPJS DIVERGENTES!")
    if not fornecedor_ok:
        print(f"     Fornecedor {cnpj_forn_norm} NÃO encontrado no documento")
    if not grupo_mrv_ok:
        print(f"     Grupo MRV {cnpj_mrv_norm} NÃO encontrado no documento")
    print("=" * 50)
    sair_transacao_sap()
    exit()

print("\n  ✅ CNPJs VALIDADOS!")

# ============================================================
# PASSO 23: SAIR DA TELA DE CONFERÊNCIA (botão X)
# ============================================================
print("\nPASSO 23: Apertando no X para sair da tela de conferência...")
focar_sap()
clicar(APERTAR_SAIR_CONFERENCIA)
time.sleep(1)
print("✅ Saiu da tela de conferência!")

# ============================================================
# PASSO 24: LER O VALOR DO SAP
# ============================================================
print("\nPASSO 24: Lendo valor do SAP...")
focar_sap()

valor_sap_raw = ler_campo_sap(CAMPO_VALOR_SAP)
valor_sap_norm = normalizar_valor(valor_sap_raw)
print(f"   Valor SAP (original):    '{valor_sap_raw}'")
print(f"   Valor SAP (normalizado): '{valor_sap_norm}'")

# ============================================================
# PASSO 25: COMPARAR VALOR COM O DOCUMENTO
#           (reutiliza o conteúdo já lido no PASSO 21!)
# ============================================================
print("\nPASSO 25: Comparando valor com o documento...")

valores_no_documento = extrair_todos_valores(conteudo_documento)
print(f"   Valores encontrados no documento: {valores_no_documento}")

valor_encontrado = valor_sap_norm in valores_no_documento

if valor_encontrado:
    print(f"   ✅ Valor {valor_sap_raw} encontrado no documento!")
    print("\n" + "=" * 50)
    print("  ✅ VALOR VALIDADO! Pode continuar o faturamento.")
    print("=" * 50)
    # ... continua o processo de faturamento ...
else:
    print(f"   ❌ Valor {valor_sap_raw} NÃO encontrado no documento!")
    print("\n" + "=" * 50)
    print("  ❌ PROTOCOLO NÃO PODE SER FATURADO!")
    print(f"     Valor do SAP: {valor_sap_raw} ({valor_sap_norm})")
    print(f"     Valores no documento: {valores_no_documento}")
    print("     VALOR DIVERGENTE!")
    print("=" * 50)
    focar_sap()
    sair_transacao_sap()

# ============================================================
# PASSO 26: Clicar no botão de início do processo
# ============================================================
print("\nPASSO 26: Clicando no botão de início...")
focar_sap()
clicar(BOTAO_INICIO_PROCESSO)
time.sleep(1)
print("✅ Botão clicado!")

# ============================================================
# PASSO 27: Colar o valor do SAP (já lido no PASSO 24)
# ============================================================
print("\nPASSO 27: Colando valor do SAP...")
focar_sap()
clicar_e_digitar(CAMPO_COLAR_VALOR_SAP, valor_sap_raw)
print(f"✅ Valor colado: '{valor_sap_raw}'")

# ============================================================
# PASSO 28: Ler número do pedido e colar últimos 6 dígitos + "-C"
# ============================================================
print("\nPASSO 28: Lendo número do pedido...")
focar_sap()

numero_pedido_raw = ler_campo_sap(CAMPO_NUMERO_PEDIDO_SAP)
print(f"   Número do pedido completo: '{numero_pedido_raw}'")

# Extrai só os números do pedido
numero_pedido_limpo = re.sub(r'\D', '', numero_pedido_raw)

# Pega os últimos 6 dígitos e adiciona "-C"
ultimos_6_pedido = numero_pedido_limpo[-6:]
valor_pedido_formatado = f"{ultimos_6_pedido}-C"

print(f"   Últimos 6 dígitos: '{ultimos_6_pedido}'")
print(f"   Valor formatado:   '{valor_pedido_formatado}'")

# Cola no campo
clicar_e_digitar(CAMPO_COLAR_PEDIDO, valor_pedido_formatado)
print(f"✅ Pedido colado: '{valor_pedido_formatado}'")

# ============================================================
# PASSO 29: Verificar se é PF ou PJ e agir conforme
# ============================================================
print("\nPASSO 29: Verificando se é PF ou PJ...")
focar_sap()

tipo_pf_pj = ler_campo_sap(CAMPO_VERIFICAR_PF_PJ)
print(f"   Tipo encontrado: '{tipo_pf_pj}'")

if 'PF' in tipo_pf_pj.upper():
    # ─── É PF: não faz nada ───
    print("   📋 É PF → Não faz nada, segue o fluxo.")
    
    # Apenas clica no botão
    clicar(BOTAO_CONDICIONAL_PF_PJ)
    time.sleep(0.5)
    print("✅ Botão clicado (PF)!")

else:
    # ─── É PJ: aperta Ctrl+Y, seleciona arrastando e deleta ───
    print("   🏢 É PJ → Executando limpeza...")
    
    # Clica no botão primeiro
    clicar(BOTAO_CONDICIONAL_PF_PJ)
    time.sleep(0.5)
    
    # Ctrl+Y
    pyautogui.hotkey('ctrl', 'y')
    time.sleep(0.5)
    print("   ✅ Ctrl+Y pressionado!")
    
    # Seleciona arrastando de CAMPO_SELECAO_INICIO até CAMPO_SELECAO_FIM
    print("   🖱️ Selecionando área (arrastando)...")
    pyautogui.moveTo(x=CAMPO_SELECAO_INICIO[0], y=CAMPO_SELECAO_INICIO[1])
    time.sleep(0.3)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(
        x=CAMPO_SELECAO_FIM[0], 
        y=CAMPO_SELECAO_FIM[1], 
        duration=0.5
    )
    time.sleep(0.2)
    pyautogui.mouseUp()
    time.sleep(0.3)
    print("   ✅ Área selecionada!")
    
    # Aperta Delete
    pyautogui.press('delete')
    time.sleep(0.5)
    print("   ✅ Conteúdo deletado!")
    
    print("✅ Processo PJ concluído!")

# ============================================================
# PASSO 30: Clicar no botão após a condicional
# ============================================================
print("\nPASSO 30: Clicando no botão pós-condicional...")
focar_sap()
clicar(BOTAO_APOS_CONDICIONAL)
time.sleep(1)
print("✅ Botão clicado!")

# ============================================================
# PASSO 31: Sequência de botões (SAP atualiza entre cada um)
# ============================================================
print("\nPASSO 31: Executando sequência de atualização...")
focar_sap()

# Botão 1
print("   🔄 Clicando botão 1/4...")
clicar(BOTAO_ATUALIZAR_1)
time.sleep(3)  # SAP atualiza
print("   ✅ Botão 1 OK!")

# Botão 2
print("   🔄 Clicando botão 2/4...")
clicar(BOTAO_ATUALIZAR_2)
time.sleep(3)  # SAP atualiza
print("   ✅ Botão 2 OK!")

# Botão 3
print("   🔄 Clicando botão 3/4...")
clicar(BOTAO_ATUALIZAR_3)
time.sleep(3)  # SAP atualiza
print("   ✅ Botão 3 OK!")

# Botão 4
print("   🔄 Clicando botão 4/4...")
clicar(BOTAO_ATUALIZAR_4)
time.sleep(3)  # SAP atualiza
print("   ✅ Botão 4 OK!")

print("\n" + "=" * 50)
print("  🎉 PROCESSO COMPLETO!")
print("=" * 50)


print()
print("=" * 50)
print("  🎉 PROCESSO COMPLETO!")
print("=" * 50)