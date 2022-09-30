from tkinter.filedialog import askopenfilenames
from tkinter.ttk import *
from tkinter import *
from mttkinter import mtTkinter
from tkinter import messagebox
from tkcalendar import DateEntry 
from time import sleep
from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime
import smtplib
from openpyxl import Workbook, load_workbook
from datetime import date
import webbrowser
from win10toast_click import ToastNotifier 
from threading import *


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
        if line != '':
            (k, v) = line.split(';')
            dicioTipo[str(k)] = v
    for chave in dicioTipo.keys():
        if chave != '':
            listaTipo.append(chave)

cod_caminho = open('codigos.txt', 'r', encoding="UTF-8")
codigos = []

for linhas in cod_caminho:
    linhas = linhas.strip()
    if linhas != '':
        codigos.append(linhas)

cc_caminho = open('centrocustos.txt', 'r', encoding="UTF-8")
centroCustos = []

for linhas in cc_caminho:
    linhas = linhas.strip()
    if linhas != '':
        centroCustos.append(linhas)

categorias_caminho = open('categorias.txt', 'r', encoding="UTF-8")
categorias = []

for linhas in categorias_caminho:
    linhas = linhas.strip()
    if linhas != '':
        categorias.append(linhas)

janela = Tk()
janela.title('Abertura de requisições')
janela.geometry('350x600')

menubar = Menu(janela)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Arquivos", menu=filemenu)
filemenu.add_command(label='Itens', command=lambda: abreArquivo('codigos.txt'))
filemenu.add_command(label='Categorias', command=lambda: abreArquivo('categorias.txt'))
filemenu.add_command(label='Centro de custos', command=lambda: abreArquivo('centrocustos.txt'))
filemenu.add_command(label='Tipo requisição', command=lambda: abreArquivo('TipoRequisicao.txt'))
filemenu.add_command(label='Filiais', command=lambda: abreArquivo('filiais.txt'))
filemenu.add_separator()
filemenu.add_command(label='Credenciais ME', command=lambda: abreArquivo('credenciais.txt'))

toaster = ToastNotifier()
codLista = []
tabela = load_workbook('notas.xlsm', data_only=True)
aba_ativa = tabela['REQUISIÇÕES PENDENTES']
ultimaLinha = 'B' + str(len(aba_ativa['B'])+1)
filenames = ''

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
    
def printTeste(): 
    while True:
        if varmonitorReq.get() is True:    
            sleep(1)
            print('monitorando: ', varmonitorReq.get())  
        else:
            break

