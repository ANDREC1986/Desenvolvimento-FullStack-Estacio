import csv_loader
from faker import Faker
import random

def turno():
    turnos = ['Manhã','Tarde','Noite']
    turno = random.choice(turnos)
    return turno

def contato():
    contato = ''
    tipo = random.randint(8,9)
    for i in range(tipo):
        contato += ''.join(str(random.randint(0,9)))
    return contato

def equipe():
    equipes = ['Equipe A', 'Equipe B', 'Equipe C', 'Equipe D', 'Gerencia A', 'Gerencia B','Gerencia C','Transporte A','Manutenção A']
    equipe = random.choice(equipes)
    return equipe

def cpf():                                                        
    cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                
    for _ in range(2):                                                          
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
        cpf.append(11 - val if val > 1 else 0)

    result = ''.join(str(cpf))
    result = result.replace(', ','')
    result = result.replace('[','')
    result = result.replace(']','')
    return result

def nomes():
    nome = Faker('pt_BR')
    result = nome.unique.name()
    return result

def valida_cpf(cpf):
    numbers = cpf
    numeros = numbers[:-2]
    valida1 = numbers[-2]
    valida2 = numbers[-1]
    numbers = 10
    resultado = 0
    for c in numeros:
        resultado = resultado + int(c)*numbers
        numbers -= 1
    resultado = resultado * 10
    resultado = resultado % 11
    if resultado == 10: resultado = 0
    if str(resultado) != str(valida1):
        return False
    numbers = cpf
    numeros = numbers[:-1]
    numbers = 11
    resultado = 0
    for c in numeros:
        resultado = resultado + int(c)*numbers
        numbers -= 1
    resultado = resultado * 10
    resultado = resultado % 11
    if resultado == 10: resultado = 0
    if str(resultado) != str(valida2):
        return False

def feed_funcionarios():
    funcionario = []
    i=0
    while i <= 100:
        CPF = cpf()
        funcionario.append([CPF,nomes(),equipe(),turno(),contato()])
        i += 1
    return funcionario
funcionarios = csv_loader.funcionarios

def funcionario():
    novos_funcionarios = feed_funcionarios()
    for item in novos_funcionarios:
        funcionarios.append(item)
    csv_loader.save_funcionarios()

ferramentas_nomes = ['Alicate universal para eletricista', 'Alicate de corte diagonal para eletricista', 'Chave de fenda isolada ', 'Chave de fenda isolada 6” x 1/8” (chave de bornes)', 'Chave Philips isolada 6','Chave Philips isolada 6” x 1/8” (chave debornes)','Alicate decapadorautomático', 'Alicate prensa terminais tubolares, com catraca, para terminais','Alicate prensa terminais laminados sem isolação, com catraca, para terminais','Alicate amperímetro','Martelo','Furadeira','Parafusadeira','Tubotoch']
medidas = ['pol','mm','cm']
tamanhos = [[1,15],[0.5,5],[0.5,5],[5,40]]
voltagem = ['NA','127v','220v','5v','12v']

def tempo():
    result = random.randint(0,24)
    return result

def medida():
    result = random.choice(medidas)
    return result

def tamanho():
    tama = tamanhos[random.randint(0,3)]
    result = random.randrange(int(tama[0]),int(tama[1]))
    return result

def partnum():
    id = ''
    for i in range(10):
        id += ''.join(str(random.randint(0,9)))
    return id

def id():
    id = ''
    for i in range(7):
        id += ''.join(str(random.randint(0,9)))
    return id
    
ferramentas = csv_loader.ferramentas

def fab():
    choices = ['Bocsh','Makita','Hemmer','Wonder','Tramontina']
    result = random.choice(choices)
    return result

def ferramenta_nome():
    result = random.choice(ferramentas_nomes)
    return result

def volt():
    result = random.choice(voltagem)
    return result

def tipo():
    choices = ['Manual','Eletrico','Mecanico']
    result = random.choice(choices)
    return result

def mat():
    choices = ['Metal','Aço','Plástico','Metal','Aço','Plástico','Chumbo']
    result = random.choice(choices)
    return result

def unid():
    match = False
    check = False
    while check == False:
        unid = id()
        for item in ferramentas:
            if item[0] == unid:
                match = True
        if match == False:
            check = True
    return unid

def ferramenta():
    ferramenta = []
    i = 0
    while i < 100:
        ferramentas.append([unid(),ferramenta_nome(),fab(),partnum(),tipo(),volt(),tamanho(),medida(),mat(),tempo()])
        i += 1

ferramenta()
csv_loader.save_ferramentas()
funcionario()