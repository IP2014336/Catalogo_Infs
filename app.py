import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
import smtplib
import ssl
import base64

from collections import OrderedDict
import textwrap
port = 465  # For SSL
# Create a secure SSL context
context = ssl.create_default_context()

#######################################
# Inicio do Indice
# 1 > Recupera Imagem homepage
# 2 > Recupera dados
# 3 > Define cores genéricas
# 4 > Definição das opções para os menus interativos
# 5 > Definição dos menus interativos
# 6 > Inicio do layout da app
#   6.1 > Título geral da página, por cima das Tabs
#   6.2 > Tabs do menu
# 7 > Callback das tabs
#   7.1 > Tab Inicial
#     7.1.1 > Call Imagem
#     7.1.2 > Quote
#     7.1.3 > Objetivos da app
#   7.2 > Tab Global
#     7.2.1 > Menu de anos
#     7.2.2 > Call Gráfico Globo
#     7.2.3 > Call Gráfico Paises com mais universidades no top200
#     7.2.4 > Call Gráfico Top 10 universidades
#   7.3 > Tab de Países
#     7.3.1 > Menu de país
#     7.3.2 > Call Cards do top 3 nacional
#     7.3.3 > Call de gráfico das universidades do país
#     7.3.4 > Menu de intervalo de datas
#   7.4 > Tab de Universidades
#     7.4.1 > Menu de universidade
#     7.4.2 > Call de scatter plot de evolução do score da universidade
#     7.4.3 > Call de 11 gráficos de barras de indicadores da universidade
#   7.5 > Tab de Indicadores (estática)
#     7.5.1 > Call de 4 scatter plots de indicadores vs score
#   7.6 > Tab de feedback
#     7.6.1 > Título
#     7.6.2 > Perguntas
#     7.6.3 > Caixa de comentario
#     7.6.4 > Call Botão de submissao
# 8 > app.callback para Tab Global
#   8.1 > Define gráfico das 10 melhores Universidades
#   8.2 > Define gráfico dos Paises com mais univ no top 200
#   8.3 > Define gráfico de Globo
# 9 > app.callback para Tab Paises
#   9.1 > Define Card 1
#   9.2 > Define Card 2
#   9.3 > Define Card 3
#   9.4 > Define Gráfico das Universidades do País
# 10 > app.callback para Tab Universidade
#   10.1 > Define gráfico da evolução do rank da universidade
#   10.2 > Define gráfico da evolução do nº de estudandes
#   10.3 > Define gráfico da evolução do nº de estudandes por funcionario
#   10.4 > Define gráfico da evolução do Teaching
#   10.5 > Define gráfico da evolução do Research
#   10.6 > Define gráfico da evolução do Citations
#   10.7 > Define gráfico da evolução do Industry_Income
#   10.8 > Define gráfico da evolução do International_Outlook
#   10.9 > Define gráfico da evolução do Pct_Female
#   10.10 > Define gráfico da % estudantes internacionais
# 11 > Define 4 scatter plots de indicadores vs score
#   11.1 > Constroi 1º gráfico
#   11.2 > Anotaçoes ao 1º gráfico
# 12 > Define botão de submissão e envio de formulario para email
# Fim do Indice
#######################################

# 1 > Recupera Imagem homepage
response = requests.get('https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/library-1082309_1280.jpg')
img = Image.open(BytesIO(response.content))
response2 = requests.get('https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/mapfre_logo_printscreen.jpg')
logo = Image.open(BytesIO(response2.content))

# 2 > Recupera dados
path = 'https://raw.githubusercontent.com/IP2014336/DVCLASS/master/'
df = pd.read_csv(path + 'THERanking.csv', sep=';', engine='python')
path = 'https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/'
dic = pd.read_csv(path + 'Dicionario_Mapfre.csv', sep=';', engine='python')
cat = pd.read_csv(path + '0_Catalogo_2021.csv', sep=';', engine='python')
logs = pd.read_csv(path + 'Log_Pedidos.csv', sep=';', engine='python')
pdf_path = 'https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/Simula_Nya.pdf'
# 3 > Define cores genéricas
colors = {
    'backsoftgrey': '#F5F5F5',
    'backmedgrey': '#d9d9d9',
    'backdarkgrey': '#A9A9A9',
    'text': '#ffffff',
    'bluetext': '#0000ff',
    'redtext': '#DC143C'
}
colorstit = {
    'background': '#b6cfe0',
    'text': '#737373'
}

box_style = {'width': 500, 'height': 50, 'padding': '5px', 'font-style': 'italic', 'backgroundColor': '#e6e6e6'}
bigbox_style = {'width': 350, 'height': 225, 'padding': '5px', 'font-style': 'italic', 'backgroundColor': '#e6e6e6'}
thinbox_style = {'width': 350, 'height': 50, 'padding': '5px', 'font-style': 'italic', 'backgroundColor': '#e6e6e6'}

P_style = {'padding': '5px', 'width': '30%', 'textAlign': 'right'}

grey_button_style = {'background-color': '#A9A9A9',
                     'color': 'white',
                     'height': '50px',
                     'width': '100px',
                     'margin-top': '50px',
                     'margin-left': '50px',
                     'font-size': '14px',
                     'marginTop': '5px'}

red_button_style = {'background-color': '#8B0000',
                    'color': 'white',
                    'height': '50px',
                    'width': '100px',
                    'margin-top': '50px',
                    'margin-left': '50px',
                    'font-size': '14px',
                    'marginTop': '5px'}

radio_style = {'textAlign': 'center',
               'padding': '5px',
               'border': 'thin solid #888888',
               #'width': '50%',
               'font-size': '12px',
               'box-shadow': '5px 5px #888888',
               'backgroundColor': colors['backsoftgrey']}

# 4 > Definição das opções para os menus interativos
area_options = [dict(label=area, value=area) for area in cat['AREA'].unique()]
University_options = [
    dict(label=University, value=University)
    for University in df['University'].unique()]
Letter_options = [
    dict(label=Letra, value=Letra)
    for Letra in dic['Letra'].unique()]

estados = ['EM PRODUÇÃO', 'DESCONTINUADO', 'EM DESENVOLVIMENTO']
estado_options = [dict(label=estado, value=estado) for estado in estados]

YesNo = ['Sim', 'Não']
YesNo_options = [dict(label=simnao, value=simnao) for simnao in YesNo]

tipos = ['Dataset', 'Informações', 'Todos']
tipo_options = [dict(label=tipo, value=tipo) for tipo in tipos]

uniquests = ['Oxford', 'Harvard ', 'Yale', 'Nova University of Lisbon', 'Dont know']
quest_options = [dict(label=uniquest, value=uniquest) for uniquest in uniquests]

