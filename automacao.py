from faulthandler import disable
from fileinput import filename
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import *
from tkinter import *

from requests import delete

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
       (k, v) = line.split(';')
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



janela.title('Abertura de requisições')
janela.geometry('350x600')

def obterInfos(*args):
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

def limpar():
    input_comentario.delete(0,"end")
    input_data.delete(0,"end")
    input_quantidade.delete(0,"end")
    input_titulo.delete(0,"end")
    input_valorUN.delete(0,"end")
    input_arquivo.delete("1.0","end")
    combo_categoria.set("")
    combo_centroCusto.set("")
    combo_filial.set("")
    combo_item.set("")
    combo_tipo.set("")

def procurarArquivos():
    filenames = askopenfilenames(
        title='Procurar arquivos',
    )
    input_arquivo.insert(INSERT, filenames)

def habilitaProcurar(*args):

    if combo_categoria.get() == "PEDIDO REGULARIZACAO":
        arquivo_requisicao.grid(column=0, row=12, pady=5, columnspan=2)
        input_arquivo.grid(column=0, row=13, columnspan=2, padx=5, sticky=W)
        botaoProcuraArquivo.grid(column=1, row=13, pady=10, sticky=E)
    else:
        arquivo_requisicao.grid_remove()
        input_arquivo.grid_remove()
        botaoProcuraArquivo.grid_remove()

codLista = []

def atualizaCodigo(event):
    codLista.append(dicioTipo[combo_tipo.get()])
    combo_item.set(';'.join(codLista).strip())

varcheckNavegador = BooleanVar()
varmonitorReq = BooleanVar()

checkNavegador = Checkbutton(janela, text='Abre Nav',variable=varcheckNavegador, offvalue=False, onvalue=True).grid(column=0, row=0, sticky=E)
monitorReq = Checkbutton(janela, text='Monitor',variable=varmonitorReq, onvalue=True, offvalue=False).grid(column=2, row=0,sticky=E)

titulo_requisicao = Label(janela, text='Titulo da requisição', font='calibri, 10')
titulo_requisicao.grid(column=1, row=0, pady=5, sticky=NW)
input_titulo = Entry(janela, text='Titulo', width=50)
input_titulo.grid(column=0, row=1, pady=5, columnspan=2)

tipo_requisicao = Label(janela, text='Tipo de requisição', font='calibri, 10')
tipo_requisicao.grid(column=0, row=2, pady=5, columnspan=2)
combo_tipo = Combobox(janela, width=47, state="readonly")
combo_tipo['values']=(listaTipo)
combo_tipo.grid(column=0, row=3, columnspan=2)
combo_tipo.bind("<<ComboboxSelected>>", atualizaCodigo)

item_requisicao = Label(janela, text='Item', font='calibri, 10')
item_requisicao.grid(column=0, row=4,  pady=5)
combo_item = Combobox(janela, width=20)
combo_item['values']=(codigos)
combo_item.grid(column=0, row=5)

valorUN_requisicao = Label(janela, text='Valor unitário', font='calibri, 10')
valorUN_requisicao.grid(column=1, row=4, pady=5)
input_valorUN = Entry(janela, text='valorunitario')
input_valorUN.grid(column=1, row=5)

quantidade_requisicao = Label(janela, text='Quantidade', font='calibri, 10')
quantidade_requisicao.grid(column=0, row=6, pady=5)
input_quantidade = Entry(janela, text='quantidade', width=23)
input_quantidade.grid(column=0, row=7)

data_requisicao = Label(janela, text='Data esperada', font='calibri, 10')
data_requisicao.grid(column=1, row=6, pady=5)
input_data = Entry(janela, text='dataesperada', width=20)
input_data.grid(column=1, row=7)


categoria_requisicao = Label(janela, text='Selecione a categoria', font='calibri, 10')
categoria_requisicao.grid(column=0, row=8, pady=5, padx=10)
combo_categoria = Combobox(janela, width=25, state="readonly")
combo_categoria['values']=(categorias)
combo_categoria.grid(column=0, row=9, padx=10)
combo_categoria.bind("<<ComboboxSelected>>", habilitaProcurar)

centroCusto_requisicao = Label(janela, text='Centro de custo', font='calibri, 10')
centroCusto_requisicao.grid(column=1, row=8, pady=5)
combo_centroCusto = Combobox(janela, width=20, state="readonly")
combo_centroCusto['values']=(centroCustos)
combo_centroCusto.grid(column=1, row=9)

filial_requisicao = Label(janela, text='Selecione a filial', font='calibri, 10')
filial_requisicao.grid(column=0, row=10, pady=5, columnspan=2)
combo_filial = Combobox(janela, width=50, state="readonly")
combo_filial['values']=(filiais)
combo_filial.grid(column=0, row=11, columnspan=2)

arquivo_requisicao = Label(janela, text='Selecionar arquivos:', font='calibri, 10')
input_arquivo = Text(janela, width=28, height=1)
botaoProcuraArquivo = Button(janela, text='Procurar', command=procurarArquivos, width=10, font='calibri, 10')

comentario_requisicao = Label(janela, text='Comentario:', font='calibri, 10')
comentario_requisicao.grid(column=0, row=14, pady=5, columnspan=2)
input_comentario = Entry(janela, text='comentario', width=40)
input_comentario.grid(column=0, row=15, columnspan=2)

botaoCriar = Button(janela, text='Criar', command=obterInfos, width=10, font='calibri, 10').grid(column=0, row=16, pady=10, padx=10, sticky=N)

botaoCancelar = Button(janela, text='Cancelar',  width=10, font='calibri, 10', command=janela.destroy).grid(column=1, row=16, pady=10, sticky=S)

botaoLimpar = Button(janela, text='Limpar', width=20, font='calibri, 10', command=limpar).grid(column=0, row=17, pady=10, columnspan= 2)

janela.mainloop()