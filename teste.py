from email.policy import default
from tkinter.filedialog import askopenfilenames
from tkinter.ttk import *
from tkinter import *
from tkcalendar import DateEntry 

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
    print(input_data.get_date().strftime("%d/%m/%Y"))
    print(input_quantidade.get())
    print(input_titulo.get())
    print(input_valorUN.get())
    print(combo_categoria.get())
    print(combo_centroCusto.get())
    print(combo_filial.get())
    print(combo_item.get())
    print(combo_tipo.get())
    print(varcheckNavegador.get())
    print(varmonitorReq.get())

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
    checkNavegador.deselect()
    habilitaProcurar()

def procurarArquivos():
    filenames = askopenfilenames(
        title='Procurar arquivos',
    )
    input_arquivo.insert(INSERT, filenames)

def habilitaProcurar(*args):
    print(combo_categoria.get())
    if combo_categoria.get() == "PEDIDO REGULARIZACAO":
        arquivo_requisicao.place(relx=.33, rely=.5)
        input_arquivo.place(relx=.02, rely=.54)
        botaoProcuraArquivo.place(relx=.72, rely=.53)
        comentario_requisicao.place(relx=.41, rely=.6)
        input_comentario.place(relx=.15, rely=.64)
        botaoCriar.place(relx=.02, rely=.69)
        botaoCancelar.place(relx=.42, rely=.69)
        botaoLimpar.place(relx=.83, rely=.69)
        print(combo_categoria.get())
    else:
        arquivo_requisicao.place_forget()
        input_arquivo.place_forget()
        botaoProcuraArquivo.place_forget()
        comentario_requisicao.place(relx=.41, rely=.5)
        input_comentario.place(relx=.15, rely=.54)
        botaoCriar.place(relx=.02, rely=.60)
        botaoCancelar.place(relx=.42, rely=.60)
        botaoLimpar.place(relx=.83, rely=.60)

codLista = []

def atualizaCodigo(event):
    codLista.append(dicioTipo[combo_tipo.get()])
    combo_item.set(';'.join(codLista).strip())

varcheckNavegador = BooleanVar()
varmonitorReq = BooleanVar()

checkNavegador = Checkbutton(janela, text='Abre Nav',variable=varcheckNavegador, offvalue=False, onvalue=True)
checkNavegador.place(relx=.02, rely=.02)

monitorReq = Checkbutton(janela, text='Monitor',variable=varmonitorReq, onvalue=True, offvalue=False)
monitorReq.place(relx=.78, rely=.02)
monitorReq.select()

titulo_requisicao = Label(janela, text='Titulo da requisição', font='calibri, 10')
titulo_requisicao.place(relx=.35, rely=.02)
input_titulo = Entry(janela, text='Titulo',width=55)
input_titulo.place(relx=.02, rely=.06)

tipo_requisicao = Label(janela, text='Tipo de requisição', font='calibri, 10')
tipo_requisicao.place(relx=.35, rely=.09)
combo_tipo = Combobox(janela, width=52, state="readonly")
combo_tipo['values']=(listaTipo)
combo_tipo.place(relx=.02, rely=.13)
combo_tipo.bind("<<ComboboxSelected>>", atualizaCodigo)

item_requisicao = Label(janela, text='Item', font='calibri, 10')
item_requisicao.place(relx=.02, rely=.17)
combo_item = Combobox(janela, width=20)
combo_item['values']=(codigos)
combo_item.place(relx=.02, rely=.21)

valorUN_requisicao = Label(janela, text='Valor unitário', font='calibri, 10')
valorUN_requisicao.place(relx=.57, rely=.17)
input_valorUN = Entry(janela, text='valorunitario')
input_valorUN.place(relx=.57, rely=.21)

quantidade_requisicao = Label(janela, text='Quantidade', font='calibri, 10')
quantidade_requisicao.place(relx=.02, rely=.25)
input_quantidade = Entry(janela, text='quantidade', width=23)
input_quantidade.place(relx=.02, rely=.29)

data_requisicao = Label(janela, text='Data esperada', font='calibri, 10')
data_requisicao.place(relx=.57, rely=.25)
input_data = DateEntry(janela, width=20)
input_data.delete(0,"end")
input_data.place(relx=.57, rely=.29)


categoria_requisicao = Label(janela, text='Selecione a categoria', font='calibri, 10')
categoria_requisicao.place(relx=.02, rely=.33)
combo_categoria = Combobox(janela, width=25, state="readonly")
combo_categoria['values']=(categorias)
combo_categoria.place(relx=.02, rely=.37)
combo_categoria.bind("<<ComboboxSelected>>", habilitaProcurar)

centroCusto_requisicao = Label(janela, text='Centro de custo', font='calibri, 10')
centroCusto_requisicao.place(relx=.57, rely=.33)
combo_centroCusto = Combobox(janela, width=20, state="readonly")
combo_centroCusto['values']=(centroCustos)
combo_centroCusto.place(relx=.57, rely=.37)

filial_requisicao = Label(janela, text='Selecione a filial:', font='calibri, 10')
filial_requisicao.place(relx=.34, rely=.41)
combo_filial = Combobox(janela, width=52, state="readonly")
combo_filial['values']=(filiais)
combo_filial.place(relx=.02, rely=.45)

arquivo_requisicao = Label(janela, text='Selecionar arquivos:', font='calibri, 10')
input_arquivo = Text(janela, width=28, height=1)
botaoProcuraArquivo = Button(janela, text='Procurar', command=procurarArquivos, width=10, font='calibri, 10')

comentario_requisicao = Label(janela, text='Comentario:', font='calibri, 10')
comentario_requisicao.place(relx=.41, rely=.5)
input_comentario = Entry(janela, text='comentario', width=40)
input_comentario.place(relx=.15, rely=.54)


botaoCriar = Button(janela, text='Criar', command=obterInfos, width=15, font='calibri, 10')
botaoCriar.place(relx=.02, rely=.60)
botaoCancelar = Button(janela, text='Cancelar',  width=15, font='calibri, 10', command=janela.destroy)
botaoCancelar.place(relx=.42, rely=.60)
botaoLimpar = Button(janela, text='Limpar', width=5, font='calibri, 10', command=limpar)
botaoLimpar.place(relx=.83, rely=.60)
# botaoCriar = Button(janela, text='Criar', command=obterInfos, width=15, font='calibri, 10').place(relx=.02, rely=.69)
# botaoCancelar = Button(janela, text='Cancelar',  width=15, font='calibri, 10', command=janela.destroy).place(relx=.42, rely=.69)
# botaoLimpar = Button(janela, text='Limpar', width=5, font='calibri, 10', command=limpar).place(relx=.83, rely=.69)

janela.mainloop()