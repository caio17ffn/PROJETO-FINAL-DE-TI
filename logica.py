def bubble_sort_pacientes(lista, campo="nome"):
    """Ordena a lista de pacientes sem usar sort() pronto (UC30)."""
    pacientes = [dict(p) for p in lista]     # copia pra não mexer na original
    n = len(pacientes)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            a = str(pacientes[j][campo]).lower()
            b = str(pacientes[j + 1][campo]).lower()
            if a > b:
                pacientes[j], pacientes[j + 1] = pacientes[j + 1], pacientes[j]
                trocou = True
        if not trocou:                        # já ordenado, para antes
            break
    return pacientes


def busca_binaria_por_data(consultas, data_alvo):
    """Busca binária numa lista de consultas já ordenada por data (UC30)."""
    inicio, fim = 0, len(consultas) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        atual = consultas[meio]["data"]
        if atual == data_alvo:
            return consultas[meio]
        elif atual < data_alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None


def contar_por_paciente(consultas):
    """Retorna um dicionário {nome: quantidade} usando for + if."""
    contagem = {}
    for c in consultas:
        nome = c["paciente"]
        if nome in contagem:
            contagem[nome] += 1
        else:
            contagem[nome] = 1
    return contagem