def monitorME():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=False)
            page = browser.new_page()
            page.goto(site)

            # LOGIN ME
            page.locator('xpath=//*[@id="LoginName"]').fill(usuario_me)
            page.locator('xpath=//*[@id="RAWSenha"]').fill(senha_me)
            page.locator('xpath=//*[@id="SubmitAuth"]').click()
            page.wait_for_timeout(1)

            # ANALISA STATUS DA REQUISIÇÃO E ATUALIZA PLANILHA
            for celula in aba_ativa['I']:
                linha = celula.row
                if celula.value == 'Pendente' and aba_ativa[f'E{linha}'].value == None:
                    cnpj = aba_ativa[f'D{linha}'].value
                    reqPendente = aba_ativa[f'B{linha}'].value
                    page.goto(f'https://www.me.com.br/DO/Request/Home.mvc/Show/{reqPendente}')
                    statusRequisicao = page.locator('//*[@id="formRequest"]/div/div[2]/div[2]/p[2]/span[2]').inner_html().strip()
                    filial_requisicao = page.locator('//*[@id="formRequest"]/section[1]/div[1]/div[2]').inner_html().strip()

                    if statusRequisicao == 'APROVADO':
                    #CRIAR PRE-PEDIDO
                        toaster.show_toast(f'Requisição aprovada!',f'Requisição {reqPendente} aprovada! \n Criando pré-pedido',icon_path=None, duration=10, threaded=True)
                        page.locator('xpath=//*[@id="btnEmergency"]').click()
                        page.locator('xpath=/html/body/div[1]/div[3]/div/button[1]/span').click()
                        page.locator('xpath=//*[@id="MEComponentManager_MEButton_2"]').click()
                        page.locator('xpath=//*[@id="CGC"]').fill(cnpj)
                        page.keyboard.press('Enter')
                        page.locator('xpath=//*[@id="grid"]/div[2]/table/tbody/tr/td[1]/div/input').click()
                        page.locator('xpath=//*[@id="btnSalvarSelecao"]').click()
                        page.locator('xpath=//*[@id="btnVoltarPrePedEmergencial"]').click()
                        page.locator('xpath=//*[@id="Resumo"]').fill(input_data.get_date().strftime("%d/%m/%Y"))
                        filiaisPrePedido = page.locator('//select[@name="LocalCobranca"]').inner_html().split('\n')
                        indice = [i for i, s in enumerate(filiaisPrePedido) if filial_requisicao in s][0]
                        page.locator('//select[@name="LocalCobranca"]').select_option(index=indice-1)
                        page.locator('xpath=//*[@id="DataEntrega"]').fill(input_titulo.get())
                        page.locator('xpath=//*[@id="MEComponentManager_MEButton_3"]').click()
                        page.locator('xpath=/html/body/main/form[2]/table[3]/tbody/tr[1]/td/input[1]').click()
                        page.locator('xpath=//*[@id="MEComponentManager_MEButton_2"]').click()
                        page.locator('xpath=//*[@id="MEComponentManager_MEButton_2"]').click()
                        page.locator('xpath=//*[@id="formItemStatusHistory"]/div/b[1]/a').click()
                        numPrePedido = page.locator('xpath=/html/body/main/div/div[1]/div[1]/p').inner_html().strip()
                        statusPrePedido = page.locator('xpath=/html/body/main/div/div[1]/div[2]/div[2]/p[1]/span[2]').inner_html().strip()
                        aba_ativa[f'F{linha}'] = date.today().strftime('%d/%m/%Y')
                        aba_ativa[f'E{linha}'] = numPrePedido
                    
                if celula.value == 'Pendente' and aba_ativa[f'E{linha}'].value != None:
                    
                    prePedidoPendente = aba_ativa[f'E{linha}'].value
                    page.goto(f'https://www.me.com.br/VerPrePedidoWF.asp?Pedido={prePedidoPendente}&SuperCleanPage=false&Origin=home')
                    statusPrePedido = page.locator('xpath=/html/body/main/div/div[1]/div[2]/div[2]/p[1]/span[2]').inner_html().strip()[:8]
                    if statusPrePedido == 'APROVADO':
                        numPedidoSAP = page.locator('xpath=/html/body/main/div/div[1]/div[1]/p[1]').inner_html().strip()
                        aba_ativa[f'G{linha}'] = numPedidoSAP
                        toaster.show_toast(f'Pré-Pedido {prePedidoPendente} aprovado!',f'O número do seu pedido é {numPedidoSAP} \nclique para abrir no navegador!',icon_path=None, duration=10, threaded=True,
                        callback_on_click=lambda: webbrowser.open(f'https://www.me.com.br/VerPrePedidoWF.asp?Pedido={prePedidoPendente}&SuperCleanPage=false&Origin=home'))
        tabela.save('Tabelateste.xlsx')

    except TimeoutError:
        toaster.show_toast(f'Erro no monitoramento de requisição.',f'Não foi possivel monitorar as requisições. \n Lentidão no mercado eletronico, tentando novamente em alguns minutos!',icon_path=None, duration=20, threaded=True)    
        
        tabela.save('Tabelateste.xlsx')

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
    progress_bar.place_forget()
    caixa_numero_req.place_forget()
    caixa_numero_req.delete("1.0", 'end')
    mensagem_titulo['text'] = ('')
    mensagem_numero_req['text'] = ('')
    titulo_progress_bar['text'] = ('')
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