formato_options = [dict(label=formato, value=formato) for formato in cat['FORMATO'].unique()]

DS_options = [dict(label=Data_stweard, value=Data_stweard) for Data_stweard in cat['DATA STEWARD'].unique()]

per_options = [dict(label=perio, value=perio) for perio in cat['PERIODICIDADE'].unique()]

letras = ['tudo', 'a', 'b ', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
          't', 'u', 'v', 'w', 'x', 'y', 'z']
letra_options = [dict(label=letra, value=letra) for letra in letras]
# 5 > Definição dos menus interativos
radio_perio = dcc.RadioItems(
    id='radio_perio',
    options=per_options,
    value='todos'
)
radio_formato = dcc.RadioItems(
    id='radio_formato',
    options=formato_options,
    value='todos'
)
radio_letra = dcc.RadioItems(
    id='radio_letra',
    options=letra_options,
    value='tudo'
)
radio_area = dcc.RadioItems(
    id='radio_area',
    options=area_options,
    value='Atuarial'
)
radio_DS = dcc.RadioItems(
    id='radio_DS',
    options=DS_options,
    value='Atuarial'
)
radio_estado = dcc.RadioItems(
    id='radio_estado',
    options=estado_options,
    value='EM PRODUÇÃO'
)
radio_tipo = dcc.RadioItems(
    id='radio_tipo',
    options=tipo_options,
    value='Todos'
)
#dropdown_univ = dcc.Dropdown(
#    id='university_drop',
#    options=University_options,
#    value='NOVA University of Lisbon',
 #   multi=False
#)
DicQuesttypes = ['Nova definição', 'Alteração de definição atual']
DicQuesttype_options = [dict(label=DicQuesttype, value=DicQuesttype) for DicQuesttype in DicQuesttypes]
RadioDicQuesttype=dcc.RadioItems(id='RadioDicQuesttype', options=DicQuesttype_options)


SliderYear = dcc.RangeSlider(
    id='year_slider',
    min=2016,
    max=2020,
    value=[2016, 2020],
    marks={'2016': '2016',
           '2017': '2017',
           '2018': '2018',
           '2019': '2019',
           '2020': '2020'},
    step=1
)
tab_height = '7vh'
# suppress_callback_exceptions=True para não dar erros com os callbacks das distintas tabs
app = dash.Dash(__name__, suppress_callback_exceptions=True )#, external_stylesheets=[dbc.themes.SIMPLEX]
server = app.server #Descomentar no github

# 6 > Inicio do layout da app
app.layout = html.Div([
    # 6.1 > Título geral da página, por cima das Tabs
    html.Div([
         html.Div([html.Br()], style={'width': '35%'}),
         html.Div([html.H1(children='Governo de Dados e Informações',
                           style={'color': colorstit['text'], 'marginTop': '10px', 'marginBottom': '10px'})]),
         html.Div([html.Br()], style={'width': '10%'}),
         html.Div([html.Img(src=logo, width="250", height="50")])
            ],  style={'textAlign': 'center', 'display': 'flex'}),
    # 6.2 > Tabs do menu
    dcc.Tabs(id='tabs', value='tab-1', style={'font-size': '90%', 'height': tab_height}, children=[
        dcc.Tab(label='Início',     value='tab-1', style={'line-height': tab_height, 'padding': '0'}),
        dcc.Tab(label='Dicionário', value='tab-2', style={'line-height': tab_height, 'padding': '0'}),
        dcc.Tab(label='Catálogo',   value='tab-3', style={'line-height': tab_height, 'padding': '0'}), #,   children=[
            # dcc.Tabs(id='subtabs',  value='subtab1', style={'height': tab_height}, children=[
             #   dcc.Tab(label='Consulta',  value='ConsultaCAT', style={'line-height': tab_height, 'padding': '0'}),
             #   dcc.Tab(label='Manutenção', value='GestaoCAT', style={'line-height': tab_height, 'padding': '0'})])
        #]),
        dcc.Tab(label='Norma', value='tab-4', style={'line-height': tab_height, 'padding': '0'}),
        dcc.Tab(label='Requisições', value='tab-5', style={'line-height': tab_height, 'padding': '0'} #, #children=[
           # dcc.Tabs(id='subtabs2', value='subtab2', style={'height': tab_height, 'padding': '0'}, children=[
             #   dcc.Tab(label='Pedido de Acesso', value='AccInf', style={'line-height': tab_height, 'padding': '0'}),
             #   dcc.Tab(label='Novos desenvolvimentos', value='NovaInf', style={'line-height': tab_height, 'padding': '0'}),
             #   dcc.Tab(label='Pedidos em curso', value='InfDevelop', style={'line-height': tab_height, 'padding': '0'})])
        #]
        ),
        dcc.Tab(label='Feedback', value='tab-6', style={'line-height': tab_height, 'padding': '0'}),
        dcc.Tab(label='DataStewards', value='tab-7', style={'line-height': tab_height, 'padding': '0'})
    ]),
    html.Div(id='tabs-content')
])


