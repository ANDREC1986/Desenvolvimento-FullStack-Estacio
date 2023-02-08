import csv
def csv_load(file,header):
    try:
        with open(file, mode='r', encoding='UTF8') as f:
            data = csv.reader(f)
            f.close()
    except:
        with open(file, mode='w', encoding='UTF8') as f:
            writer=csv.writer(f)
            writer.writerow(header)
            f.close()
    finally:
        with open(file, mode='r', encoding='UTF8') as f:
            data = csv.reader(f)
            result = list(data)
            result =  list(filter(None, result))
            f.close()
            return result

def csv_save(file,values):
    with open(file, mode='w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerows(values)
        f.close

def load_ferramentas():
    file = 'ferramentas.csv'
    headers = ['ID','Nome - Descrição', 'Fabricante','Part Num','Tipo','Voltagem ','Tamanho','U.Medida','Material','Tempo Limite']
    ferramentas = csv_load(file,headers)
    return ferramentas

def load_reservas():
    file = 'reservas.csv'
    headers = ['funcionario','decrição','retirada','devolução','ferramentas']
    reservas = csv_load(file,headers)
    for item in reservas[1:]:
        item[4] = item[4].replace('"', '')
        item[4] = item[4].replace("'", '')
        item[4] = item[4].replace('[', '')
        item[4] = item[4].replace(']', '')
        item[4] = item[4].replace(' ', '')
        item[4] = item[4].split(',')
    return reservas

def save_reservas():
    file ='reservas.csv'
    values = reservas
    csv_save(file,values)

def load_funcionarios():
    file = 'funcionarios.csv'
    headers = ['cpf','nome','equipe','turno','contato']
    funcionarios = csv_load(file,headers)
    return funcionarios

def save_funcionarios():
    file ='funcionarios.csv'
    values = funcionarios
    csv_save(file,values)

def save_ferramentas():
    file = 'ferramentas.csv'
    values = ferramentas
    csv_save(file,values)

ferramentas = load_ferramentas()
funcionarios = load_funcionarios()
reservas = load_reservas()