def atualizaCodigo(*args):
    codLista.append(dicioTipo[combo_tipo.get()])
    combo_item.set(';'.join(codLista).strip())

def criarRequisicao(*args):
    comentario = input_comentario.get()
    caminho_arquivo = str(filenames).split(';')
    centro_custo = combo_centroCusto.get()
    cat_Pedido = combo_categoria.get()
    titulo_requisicao = input_titulo.get()
    item = str(combo_item.get()).strip().split(";")
    valorun = str(input_valorUN.get()).strip().split(";")
    quant = str(input_quantidade.get()).split(";")
    data_esperada = input_data.get_date().strftime("%d/%m/%Y")
    filial = combo_filial.get()
    nome_filial = filial.split('-',1)[1][1:]
    
    progress_bar.place_forget()
    caixa_numero_req.place_forget()
    caixa_numero_req.delete("1.0", 'end')
    mensagem_titulo['text'] = ('')
    mensagem_numero_req['text'] = ('')
    titulo_progress_bar['text'] = ('')

    
    try:
        with sync_playwright() as p:

            progress_bar.place(relx= .10, rely=.72)
            # valorTotal = str(float(valorun) * int(quant))
            if varcheckNavegador.get():
                browser = p.chromium.launch(channel="chrome",headless=False)
            else:
                browser = p.chromium.launch(channel="chrome")
            page = browser.new_page()
            page.goto(site)

            # LOGIN ME
            titulo_progress_bar['text'] = ('Efetuando login no ME')      
            progress_bar['value'] += 40
            page.locator('xpath=//*[@id="LoginName"]').fill(usuario_me)
            page.locator('xpath=//*[@id="RAWSenha"]').fill(senha_me)
            page.locator('xpath=//*[@id="SubmitAuth"]').click()

            # CONFIGURAÇÃO DA REQUISIÇÃO
            titulo_progress_bar['text'] = ('Configurando a requisição')      
            progress_bar['value'] += 40
            page.locator('xpath=//*[@id="__layout"]/div/main/div/div/div[2]/div/div[1]/section/div/div/div/button').click()
            page.locator('xpath=//*[@id="__layout"]/div/main/div/div/div[2]/div/div[1]/section/div[1]/div[2]/ul/li[1]/a').click()
            page.locator('xpath=//*[@id="__layout"]/div/main/div/div/div[2]/div/div[1]/section/div[1]/div[2]/ul[2]/li[1]/a').click()
            frame = page.frame_locator('#PopUpConfiguration-if')
            page.wait_for_timeout(1000)
            frame.locator('xpath=//*[@id="select2-Categoria_Value-container"]').click()
            page.wait_for_timeout(500)
            frame.locator('xpath=/html/body/span/span/span[1]/input').fill(cat_Pedido)
            page.wait_for_timeout(500)
            frame.locator('xpath=/html/body/span/span/span[1]/input').press('Enter')
            page.wait_for_timeout(500)
            frame.locator('xpath=//*[@id="BOrgs_1__BorgDescription"]').press('Tab')
            page.wait_for_timeout(500)
            if frame.locator('xpath=//*[@id="BOrgs_0__BorgDescription"]').input_value().strip() == "":
                frame.locator('xpath=//*[@id="BOrgs_0__BorgDescription"]').fill("1 - VERO S.A.")
            frame.locator('xpath=//*[@id="BOrgs_1__BorgDescription"]').press('Tab')
            page.wait_for_timeout(500)
            frame.locator('xpath=//*[@id="BOrgs_1__BorgDescription"]').fill(filial)
            frame.locator('xpath=//*[@id="BOrgs_1__BorgDescription"]').press('Tab')
            frame.locator('xpath=//*[@id="btnSave"]').click()

            # SELECIONA ITENS E QUANTIDADES
            titulo_progress_bar['text'] = ('Adicionando itens e quantidades')      
            progress_bar['value'] += 40
            for i in range(len(quant)):
                page.wait_for_timeout(1000)
                page.locator('xpath=//*[@id="Valor"]').fill(item[i])
                page.locator('xpath=//*[@id="btnSearchSimple"]').click()
                page.locator('.icon-shopping-cart').click()
                page.wait_for_timeout(1000)
                page.keyboard.press('Control+A')
                page.wait_for_timeout(1000)
                page.keyboard.type(quant[i])
                page.wait_for_timeout(1000)
                page.keyboard.press('Tab')
                page.wait_for_timeout(1000)
            page.locator('xpath=//*[@id="btnAvancar"]').click()

            # TELA CONDIÇÕES GERAIS
            titulo_progress_bar['text'] = ('Ajustando condições gerais')      
            progress_bar['value'] += 40
            page.locator('xpath=//*[@id="Titulo_Value"]').fill(titulo_requisicao)
            page.locator('xpath=//*[@id="DataEsperada_Value"]').fill(data_esperada)
            page.wait_for_timeout(500)
            page.locator('xpath=//*[@id="select2-LocalEntrega_Value-container"]').click()
            page.locator('xpath=/html/body/span/span/span[1]/input').fill(nome_filial)
            page.locator('xpath=/html/body/span/span/span[1]/input').press('Enter')
            page.locator('xpath=//*[@id="CentroCusto_Text"]').fill(centro_custo[:4])
            page.wait_for_timeout(1000)
            page.locator('xpath=//*[@id="ui-id-2"]').click()
            page.locator('xpath=//*[@id="select2-LocalFaturamento_Value-container"]').click()
            page.locator('xpath=/html/body/span/span/span[1]/input').fill(nome_filial)
            page.locator('xpath=/html/body/span/span/span[1]/input').press('Enter')
            page.locator('xpath=//*[@id="Observacao_Value"]').fill(comentario)
            page.locator('xpath=//*[@id="btnAvancar"]').click()
            
            #            TELA DETALHES DOS ITENS
            titulo_progress_bar['text'] = ('Ajustando detalhes dos itens')      
            progress_bar['value'] += 40
            for i in range(len(quant)):
                valorTotal = str(float(valorun[i]) * int(quant[i]))
                page.locator(f'xpath=//*[@id="Itens_{i}__PrecoEstimado_Value"]').fill(valorun[i].replace(".",","))
                page.locator(f'xpath=//*[@id="select2-Itens_{i}__CategoriaContabil_Value-container"]').click()
                page.locator(f'xpath=//*[@id="select2-Itens_{i}__CategoriaContabil_Value-container"]').press('Enter')
                page.wait_for_timeout(1000)
                if cat_Pedido == 'PEDIDO REGULARIZACAO':
                    page.locator(f'xpath=//*[@id="Itens_{i}__Attributes_0__valor"]').fill(valorTotal.replace(".",","))
                else:
                    page.locator(f'xpath=//*[@id="Itens_{i}__Attributes_1__valor"]').fill(titulo_requisicao)
                    page.locator(f'xpath=//*[@id="Itens_{i}__Attributes_0__valor"]').fill(valorTotal.replace(".",","))
            page.locator('xpath=//*[@id="btnAvancar"]').click()
            page.wait_for_timeout(1000)


            # FINALIZAR REQUISIÇÃO
            titulo_progress_bar['text'] = ('Finalizando a requisição')      
            progress_bar['value'] += 40
            if cat_Pedido == 'PEDIDO REGULARIZACAO':
                with page.expect_popup() as popup_info:
                    page.locator('xpath=//*[@id="anexoReq_link"]').click()
                    popup = popup_info.value
                    popup.wait_for_load_state()
                    popup.locator('xpath=//*[@id="fuArquivo"]').set_input_files(caminho_arquivo)
                    popup.locator('xpath=//*[@id="ctl00_conteudo_formUpload_btn_ctl00_conteudo_formUpload_btnEnviar"]').click()
                    popup.wait_for_load_state()
                    popup.close()

            page.locator('xpath=//*[@id="btnAvancar"]').click()
            requisicao = page.locator('.badge-code ')
            page.wait_for_timeout(1000)
            progress_bar['value'] += 40
            titulo_progress_bar['text'] = ('########### REQUISIÇÃO FINALIZADA ###########')
            caixa_numero_req.place(relx= .64, rely=.825)
            caixa_numero_req['text']('Sua requisição é: ')
            mensagem_titulo.place(relx= .35, rely=.77)
            mensagem_titulo['text'](titulo_requisicao)
            mensagem_numero_req.place(relx= .02, rely=.82)
            mensagem_numero_req.insert(INSERT, requisicao.inner_html().strip()[4:])
            if cat_Pedido == 'PEDIDO REGULARIZACAO':
                aba_ativa[ultimaLinha] = requisicao
    
    except TimeoutError:
        toaster.show_toast(f'Erro ao criar a requisição.',f'Lentidão no mercado eletronico!\n Tente novamente em alguns minutos!',icon_path=None, duration=20, threaded=True)    
      