# 7 > Callback das tabs
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':  # 7.1 > Tab Inicial
        return html.Div([
            # 7.1.1 > Call Imagem
            html.Div([html.Div([html.Br()], style={'height': '3px'}), html.Img(src=img, width="590", height="420")]),
            html.Div([html.Br()], style={'width': '100px'}),
            html.Div([
                # 7.1.2 > Quote
                html.Br(),
                html.H1('"I did then what I knew how to do.',
                        style={'textAlign': 'right', 'marginTop': '0', 'marginBottom': '0'}),
                html.H1('Now that I know better, I do better"',
                        style={'textAlign': 'right', 'marginTop': '0', 'marginBottom': '0'}),
                html.H4('Maya Angelou',  style={'font-weight': 'normal', 'textAlign': 'right', 'font-size': '15px',
                                                     'font-style': 'italic', 'marginTop': '0', 'marginBottom': '0'}),
                # 7.1.3 > Objetivos da app
                html.Br(),
                html.Div([
                    html.H4(children="o ", style={'color': colors['redtext'], 'font-size': '15px'}),
                    html.Div([html.Br()], style={'width': '6px'}),
                    html.H4(children="Conheça os Dados e Informações que se produzem")
                    ], style={'display': 'flex', 'marginTop': '0', 'marginBottom': '0'}),
                html.Div([
                    html.H4(children="o ", style={'color': colors['redtext'], 'font-size': '15px'}),
                    html.Div([html.Br()], style={'width': '6px'}),
                    html.H4(children="Encontrou uma informação relevante para as suas funções?"),
                    html.H4(children="Peça aqui", style={'color': colors['bluetext'], 'font-size': '10px'})
                    ], style={'display': 'flex', 'marginTop': '0', 'marginBottom': '0'}),
                html.Div([
                    html.H4(children="o ", style={'color': colors['redtext'], 'font-size': '15px'}),
                    html.Div([html.Br()], style={'width': '6px'}),
                    html.H4(children="O que procura não existe?"),
                    html.H4(children="Peça aqui",
                            style={'color': colors['bluetext'], 'font-size': '10px', 'top': '50'})
                    ], style={'display': 'flex', 'marginTop': '0', 'marginBottom': '0'}),
                html.Div([
                    html.H4(children="o", style={'color': colors['redtext'], 'font-size': '15px'}),
                    html.Div([html.Br()], style={'width': '6px'}),
                    html.H4(children="Consulte o dicionário de termos da nossa empresa e sector")
                    ], style={'display': 'flex', 'marginTop': '0', 'marginBottom': '0'})
            ])
        ], style={'display': 'flex'})
    elif tab == 'tab-2':
        # 7.2 > Tab Dicionario
        return html.Div([
            # 7.2.1 > Menu de letras
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([html.H3(children='Dicionário de Termos', style={'marginTop': '0', 'marginBottom': '0'})
                      ], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                'box-shadow': '5px 5px #888888'}),
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([
                html.Div([html.H3(children='Utilize a primeira linha para filtrar os resultados',
                                  style={'marginTop': '1px', 'marginBottom': '1px', 'font-size': '12px',
                                         'font-style': 'italic'})
                          ],
                         style={'textAlign': 'left', 'padding': '1px', 'marginTop': '2px', 'color': colorstit['text']
                                # , 'border': 'thin solid #888888', 'backgroundColor': colors['background']
                                }),
                html.Div([dash_table.DataTable(
                    id='dictable',
                    data=dic.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in dic.columns],
                    style_cell={'textAlign': 'left', 'font_family': 'Cambria', 'font_size': '10px',
                                'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 250},
                    tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                                   for column, value in row.items()} for row in dic.to_dict('records')],
                    css=[{'selector': '.dash-table-tooltip',
                          'rule': 'background-color: grey; font-family: monospace; color: white'}],
                    tooltip_duration=None,
                    style_data_conditional=[{'if': {'row_index': 'odd'},
                                             'backgroundColor': 'rgb(248,248,248)'}],
                    filter_action='native',
                    style_header={'backgroundColor': '#DC143C', 'fontWeight': 'bold', 'font_size': '11px',
                                  'color': '#ffffff'},
                    page_action="native",
                    page_current=0,
                    page_size=10
                )]),
                html.Div([html.Br()], style={'height': '50px'}),
                html.Div([html.H3(children='Proponha alterações', style={'marginTop': '0', 'marginBottom': '0'})
                          ], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                    'box-shadow': '5px 5px #888888'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Selecione o tipo de proposta")],  style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    html.Div(RadioDicQuesttype, style={'marginBottom': '0px', 'marginTop': '15px'})
                ], style={'display': 'flex'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Nome")], style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    # 7.6.3 > Caixa de nome
                    html.Div([
                        dcc.Textarea(
                            id='nome',
                            value='Introduza o Nome do termo a criar/alterar',
                            style={'width': 550, 'height': 25, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                        )])
                ], style={'display': 'flex'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Definição")], style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    html.Div([
                        dcc.Textarea(
                            id='definicao',
                            value='Introduza a definição do termo',
                            style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                        )])
                ], style={'display': 'flex'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Relacionados")], style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    html.Div([
                        dcc.Textarea(
                            id='relacionados',
                            value='Introduza outros termos relacionados',
                            style={'width': 550, 'height': 25, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                        )])
                ], style={'display': 'flex'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Sinónimos")], style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    html.Div([
                        dcc.Textarea(
                            id='sinonimos',
                            value='Introduza outros termos sinónimos',
                            style={'width': 550, 'height': 25, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                        )])
                ], style={'display': 'flex'}),
                html.Div([
                    html.Div([html.Br()], style={'width': '5%'}),
                    html.Div([html.P("Comentários adicionais")], style={'width': '15%', 'textAlign': 'right'}),
                    html.Div([html.Br()], style={'width': '3%'}),
                    # 7.6.3 > Caixa de comentario
                    html.Div([
                        dcc.Textarea(
                            id='comentario',
                            value='utilize esta secção para escrever livremente o que considere necessário',
                            style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                        )])
                ], style={'display': 'flex'}),
                html.Div([html.Br()], style={'height': '15px'}),
                html.Div([
                    # 7.6.4 > Botão de submissao
                    html.Div([html.Br()], style={'width': '36%'}),
                    html.Div([html.Button(' Submeter ', id='submitbutton', n_clicks=0, style={})]),
                    html.Div(id='trigger', children=0, style=dict(display='none')),
                    html.Div([html.Br()], style={'width': '1%'}),
                    html.Div(id='container-button-basic',
                             style={'font-style': 'italic', 'font-size': '12px', 'marginTop': '5px'})
                ], style={'display': 'flex'}),
                html.Div([html.Br()], style={'height': '50px'})
            ], style={'textAlign': 'center', 'height': '390px'}),
        ]),
    elif tab == 'tab-3':  # 7.3 > Tab de Países
        return html.Div([
            html.Div([html.Br()], style={'height': '10px'}),
            # 7.3.1 > Menu de permissoes
            html.Div([html.H3(children='Seleccione o âmbito funcional', style={'marginTop': '0', 'marginBottom': '2px'}),
                      radio_area], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                          'box-shadow': '5px 5px #888888', 'backgroundColor': colors['backmedgrey']}),
            html.Div([
                    html.Div([html.H3(children='Seleccione o estado', style={'marginTop': '0', 'marginBottom': '2px'}),
                              radio_estado],
                             style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                    'width': '50%', 'font-size': '12px',
                                    'box-shadow': '5px 5px #888888', 'backgroundColor': colors['backsoftgrey']}),
                    html.Div([html.H3(children='Seleccione o tipo', style={'marginTop': '0', 'marginBottom': '2px'}),
                              radio_tipo],
                             style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                    'width': '50%', 'font-size': '12px',
                                    'box-shadow': '5px 5px #888888', 'backgroundColor': colors['backsoftgrey']})
                ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '5px'}),
            html.Div([
                html.Div([html.H3(children='Utilize a primeira linha para filtrar os resultados',
                                  style={'marginTop': '1px', 'marginBottom': '1px', 'font-size': '12px',
                                         'font-style': 'italic'})
                          ],
                         style={'textAlign': 'left', 'padding': '1px', 'marginTop': '2px', 'color': colorstit['text']
                                # , 'border': 'thin solid #888888', 'backgroundColor': colors['background']
                                })
                ]),
            html.Div([dash_table.DataTable(
                id='cattable',
                data=cat.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in cat.columns],
                style_cell={'textAlign': 'left', 'font_family': 'Cambria', 'font_size': '10px',
                            'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 100},
                tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                               for column, value in row.items()} for row in cat.to_dict('records')],
                css=[{'selector': '.dash-table-tooltip',
                      'rule': 'background-color: grey; font-family: monospace; color: white'}],
                tooltip_duration=None,
                style_data_conditional=[{'if': {'row_index': 'odd'},
                                         'backgroundColor': 'rgb(248,248,248)'}],
                filter_action='native',
                style_header={'backgroundColor': '#DC143C', 'fontWeight': 'bold', 'font_size': '11px',
                              'color': '#ffffff'},
                page_action="native",
                page_current=0,
                page_size=10
            )]),
            html.Div([html.Br()], style={'height': '50px'}),
            html.Div([html.H3(children='Solicite acesso', style={'marginTop': '0', 'marginBottom': '0'})
                      ], style={'textAlign': 'center', 'padding': '5px', 'border': 'thin solid #888888',
                                'box-shadow': '5px 5px #888888'}),
            html.Div([html.Br()], style={'height': '25px'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Nome do peticionário")], style={'width': '15%', 'textAlign': 'right'}),
                html.Div([html.Br()], style={'width': '3%'}),
                    # 7.6.3 > Caixa de nome
                html.Div([
                    dcc.Textarea(
                        id='petic',
                        value='Introduza o Nome, email e cargo da(s) pessoa(s) a serem adicionadas à lista de distribuição',
                        style={'width': 550, 'height': 25, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Justificação")], style={'width': '15%', 'textAlign': 'right'}),
                html.Div([html.Br()], style={'width': '3%'}),
                html.Div([
                    dcc.Textarea(
                        id='why',
                        value='Por favor introduza o motivo pelo qual requer o acesso',
                        style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Nº da ficha")], style={'width': '15%', 'textAlign': 'right'}),
                html.Div([html.Br()], style={'width': '3%'}),
                html.Div([
                    dcc.Textarea(
                        id='ficha',
                        value='Introduza o Nº da ficha a que pretende ter acesso',
                        style={'width': 550, 'height': 25, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([
                    # 7.6.4 > Botão de submissao
                html.Div([html.Br()], style={'width': '36%'}),
                html.Div([html.Button(' Submeter ', id='submitbutton2', n_clicks=0, style={})]),
                html.Div(id='trigger2', children=0, style=dict(display='none')),
                html.Div([html.Br()], style={'width': '1%'}),
                html.Div(id='container-button-basic2',
                            style={'font-style': 'italic', 'font-size': '12px', 'marginTop': '5px'})
            ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '50px'})
        ])
    elif tab == 'tab-4':  # 7.4 > Tab de Politica
        return html.Div([
             html.Div([
                html.H1('Norma de Governo de Dados e Informação', style={'color': colors['redtext'], 'align': 'center'}),
                html.H4(children="Incluir texto na norma ", style={'font-size': '12px'})
             ]),
        ])
    elif tab == 'tab-5':  # 7.5 > Tab de Requisições
        return html.Div([
            html.Div([html.Br()], style={'height': '7px'}),
            html.Div([
                # 7.5.1 > Call de 4 scatter plots de indicadores vs score
                html.Div([dcc.Graph(id='c1', figure=corr1)], style={'width': '35%', 'padding': '0px', 'height': '400px',
                                                                    'border': 'thin solid #888888',
                                                                    'box-shadow': '5px 5px #888888'}),
                html.Div([html.Br()], style={'width': '2%'}),
                html.Div([
                    html.Div([html.H3(children='Solicite a Nova Informação que necessita')]),
                    html.Div([
                        html.Div([
                            html.Div([html.H3(children='Âmbito funcional'), radio_area], style=radio_style),
                            html.Div([html.H3(children='Periodicidade'), radio_perio], style=radio_style),
                            html.Div([html.H3(children='Tipo de Informação'), radio_tipo], style=radio_style),
                            html.Div([html.H3(children='Formato'), radio_formato], style=radio_style)
                        ]),
                        html.Div([
                            html.Div([html.Div([html.P("Descritivo")], style=P_style),
                                     html.Div([dcc.Textarea(id='Descritivo', style=bigbox_style,
                                                            value='Introduza a descrição da informação que pretende')])
                                      ], style={'padding': '5px', 'display': 'flex'}),
                            html.Div([html.Div([html.P("Distribuição")], style=P_style),
                                     html.Div([dcc.Textarea(id='listadistri', style=thinbox_style,
                                                        value='Introduza a quem a informação será distribuida')])
                                     ], style={'padding': '5px', 'display': 'flex'}),
                            ])
                        ], style={'padding': '5px', 'display': 'flex'}),
                    ]),
                ], style={'padding': '5px', 'display': 'flex'}),

            # 7.6.4 > Botão de submissao
            html.Div([
                html.Div([html.Br()], style={'width': '50%'}),
                html.Div([html.Button(' Submeter ',
                                      id='submitbutton4', n_clicks=0,
                                      style=red_button_style)]),
                html.Div(id='trigger4', children=0, style=dict(display='none')),
                html.Div([html.Br()], style={'width': '1%'}),
                html.Div(id='container-button-basic4')
            ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '50px'}),
        ])
    elif tab == 'tab-6':  # 7.6 > Tab de feedback
        return html.Div([
            # 7.6.1 > Título
            #html.Div([html.Button("Download", id="btn"), Download(id="download")]),
            html.H1('Help us improve!', style={'color': '#669999', 'text-shadow': '2px 0px black'}),
            # 7.6.2 > Perguntas
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The visualizations are intuitive and easy to use")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
              #  html.Div([RadioGrade1], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The visualizations loaded quickly")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
             #   html.Div([RadioGrade2], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("This is an important subject to me")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
              #  html.Div([RadioGrade3], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("I was able to gather relevant information")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
             #   html.Div([RadioGrade4], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("The application has all the options I expected")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
             #   html.Div([RadioGrade5], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("I am satisfied with the overall application")],
                         style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
             #   html.Div([RadioGrade6], style={'marginBottom': '0px', 'marginTop': '15px', 'height': '20px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Do you now know which is the world best University in 2020?")],
                         style={'width': '35%'}),
                html.Div([html.Br()], style={'width': '3%'}),
            #    html.Div(RadioQuest, style={'marginBottom': '0px', 'marginTop': '15px'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Feel free to leave any comment")], style={'width': '35%'}),
                html.Div([html.Br()], style={'width': '3%'}),
                # 7.6.3 > Caixa de comentario
                html.Div([
                    dcc.Textarea(
                        id='comentario',
                        value='write here',
                        style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '15px'}),
            html.Div([
                # 7.6.4 > Botão de submissao
                html.Div([html.Br()], style={'width': '36%'}),
                html.Div([html.Button(' Submit ', id='submitbutton', n_clicks=0, style={})]),
                html.Div(id='trigger', children=0, style=dict(display='none')),
                html.Div([html.Br()], style={'width': '1%'}),
                html.Div(id='container-button-basic',
                         style={'font-style': 'italic', 'font-size': '12px', 'marginTop': '5px'})
            ], style={'display': 'flex'})
        ])
    elif tab == 'tab-7':
        return \
            html.Div([
                html.H1('Área Reservada a Data Steward(ess)!', style={'color': '#669999', 'text-shadow': '2px 0px black'}),
                html.Div([
                    html.Div([
                        html.Div([html.H3(children='Âmbito funcional'), radio_area], style=radio_style),
                        html.Div([html.H3(children='Periodicidade'), radio_perio], style=radio_style),
                        html.Div([html.H3(children='Estado'), radio_estado], style=radio_style),
                        html.Div([html.H3(children='Tipo de Informação'), radio_tipo], style=radio_style),
                        html.Div([html.H3(children='Formato'), radio_formato], style=radio_style)
                        ]),
                    html.Div([
                        html.Div([html.Div([html.P("Nome")], style=P_style),
                                  html.Div([dcc.Textarea(id='nome', style=box_style,
                                                         value='Introduza o Nome da ficha a criar/alterar')])
                                  ], style={'padding': '5px', 'display': 'flex'}),
                        html.Div([html.Div([html.P("Descritivo")], style=P_style),
                                  html.Div([dcc.Textarea(id='Descritivo', style=box_style,
                                                         value='Introduza a descrição do conteúdo')])
                                  ], style={'padding': '5px', 'display': 'flex'}),
                        html.Div([html.Div([html.P("Distribuição")], style=P_style),
                                  html.Div([dcc.Textarea(id='listadistri', style=box_style,
                                                         value='Introduza a quem a informação é distribuida')])
                                  ], style={'padding': '5px', 'display': 'flex'}),
                        html.Div([html.Div([html.P("Comentários adicionais")], style=P_style),
                                  html.Div([dcc.Textarea(id='comentario', style=box_style,
                                                         value='utilize esta secção para escrever livremente o que considere necessário')])
                                  ], style={'padding': '5px',  'display': 'flex'}),
                        html.Div([html.H3(children='Data Steward(ess)'), radio_DS], style=radio_style),
                        ])
                    ], style={'padding': '5px', 'display': 'flex'}),
                # 7.6.4 > Botão de submissao
                html.Div([
                    html.Div([html.Br()], style={'height': '125px'}),
                    html.Div([html.Button(' Submeter ',
                                          id='submitbutton3', n_clicks=0,
                                          style=red_button_style)]),
                    html.Div(id='trigger3', children=0, style=dict(display='none')),
                    html.Div([html.Br()], style={'width': '1%'}),
                    html.Div(id='container-button-basic3')
                ]),
                html.Div([html.Br()], style={'height': '50px'}),
                html.Div([dash_table.DataTable(
                        id='cattable',
                        data=cat.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in cat.columns],
                        style_cell={'textAlign': 'left', 'font_family': 'Cambria', 'font_size': '12px',
                                    'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 250},
                        tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                                       for column, value in row.items()} for row in cat.to_dict('records')],
                        css=[{'selector': '.dash-table-tooltip',
                              'rule': 'background-color: grey; font-family: monospace; color: white'}],
                        tooltip_duration=None,
                        style_data_conditional=[{'if': {'row_index': 'odd'},
                                                 'backgroundColor': 'rgb(248,248,248)'}],
                        filter_action='native',
                        style_header={'backgroundColor': '#DC143C', 'fontWeight': 'bold', 'font_size': '13px',
                                      'color': '#ffffff'},
                        page_action="native",
                        page_current=0,
                        page_size=10
                    )]),
                html.Div([html.Br()], style={'height': '50px'})
            ], style={'textAlign': 'center', 'height': '390px'})


# 8 > app.callback para GLOBAL
#@app.callback(
#    [Output('tabdic', 'value')#,
#     #Output('top10uni', 'figure'),
#     #Output('top10country', 'figure'),
 #    #Output('globe', 'figure')
#     ],
#    [Input('RadioLetter', 'value')]
#)
#def update_graph(letter):
#    dfdic = dic.loc[dic['Letra'] == letter]
#    tabdic = dash_table.DataTable(
#        id='tabdic',
#        columns=[{'name': i, 'id': i} for i in dfdic.columns],
#        style_cell={'textAlign': 'left'},
#        data=dfdic.to_dict('records'),
#        style_data={'whiteSpace': 'normal'}
#    )
 #   return dfdic
#def update_graph(year2):
    # 8.1 > Define gráfico das 10 melhores Universidades
 #   df_year2 = df.loc[df['Year'] == year2]
#    df_topu = df_year2.loc[df_year2['Rank'] <= 10].sort_values(by='ScoreResult', ascending=False)
#    figtopu = px.bar(data_frame=df_topu,
 #                    x=df_topu['ScoreResult'],
#                     y=df_topu['University'],
#                     color=df_topu['Country'],
#                     text=df_topu['Rank'],
#                     color_discrete_sequence=px.colors.sequential.Viridis_r,
#                     orientation='h',
##                     opacity=0.8,
 #                    barmode='relative',
#                     height=390,
#                     title='<b>TOP 10 Universities world wide in ' + str(year2))
##    figtopu.update_layout(margin=dict(l=20, r=20, t=40, b=20), titlefont=dict(size=15),
 #                         title={'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
 ##   figtopu.update_layout({'paper_bgcolor': 'rgba(255, 255, 255, 0)'})
 #   figtopu.update_layout(yaxis_categoryorder='total ascending')
    #   8.2 > Define gráfico dos Paises com mais univ no top 200
 #   df_topc = df_year2.loc[df_year2['Rank'] <= 200][['Country', 'Rank', 'University', 'ScoreResult']]
  #  countrylist = df_topc['Country'].value_counts()[:10].sort_values(ascending=False).index
  #  df_topc3 = df_topc[df_topc['Country'].isin(countrylist)]
  #  df_topc3.loc[:, 'count'] = df_topc3.groupby('Country')['Country'].transform('count')
  #  df_topc3 = df_topc3.sort_values(by=['count', 'Rank'], ascending=False)
  #  figtopc = px.bar(data_frame=df_topc3,
  #                   x=df_topc3['Rank'],
   #                  y=df_topc3['Country'],
   #                  color=df_topc3['Country'],
    #                 hover_name=df_topc3['University'],
     #                color_discrete_sequence=px.colors.sequential.Viridis_r,
      #               orientation='h',
       #              opacity=0.9,
        #             barmode='relative',
         #            height=390,
          #           title='<b>TOP 10 Countries with most universities on TOP 200 in ' + str(year2))
 #   figtopc.update_layout(margin=dict(l=20, r=20, t=40, b=20), titlefont=dict(size=15), showlegend=False,
  #                        xaxis=dict(title='<i><b>Stacked Ranks', showgrid=False, zeroline=False, showticklabels=False),
   #                       title={'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    # 8.3 > Define gráfico de Globo
#    df_NR1 = df_year2.loc[df_year2['National_Rank'] == 1][['Country', 'Rank', 'ScoreResult', 'University']]
#
 #   data_choropleth = dict(type='choropleth',
  #                         locations=df_NR1['Country'],
   #                        locationmode='country names',
    #                       z=df_NR1['ScoreResult'],
     #                      text=df_NR1['Country'] + '<br>' + df_NR1['University'] + '<br>' +
      #                          'World Rank: ' + df_NR1['Rank'].apply(str),
       #                    colorscale='viridis',
        #                   reversescale=True
         #                  )

  #  layout_choropleth = dict(geo=dict(scope='world',  # default
   #                                   projection=dict(type='orthographic'),
    #                                  landcolor='black',
     #                                 lakecolor='white',
      #                                showocean=True,  # default = False
       #                               oceancolor='azure'
        #                              ),
         #                    title=dict(text='<b>University Rank ' + str(year2) + '</b><br>'
          #                                   + '<i>top scored in country',
           #                             x=.47  # Title relative position according to the xaxis, range (0,1)
            #                            ),
             #                height=350
              #               )

  #  fig_choropleth = go.Figure(data=data_choropleth, layout=layout_choropleth)
  #  fig_choropleth.update_layout(margin=dict(l=5, r=5, t=50, b=10), titlefont=dict(size=15))
  #  fig_choropleth.update_layout({
  #      'plot_bgcolor': 'rgba(95, 158, 160, 0)',
   #     'paper_bgcolor': 'rgba(95, 158, 160, 0)'
    #})
    # Graficos para GLOBAL END
   # return figtopu, figtopc, fig_choropleth


# 9 > app.callback para Tab Países
@app.callback(
    Output('first_card', 'children'),
    [Input('area_radio', 'value'),
     Input('estado_radio', 'value'),
     Input('tipo_radio', 'value')]
)
def update_graph(area, estado, tipo):
    cat_cards = cat.loc[(cat['AREA'] == area)]
    # 9.1 > Define Card 1
    for aux in range(0, 1):
        cat_1cards = cat_cards.iloc[[aux]]
        first_card = dbc.Card([
            html.Br(), html.Br(), html.Br(), html.Br(),
            dbc.CardHeader("Ficha 1", style={'color': colors['text']}),
            dbc.CardBody(
                [
                    html.H3(cat_1cards['NOME'], className="card-title",
                            style={'color': '#75a3a3', 'text-shadow': '1px 0px grey'}),
                    html.H5("Formato: " + cat_1cards['FORMATO'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Periodicidade: " + cat_1cards['PERIODICIDADE'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Estado: " + cat_1cards['ESTADO'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Produtor: " + cat_1cards['PRODUTOR'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Data Steward : " + cat_1cards['DATA STEWARD'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Distribuição: " + cat_1cards['DISTRIBUIÇÃO'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Forma Distribuição: " + cat_1cards['FORMA DISTRIBUIÇÃO'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.H5("Data Atualização: " + cat_1cards['Data Atualização'].apply(str),
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
                    html.P("Descritivo: " + cat_1cards['DESCRITIVO'].apply(str), className="card-text",
                            style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']})
                ]),
        ], style={"width": "25rem", 'line-height': '2px', 'textAlign': 'center', "border": "2px black solid",
                  'backgroundColor': 'rgba(0, 0, 0, 1)'})
    # 9.2 > Define Card 2
    #df_2cards = df_cards.loc[df['National_Rank'] == 2]
    #second_card = dbc.Card([
    #    html.Br(), html.Br(), html.Br(), html.Br(),
     #   dbc.CardHeader("Nº 2 National Rank", style={'color': colors['text']}),
      #  dbc.CardBody(
       #     [
        #        html.H3(df_2cards['University'], className="card-title",
         #               style={'color': '#75a3a3', 'text-shadow': '1px 0px grey'}),
          #      html.H5("World Rank: " + df_2cards['Rank'].apply(str),
    #             style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
            #    html.H5("Nº of Students: " + df_2cards['Number_students'].apply(str),
             #           style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #  html.H5("Nº of Students per staff: " + df_2cards['Numbstudentsper_Staff'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #           html.H5("% International Students: " + df_2cards['International_Students'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #           html.H5("% Females : " + df_2cards['Pct_Female'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    ##           html.H5("Teaching: " + df_2cards['Teaching'].apply(str),
    #                  style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #           html.H5("Research: " + df_2cards['Research'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #           html.H5("Citations: " + df_2cards['Citations'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    ###           html.H5("Industry Income: " + df_2cards['Industry_Income'].apply(str),
    #                 style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']}),
    #           html.H5("International Outlook: " + df_2cards['International_Outlook'].apply(str),
    #                   style={'marginTop': '5px', 'marginBottom': '15px', 'color': colors['text']})
    #       ]),
    #], style={"width": "25rem", 'line-height': '2px', 'textAlign': 'center', "border": "2px black solid",
    #         'backgroundColor': 'rgba(0, 0, 0, 0.6)'})

    # 9.4 > Define Gráfico das Universidades do País
  #  by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]
   # full_filtered_df = by_year_df.loc[by_year_df['Country'] == country]
    #fig = px.scatter(full_filtered_df,
     #                x=full_filtered_df['Year'],
      #               y=full_filtered_df['Rank'],
       #              color=full_filtered_df['University'],
        #             symbol=full_filtered_df['Country'],
         #            hover_data=['University', 'National_Rank'],
          #           height=400,
           #          title='Ranks for Universities from ' + '<b>' + country + '</b> between ' +
            #               '<b>' + str(year[0]) + '</b> and ' + '<b>' + str(year[1])
             #        )
   # fig.update_layout({
    #    'plot_bgcolor': 'rgba(95, 158, 160, 0.1)',
     #   'paper_bgcolor': 'rgba(95, 158, 160, 0)'
   # })
   # fig.update_yaxes(autorange="reversed")
   # fig.update_layout(xaxis_type='category', title={'y': 0.97, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',
    #                                                'font_color': 'black'},
     #                 legend=dict(x=1, y=1), titlefont=dict(size=15), margin=dict(l=300, r=5, t=40, b=5),
      #                plot_bgcolor='rgba(255, 255, 255, 0.1)', paper_bgcolor='rgba(95, 158, 160, 0)')
    #fig.update_traces(marker=dict(size=10, line=dict(width=1, color='grey'), opacity=0.7),
     #                 selector=dict(mode='markers'))

    return first_card
# Gráficos para Countries END

@app.callback(
    [Output('db_table3', 'data')],
    [Input('radio_letra', 'value')]
)
def generate_table(max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dic.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dic.iloc[i][col]) for col in dic.columns
            ]) for i in range(min(len(dic), max_rows))
        ])
    ])

# 10 > app.callback para Tab Universidade
@app.callback(
    [Output('uni_evol', 'figure'),
     Output('measure1', 'figure'),
     Output('measure2', 'figure'),
     Output('measure3', 'figure'),
     Output('measure4', 'figure'),
     Output('measure5', 'figure'),
     Output('measure6', 'figure'),
     Output('measure7', 'figure'),
     Output('measure8', 'figure'),
     Output('measure9', 'figure')],
    [Input('university_drop', 'value')]
)
def update_graph(university):
    df_univ = df.loc[df['University'] == university]
    # 10.1 > Define gráfico da evolução do rank da universidade
    figun = px.scatter(df_univ, x=df_univ['Year'], y=df_univ['ScoreResult'], width=500, height=500,
                       title='<b>World Rank: Score Results <br> </b> <i> evolution 2016-2020')
    figun.update_layout(plot_bgcolor='rgba(255, 255, 255, 0.1)', paper_bgcolor='rgba(95, 158, 160, 0)',
                        titlefont=dict(size=15),
                        title={'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    figun.data[0].update(mode='markers+lines')
    figun.update_traces(marker=dict(size=25, color='#004080', line=dict(width=2, color='white'), opacity=0.8))

    for ano in df['Year'].unique():
        if not df_univ.loc[df_univ['Year'] == ano].empty:
            figun.add_annotation(x=ano, y=df_univ.loc[df_univ['Year'] == ano]['ScoreResult'].values[0], font=dict(size=10),
                                 text='Rank: <b>' + str(df_univ.loc[df_univ['Year'] == ano]['Rank'].values[0])
                                 , xref="x", yref="y", showarrow=True, arrowhead=7, ax=0, ay=-20,)

    # 10.2 > Define gráfico da evolução do nº de estudandes
    measure1 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Number_students'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkCyan"],
                      title='<b>Nº of Students')
    measure1.update_layout(margin=dict(l=5, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.3 > Define gráfico da evolução do nº de estudandes por funcionario
    measure2 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Numbstudentsper_Staff'], orientation='v',
                      opacity=0.9, barmode='relative', height=218, width=230, color_discrete_sequence=["CadetBlue"],
                      title='<b>Nº of Students per staff')
    measure2.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.4 > Define gráfico da evolução do Teaching
    measure3 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Teaching'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkSeaGreen"],
                      title='<b>Teaching')
    measure3.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.5 > Define gráfico da evolução do Research
    measure4 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Research'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["ForestGreen"],
                      title='<b>Research')
    measure4.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)",
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False),
                           xaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.6 > Define gráfico da evolução do Citations
    measure5 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Citations'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkOliveGreen"],
                      title='<b>Citations')
    measure5.update_layout(margin=dict(l=5, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(title_text="", showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.7 > Define gráfico da evolução do Industry_Income
    measure6 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Industry_Income'], orientation='v', opacity=0.9,
                      barmode='relative', height=218, width=230, color_discrete_sequence=["DarkSlateGrey"],
                      title='<b>Industry Outcome')
    measure6.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(title_text="", showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.8 > Define gráfico da evolução do International_Outlook
    measure7 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['International_Outlook'],
                      opacity=0.9, orientation='v',
                      barmode='relative', height=218, width=230, color_discrete_sequence=["Gray"],
                      title='<b>International Outlook')
    measure7.update_layout(margin=dict(l=10, r=10, t=23, b=5), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.9 > Define gráfico da evolução do Pct_Female
    measure8 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['Pct_Female'], orientation='v', opacity=0.9,
                      barmode='stack', height=218, width=230, color_discrete_sequence=["magenta"],
                      title='<b>% Females & Males')
    aux = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['PCT_Male'])
    measure8.add_trace(aux.data[0])
    measure8.update_layout(margin=dict(l=10, r=10, t=23, b=0), font=dict(size=10), titlefont=dict(size=10),
                           paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                           title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                           yaxis=dict(title_text="", showgrid=False, zeroline=False))
    # 10.10 > Define gráfico da % estudantes internacionais
    measure9 = px.bar(data_frame=df_univ, x=df_univ['Year'], y=df_univ['International_Students'], orientation='v',
                       opacity=0.9, barmode='stack', height=218, width=230, color_discrete_sequence=["#c2c2a3"],
                       title='<b>% International Students')
    measure9.update_layout(margin=dict(l=10, r=10, t=23, b=0), font=dict(size=10), titlefont=dict(size=10),
                            paper_bgcolor="rgba(95, 158, 160, 0)", xaxis=dict(showgrid=False, zeroline=False),
                            title={'y': 0.95, 'x': 0.6, 'xanchor': 'center', 'yanchor': 'top'},
                            yaxis=dict(title_text="", showgrid=False, zeroline=False))

    return figun, measure1, measure2, measure3, measure4, measure5, measure6, measure7, measure8, measure9
# Gráficos para Universities END


@app.callback(Output('submitbutton', 'style'), [Input('submitbutton', 'n_clicks')])
def change_button_style(n_clicks):
    if n_clicks > 0:
        return grey_button_style
    else:
        return red_button_style

# 11 > Define 4 scatter plots de indicadores vs score
# 11.1 > Constroi 1º gráfico
corr1 = px.bar(logs,
               x=logs['Estado'],
               title='<b>Nº Pedidos </b> por <b>Estado',
               height=400, width=400,
               color_discrete_sequence=px.colors.sequential.Viridis_r,
               opacity=0.8
               )
corr1.update_layout(margin=dict(l=0, r=0, t=60, b=10, pad=0),
                    title={'y': 0.97, 'x': 0.55, 'xanchor': 'center', 'yanchor': 'top'},
                    yaxis=dict(showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    xaxis=dict(title_text="Nº Pedidos", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    legend_orientation="h", legend_title_text='')

corr2 = px.scatter(df,
                   x=df['Pct_Female'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>%Females',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr2.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    title={'y': 0.97, 'x': 0.56, 'xanchor': 'center', 'yanchor': 'top'},
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="%Female", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['Pct_Female'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr2.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['Pct_Female'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr2.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))

corr3 = px.scatter(df,
                   x=df['Numbstudentsper_Staff'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>Nº Students per staff',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr3.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="Nº Students per staff", showgrid=False,
                               zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    title={'y': 0.97, 'x': 0.56, 'xanchor': 'center', 'yanchor': 'top'},
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['Numbstudentsper_Staff'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr3.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['Numbstudentsper_Staff'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr3.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))

corr4 = px.scatter(df,
                   x=df['International_Students'],
                   y=df['ScoreResult'],
                   color=df['Year'].apply(str),
                   hover_data=['University'],
                   title='<b>Score Results </b><br>    vs   <br><b>% Students International Students',
                   height=460, width=290,
                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                   opacity=0.8
                   )
corr4.update_layout(margin=dict(l=0, r=0, t=60, b=0, pad=0),
                    yaxis=dict(showgrid=False, zeroline=False),
                    xaxis=dict(title_text="% International Students", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    title={'y': 0.97, 'x': 0.55, 'xanchor': 'center', 'yanchor': 'top'},
                    legend_orientation="h", legend_title_text='')
ax = 0
ay = -50
for ano in df['Year'].unique():
    df_ano = df.loc[df['Year'] == ano]
    minx = df_ano.loc[df_ano['Rank'] == 1]['International_Students'].values[0]
    miny = df_ano.loc[df_ano['Rank'] == 1]['ScoreResult'].values[0]
    corr4.add_annotation(x=minx, y=miny, text="1º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=ax, ay=ay, font=dict(size=7))
    ax = ax + 20
    ay = ay + 12
    rankmax = df_ano['Rank'].max()
    maxx = df_ano.loc[df_ano['Rank'] == rankmax]['International_Students'].values[0]
    maxy = df_ano.loc[df_ano['Rank'] == rankmax]['ScoreResult'].values[0]
    corr4.add_annotation(x=maxx, y=maxy, text=str(rankmax) + "º [" + str(ano) + ']', xref="x", yref="y",
                         showarrow=True, arrowhead=7, ax=30, ay=0, font=dict(size=7))


# 12 > Define botão de submissão do dic
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submitbutton', 'n_clicks'),
     Input('trigger', 'children'),
     Input('RadioDicQuesttype', 'value'),
     Input('nome', 'value'),
     Input('definicao', 'value'),
     Input('relacionados', 'value'),
     Input('sinonimos', 'value'),
     Input('comentario', 'value')])
def update_output(n_clicks, trigger, quest1, nome, defi, relac, sino, comment):
    contextc = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if contextc == 'submitbutton':
        if n_clicks == 1:
            resposta = 'Tipo: ' + str(quest1) + ' Nome: '  + str(nome) + ' Definicao: '  + str(defi) + \
                       'relacionados: ' + str(relac) + 'sinonimo: ' + str(sino) + 'comment: ' + str(comment)
            resposta = resposta.encode('utf-8', 'ignore').decode('utf-8')
            password = '!Nova!Heroku2020'
            message = """\
            Subject: Hi there
            This message is sent from Python.""" + resposta
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("IMS.GrupoTopUniv@gmail.com", password)
                server.sendmail("IMS.GrupoTopUniv@gmail.com", "IMS.GrupoTopUniv@gmail.com", message)
            return 'Solicitação registada. Obrigada!'
        else:
            return 'Feedback had already been submitted'
# 12 > Define botão de submissão do cat
@app.callback(
    dash.dependencies.Output('container-button-basic2', 'children'),
    [dash.dependencies.Input('submitbutton2', 'n_clicks'),
     Input('trigger2', 'children'),
     Input('petic', 'value'),
     Input('ficha', 'value'),
     Input('why', 'value')])
def update_output(n_clicks, trigger2, petic, ficha, why):
    contextc = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if contextc == 'submitbutton2':
        if n_clicks == 1:
            resposta = 'peticionarios: ' + str(petic) + 'ficha: ' + str(ficha) + 'porquÊ: ' + str(why)
            resposta = resposta.encode('utf-8', 'ignore').decode('utf-8')
            password = '!Nova!Heroku2020'
            message = """\
            Subject: Hi there
            This message is sent from Python.""" + resposta
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("IMS.GrupoTopUniv@gmail.com", password)
                server.sendmail("IMS.GrupoTopUniv@gmail.com", "IMS.GrupoTopUniv@gmail.com", message)
            return 'Solicitação registada. Obrigada!'
        else:
            return 'Feedback had already been submitted'
# 12 > Define botão de submissão do DS
@app.callback(
    dash.dependencies.Output('container-button-basic3', 'children'),
    [dash.dependencies.Input('submitbutton3', 'n_clicks'),
     Input('trigger3', 'children'),
     Input('nome', 'value'),
     Input('Descritivo', 'value'),
     Input('listadistri', 'value'),
     Input('comentario', 'value')])
def update_output(n_clicks, trigger3, nome, Descritivo, listadistri,comentario):
    contextc = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if contextc == 'submitbutton3':
        if n_clicks == 1:
            resposta = 'peticionarios: ' + str(nome) + 'ficha: ' + str(Descritivo) + 'porquÊ: ' + str(listadistri)+ str(comentario)
            resposta = resposta.encode('utf-8', 'ignore').decode('utf-8')
            password = '!Nova!Heroku2020'
            message = """\
            Subject: Hi there
            This message is sent from Python.""" + resposta
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("IMS.GrupoTopUniv@gmail.com", password)
                server.sendmail("IMS.GrupoTopUniv@gmail.com", "IMS.GrupoTopUniv@gmail.com", message)
            return 'Ficha registada. Obrigada!'
        else:
            return 'Feedback had already been submitted'
# 12 > Define botão de submissão do DS
@app.callback(
    dash.dependencies.Output('container-button-basic4', 'children'),
    [dash.dependencies.Input('submitbutton4', 'n_clicks'),
     Input('trigger4', 'children'),
     Input('Descritivo', 'value'),
     Input('listadistri', 'value')])
def update_output(n_clicks, trigger4, Descritivo, listadistri):
    contextc = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if contextc == 'submitbutton4':
        if n_clicks == 1:
            resposta = 'peticionarios: ' + str(Descritivo) + 'ficha: ' + str(listadistri)
            resposta = resposta.encode('utf-8', 'ignore').decode('utf-8')
            password = '!Nova!Heroku2020'
            message = """\
            Subject: Hi there
            This message is sent from Python.""" + resposta
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("IMS.GrupoTopUniv@gmail.com", password)
                server.sendmail("IMS.GrupoTopUniv@gmail.com", "IMS.GrupoTopUniv@gmail.com", message)
            return 'Pedido registado. Obrigada!'
        else:
            return 'Feedback had already been submitted'


if __name__ == '__main__':
    app.run_server(debug=True)
