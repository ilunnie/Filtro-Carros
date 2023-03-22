"""
Created on 20/03/2023

@Author: Luis Gustavo Caris dos Santos
"""

# -*- coding: utf-8 -*-
#======================
#     BIBLIOTECAS
#======================
import pandas
import random
import re
#======================

def recebe_int(texto, erro = "Valor inválido\n"):
    while True:
        try:
            return int(input(texto))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print(erro)

def recebe_confirmacao(texto, erro="Resposta inválida!\n"):
    while True:
        val = input(texto)
        if val[0].upper() == 'S' or val[0].upper() == 'Y': return 'SIM'
        if val[0].upper() == 'N': return 'NÃO'
        print(erro)

def recebe_placa(texto, erro = "Placa inválida ou já registrada\n", regex = r"[a-zA-Z]{3}\d{4}"):
    while True:
        placa = input(texto).upper()
        if placa not in placas_registradas:
            if re.match(regex, placa):
                placas_registradas.append(placa)
                return placa
        print(erro)
        
def recebe_chassi(texto, erro = "Chassi inválido ou já registrada\n"):
    while True:
        chassi = input(texto).upper()
        if chassi not in chassis_regristrados:
            if len(chassi) == 4:
                try:
                    int(chassi)
                    chassis_regristrados.append(chassi)
                    return chassi
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    None
        print(erro)
    
def recebe_combustivel(texto, erro = 'Combustível inválido\n', tipos = ['G', 'D', 'A']):
    while True:
        comb = input(texto)
        if comb[0].upper() in tipos: return comb[0].upper()
        print(erro)
    
def recebe_ano(texto, anomax = 2023, anomin = 1886, erro = 'Ano fora do limite!\n'):
    while True:
        ano = recebe_int(texto)
        
        if ano >= anomin and ano <= anomax:
            return ano
        else:
            print(erro)
    
def gerar_placa(regex = r"[a-zA-Z]{3}\d{4}"):
    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    while True:
        placa_auto = ''
        for i in range(7):
            placa_auto += random.choice(chars)
        if placa_auto not in placas_registradas:
            if re.match(regex, placa_auto):
                placas_registradas.append(placa_auto)
                return placa_auto

def gerar_chassi():
    chars = list("0123456789")
    while True:
        chassi_auto = ''
        for i in range(4):
            chassi_auto += random.choice(chars)
        if chassi_auto not in chassis_regristrados:
            chassis_regristrados.append(chassi_auto)
            return chassi_auto

def regCarro(quant = 0, forma = "AUTO"):
    if forma == "MANUAL":
        try:
            while True:
                carro = {}
                print("Crtl+C para finalizar")
                carro["PROPRIETARIO"] = input("   Proprietário: ").upper()
                carro["MODELO"] = input("   Modelo: ").upper()
                carro["ANO"] = recebe_ano("   Ano: ")
                carro["PLACA"] = recebe_placa("   Placa: ", erro="Placa inválida\n")
                carro["COR"] = input("   Cor: ").upper()
                carro["NUM CHASSI"] = recebe_chassi("   Número do Chassi: ")
                carro["COMBUSTIVEL"] = recebe_combustivel("   Combustível: ")
                global carros
                carros.append(carro)
        except KeyboardInterrupt:
            print("\n\n\nFinalizando o registro...")
    elif forma == "AUTO":
        nomes = pandas.read_csv("nomes.csv", sep=',')
        nomes_carros = pandas.read_csv("marcas-carros.csv", sep=';')
        cores_lista = ["AZUL", "VERDE", "AMARELO", "ROXO", "ROSA", "VERMELHO", "LARANJA", "MARROM", "CINZA", "BRANCO", "PRETO"]
        tipos_combustiveis = ['G', 'D', 'A']
        
        for i in range(quant):
            carro = {}
            carro["PROPRIETARIO"] = nomes["group_name"].sample().iloc[0]
            carro["MODELO"] = nomes_carros["NOME"].sample().iloc[0]
            carro["ANO"] = random.randint(1886, 2023)
            carro["PLACA"] = gerar_placa()
            carro["COR"] = random.choice(cores_lista)
            carro["NUM CHASSI"] = gerar_chassi()
            carro["COMBUSTIVEL"] = random.choice(tipos_combustiveis)
            carros.append(carro)
            
def troca_de_carro(nome):
    chassi = input("Número do chassi: ")
    carro_novo = df[df["NUM CHASSI"] == chassi]
    if len(carro_novo) == 1:
        i = df.index.get_loc(carro_novo.index[0])
        carros[i]["PROPRIETARIO"] = nome
        return ("Proprietário alterado com sucesso!")
    else:
        return ("Carro não encontrado...")
    
def recebe_carro_chassi(chassi):
    filtrado = df[df["NUM CHASSI"] == chassi]
    if len(filtrado) == 1:
        return filtrado
    else:
        return ("Carro não encontrado")
        

carros, resp = [], ''
placas_registradas, chassis_regristrados = [], []

while True:
    try:
        resp = recebe_confirmacao("Deseja definir os carros manualmente?\n> ")
        if (resp == 'SIM'): regCarro(forma = "MANUAL")
        if (resp == 'NÃO'):
            quantidade = recebe_int("Quantos carros deseja gerar?\n> ")
            regCarro(quant = quantidade, forma = "AUTO")
        
        resp = ''
        while resp == '':
            df = pandas.DataFrame(carros)
            
            letra_a = df[(df["ANO"] >= 1980) & (df["COMBUSTIVEL"] == "D")]
            letra_b = df[(df["PLACA"].str[0] == "A") & (df["PLACA"].str[-1].isin(["0", "2", "4", "7"]))]
            letra_c = df[(df["PLACA"].str[1].isin(["A", "E", "I", "O", "U"])) & ((df["PLACA"].str[-4:].astype(int).sum() % 2) == 0)]
            
            try:
                resp = input("\nO que deseja fazer?\n 1 - Ver resultado dos exercícios\n 2 - Trocar proprietário de um carro\n 3 - Mostrar todos os carros\n 4 - Mostrar informações sobre chassi\n> ")
                if resp == "1":
                    print('\n\n')
                    print(f'\na)\n {letra_a[["PROPRIETARIO", "MODELO", "ANO", "COMBUSTIVEL", "NUM CHASSI"]]}')
                    print(f'\nb)\n {letra_b[["PROPRIETARIO", "PLACA"]]}')
                    print(f'\nc)\n {letra_c[["PLACA", "MODELO", "COR"]]}')
                elif resp == "2":
                    print(troca_de_carro(input("\nNome do novo proprietário: ").upper()))
                elif resp == "3":
                    print(df[["PROPRIETARIO", "PLACA", "MODELO", "ANO", "NUM CHASSI"]])
                elif resp == "4":
                    print(recebe_carro_chassi(input('Número do chassi:\n> ')))
                else:
                    print("Valor inválido!")
                resp = ''
            except KeyboardInterrupt:
                        raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\n\n\nFinalizando o programa...")
        break