def salvarArquivo(nome_arquivo, conteudo):
    arquivo = open(nome_arquivo, "w")
    arquivo.write(conteudo)
    print(conteudo)
    print(nome_arquivo)
    arquivo.close()

def abreArquivo(nome_arquivo):
    print(nome_arquivo)
    titulo = nome_arquivo.split('.')[0]
    janelaArquivos = Toplevel(janela)
    janelaArquivos.title(f'Editar informações de {titulo}')
    janelaArquivos.geometry('400x250')
    mensagem = Label(janelaArquivos, text='Inserir uma informação em cada linha!', font='calibri 11')
    mensagem.place(relx=.2, rely=0.02)
    caixa_texto = Text(janelaArquivos, height=10, width=40)
    caixa_texto.place(relx=.1, rely=0.15)
    botao_salvar = Button(janelaArquivos, text='Salvar', width=12 ,command=lambda: salvarArquivo(nome_arquivo, caixa_texto.get(1.0, END)))
    botao_salvar.place(relx=0.1, rely=0.85)
    botao_cancelar = Button(janelaArquivos, text='Cancelar', width=12 ,command=janelaArquivos.destroy)
    botao_cancelar.place(relx=0.68, rely=0.85)
    

    arquivo = open(nome_arquivo, "r", encoding="utf-8")
    conteudo = arquivo.read()
    caixa_texto.insert(END, conteudo)

