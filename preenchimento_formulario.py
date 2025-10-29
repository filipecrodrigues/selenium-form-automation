from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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

for aluno in alunos:
    try:
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfh9ebeWaWA27bQYKLOt359E9zvgJzvljSD48Px_VV4qP97eQ/viewform?usp=sharing&ouid=103546220084617813983")
        time.sleep(2)

        campos = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")

        if len(campos) >= 2:
            campos[0].send_keys(aluno["Nome"])
            campos[1].send_keys(aluno["Cpf"])
        else:
            msg = f"Erro: campos não encontrados para {aluno['nome']} - {aluno['cpf']}"
            print(msg)
            logging.error(msg)
            continue

        # Clica no botão "Enviar"
        botao_enviar = driver.find_element(By.XPATH, '//span[text()="Enviar"]')
        botao_enviar.click()

        msg = f"Formulário enviado para: {aluno['nome']} - {aluno['cpf']}"
        print(msg)
        logging.info(msg)
        time.sleep(2)

        # Clica em "Enviar outra resposta"
        try:
            outro = driver.find_element(By.LINK_TEXT, "Enviar outra resposta")
            outro.click()
            time.sleep(2)
        except:
            msg = "Botão 'Enviar outra resposta' não encontrado. Encerrando."
            print(msg)
            logging.warning(msg)
            break

    except Exception as e:
        logging.exception(f"Erro ao processar aluno: {aluno['nome']} - {aluno['cpf']}")

driver.quit()
