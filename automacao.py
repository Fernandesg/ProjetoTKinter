from tkinter.ttk import *
from tkinter import *

passwords = open('credenciais.txt', 'r')
login = []

for linhas in passwords:
    linhas = linhas.strip()
    login.append(linhas)
usuario_me = login[0][14:-1]
senha_me = login[1][12:-1]
site = login[2][8:-1]

filiais_caminho = open('filiais.txt', 'r', encoding="UTF-8")
filiais = []

for linhas in filiais_caminho:
    linhas = linhas.strip()
    filiais.append(linhas)

listaTipo = []
dicioTipo = {}
with open("TipoRequisicao.txt", encoding="UTF-8") as dicionarioTipoReq:
    for line in dicionarioTipoReq:
       (k, v) = line.split()
       dicioTipo[str(k)] = v
    for chave in dicioTipo.keys():
        listaTipo.append(chave)

cod_caminho = open('codigos.txt', 'r', encoding="UTF-8")
codigos = []

for linhas in cod_caminho:
    linhas = linhas.strip()
    codigos.append(linhas)

cc_caminho = open('centrocustos.txt', 'r', encoding="UTF-8")
centroCustos = []

for linhas in cc_caminho:
    linhas = linhas.strip()
    centroCustos.append(linhas)

categorias_caminho = open('categorias.txt', 'r', encoding="UTF-8")
categorias = []

for linhas in categorias_caminho:
    linhas = linhas.strip()
    categorias.append(linhas)

janela = Tk()

janela.title('Automação requisição')
janela.geometry('450x600+500+100')

def obterInfos():
    print(input_comentario.get())
    print(input_data.get())
    print(input_quantidade.get())
    print(input_titulo.get())
    print(input_valorUN.get())
    print(combo_categoria.get())
    print(combo_centroCusto.get())
    print(combo_filial.get())
    print(combo_item.get())
    print(combo_tipo.get())

titulo_requisicao = Label(janela, text='Titulo da requisição')
titulo_requisicao.grid(column=0, row=0, pady=10)
input_titulo = Entry(janela, text='Titulo', width=40)
input_titulo.grid(column=0, row=1)

tipo_requisicao = Label(janela, text='Tipo de requisição')
tipo_requisicao.grid(column=0, row=2, pady=10)
combo_tipo = Combobox(janela, width=40)
combo_tipo['values']=(listaTipo)
combo_tipo.grid(column=0, row=3)

item_requisicao = Label(janela, text='Item')
item_requisicao.grid(column=0, row=4,  pady=10)
combo_item = Combobox(janela, width=20)
combo_item['values']=(codigos)
combo_item.grid(column=0, row=5)

valorUN_requisicao = Label(janela, text='Valor unitário')
valorUN_requisicao.grid(column=1, row=4, pady=10)
input_valorUN = Entry(janela, text='valorunitario')
input_valorUN.grid(column=1, row=5)

quantidade_requisicao = Label(janela, text='Quantidade')
quantidade_requisicao.grid(column=0, row=6, pady=10)
input_quantidade = Entry(janela, text='quantidade', width=20)
input_quantidade.grid(column=0, row=7)

data_requisicao = Label(janela, text='Data esperada')
data_requisicao.grid(column=1, row=6, pady=10)
input_data = Entry(janela, text='dataesperada', width=20)
input_data.grid(column=1, row=7)

categoria_requisicao = Label(janela, text='Selecione a categoria')
categoria_requisicao.grid(column=0, row=8, pady=10)
combo_categoria = Combobox(janela, width=25)
combo_categoria['values']=(categorias)
combo_categoria.grid(column=0, row=9)

centroCusto_requisicao = Label(janela, text='Centro de custo')
centroCusto_requisicao.grid(column=1, row=8, pady=10)
combo_centroCusto = Combobox(janela, width=20)
combo_centroCusto['values']=(centroCustos)
combo_centroCusto.grid(column=1, row=9)

filial_requisicao = Label(janela, text='Selecione a filial')
filial_requisicao.grid(column=0, row=10, pady=10)
combo_filial = Combobox(janela, width=40)
combo_filial['values']=(filiais)
combo_filial.grid(column=0, row=11)

comentario_requisicao = Label(janela, text='Comentario:')
comentario_requisicao.grid(column=0, row=12, pady=10)
input_comentario = Entry(janela, text='comentario', width=40)
input_comentario.grid(column=0, row=13)

botaoCriar = Button(janela, text='Criar', command=obterInfos, width=20)
botaoCriar.grid(column=0, row=14)

janela.mainloop()