def threading():
    Thread(target=printTeste).start()

def fecharjanelas():

    janela.destroy()


varcheckNavegador = BooleanVar()
varmonitorReq = BooleanVar()

checkNavegador = Checkbutton(janela, text='Abre Nav',variable=varcheckNavegador, offvalue=False, onvalue=True)
checkNavegador.place(relx=.02, rely=.02)

monitorReq = Checkbutton(janela, text='Monitor',variable=varmonitorReq, onvalue=True, offvalue=False, command=threading)
monitorReq.place(relx=.78, rely=.02)
monitorReq.select()
if varmonitorReq.get() is True:
    Thread(target=printTeste).start()

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

titulo_progress_bar = Label(janela, text="", font='calibri, 10')
titulo_progress_bar.place(relx= .34, rely=.68)
progress_bar = Progressbar(janela, orient= 'horizontal', mode='determinate', length=280)

mensagem_titulo = Label(janela, text="", font='calibri, 12')
mensagem_titulo.place(relx= .27, rely=.77)
mensagem_numero_req = Label(janela, text="", font='calibri, 11')
mensagem_numero_req.place(relx= .15, rely=.82)
caixa_numero_req = Text(janela, font='calibri, 10', width=15, height= 1)


janela.protocol("WM_DELETE_WINDOW", janela.destroy)
janela.config(menu=menubar)
janela.mainloop()