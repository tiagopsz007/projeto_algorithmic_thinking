
import csv
from datetime import datetime

Base_preco = {
    'apartamento': 700.0,
    'casa': 900.0,
    'estudio': 1200.0,
}

Valor_contrato = 2000.0


def reais(v):
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def calcular_mensalidade(tipo, quartos, vagas, tem_criancas=True):
    # preço base
    tipo_key = tipo.lower()
    mensal = Base_preco[tipo_key]

    # acréscimos por 2 quartos
    if quartos == 2:
        if tipo_key == 'apartamento':
            mensal += 200.0
        elif tipo_key == 'casa':
            mensal += 250.0
       

    # vagas
    if tipo_key in ('apartamento', 'casa'):
        mensal += 300.0 * vagas
    elif tipo_key == 'estudio':
        if vagas > 0:
            if vagas <= 2:
                mensal += 250.0
            else:
                mensal += 250.0 + (vagas - 2) * 60.0

    # desconto de 5% para apartamentos sem criancas
    if tipo_key == 'apartamento' and not tem_criancas:
        mensal *= 0.95

    return round(mensal, 2)


def gerar_planilha_csv(filename, mensal, parcelas_contrato, include_date=True):
    if parcelas_contrato < 1 or parcelas_contrato > 5:
        raise ValueError('Parcelas do contrato devem ser entre 1 e 5')

    contrato_parcela = round(Valor_contrato / parcelas_contrato, 2)

    rows = []
    for mes in range(1, 13):
        contrato_val = contrato_parcela if mes <= parcelas_contrato else 0.0
        total = round(mensal + contrato_val, 2)
        row = {
            'mes': mes,
            'mensalidade': f'{mensal:.2f}',
            'parcela_contrato': f'{contrato_val:.2f}',
            'total_mensal': f'{total:.2f}'
        }
        if include_date:
            row['gerado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        rows.append(row)

    fieldnames = list(rows[0].keys())
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    return filename


def main():
    print('=== ORCADOR R.M - Versao CLI ===')
    print('Selecione o tipo de imovel:')
    print('1 - Apartamento')
    print('2 - Casa')
    print('3 - Estudio')
    tipo_opt = input('Opcao (1/2/3): ').strip()
    tipo_map = {'1': 'apartamento', '2': 'casa', '3': 'estudio'}
    tipo = tipo_map.get(tipo_opt)
    if not tipo:
        print('Opcao invalida. Saindo.')
        return

    quartos = 1
    if tipo in ('apartamento', 'casa'):
        q = input('Numero de quartos (1 ou 2)? [1]: ').strip()
        if q == '2':
            quartos = 2
    else:
        quartos = 1

    vagas = 0
    v = input('Deseja vagas de garagem? Quantas? [0]: ').strip()
    if v:
        try:
            vagas = int(v)
            if vagas < 0:
                vagas = 0
        except:
            vagas = 0

    tem_criancas = True
    if tipo == 'apartamento':
        c = input('Ha criancas no domicilio? (s/n) [s]: ').strip().lower()
        if c == 'n':
            tem_criancas = False

    parcelas_contrato = 1
    p = input('Parcelas do contrato (1 a 5) [1]: ').strip()
    if p:
        try:
            parcelas_contrato = int(p)
            if parcelas_contrato < 1 or parcelas_contrato > 5:
                parcelas_contrato = 1
        except:
            parcelas_contrato = 1

    mensal = calcular_mensalidade(tipo, quartos, vagas, tem_criancas=tem_criancas)
    contrato_parcela = round(Valor_contrato / parcelas_contrato, 2)
    print('\n--- RESUMO ORCAMENTO ---')
    print(f'Tipo: {tipo.capitalize()}')
    print(f'Quartos: {quartos}')
    print(f'Vagas: {vagas}')
    print(f'Valor mensal (sem contrato): {reais(mensal)}')
    print(f'Contrato total: {reais(Valor_contrato)} em {parcelas_contrato}x de {reais(contrato_parcela)}')
    print(f'Valor mensal com parcela do contrato (nos primeiros {parcelas_contrato} meses): {reais(mensal + contrato_parcela)}')

    salvar = input('\nGerar arquivo CSV com 12 parcelas do orcamento? (s/n) [s]: ').strip().lower()
    if salvar != 'n':
        filename = f'orcamento_{tipo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        caminho = gerar_planilha_csv(filename, mensal, parcelas_contrato)
        print(f'Arquivo gerado: {caminho}')

    print('\nPronto!')


if __name__ == '__main__':
    main()
