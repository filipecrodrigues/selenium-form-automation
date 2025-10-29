from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from datetime import datetime

# Configuração do arquivo de log
logging.basicConfig(
    filename='log_envios.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Dados fictícios
alunos = [
    {"nome": "Ana Paula Souza", "cpf": "123.456.789-00"},
    {"nome": "Bruno Lima Costa", "cpf": "234.567.890-11"},
    {"nome": "Carla Mendes Silva", "cpf": "345.678.901-22"},
]

# Inicia o Chrome com o driver correto
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

for aluno in alunos:
    try:
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfh9ebeWaWA27bQYKLOt359E9zvgJzvljSD48Px_VV4qP97eQ/viewform?usp=sharing&ouid=103546220084617813983")
        
        # Aguarda os campos carregarem
        time.sleep(3)

        # Tenta encontrar os campos de input do formulário
        campos = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        
        if len(campos) >= 2:
            campos[0].clear()
            campos[0].send_keys(aluno["nome"])  # Corrigido: minúsculo
            
            campos[1].clear()
            campos[1].send_keys(aluno["cpf"])   # Corrigido: minúsculo
            
            msg = f"Dados preenchidos para: {aluno['nome']}"
            print(msg)
            logging.info(msg)
        else:
            msg = f"Erro: campos não encontrados para {aluno['nome']} - {aluno['cpf']}"
            print(msg)
            logging.error(msg)
            continue

        # Aguarda um pouco antes de enviar
        time.sleep(2)

        # Clica no botão "Enviar"
        botao_enviar = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Enviar"]'))
        )
        botao_enviar.click()

        msg = f"Formulário enviado para: {aluno['nome']} - {aluno['cpf']}"
        print(msg)
        logging.info(msg)
        time.sleep(3)

        # Clica em "Enviar outra resposta"
        try:
            outro = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Enviar outra resposta"))
            )
            outro.click()
            time.sleep(2)
        except:
            msg = "Botão 'Enviar outra resposta' não encontrado. Encerrando."
            print(msg)
            logging.warning(msg)
            break

    except Exception as e:
        msg = f"Erro ao processar aluno: {aluno['nome']} - {aluno['cpf']} - Erro: {str(e)}"
        print(msg)
        logging.exception(msg)

driver.quit()