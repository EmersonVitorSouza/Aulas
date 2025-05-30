from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Iniciar o navegador
driver = webdriver.Chrome()

# Abrir o site
driver.get("https://www.mg.senac.br/Paginas/default.aspx")  # Troque pelo endereço do seu site

# Esperar o botão ficar visível (até 10 segundos)
wait = WebDriverWait(driver, 10)  # Espera de no máximo 10 segundos
botao_T= wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transparência")))

# Clicar no botão
botao_T.click()

wait = WebDriverWait(driver, 10)  # Espera de no máximo 10 segundos
botao_T2 = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Programa")))

# Mover o mouse para o botão
actions = ActionChains(driver)  
actions.move_to_element(botao_T2).perform()   

botao_T2.click()

# Espera um pouco para evitar race condition
import time
time.sleep(5)

