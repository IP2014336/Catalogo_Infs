import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
import smtplib
import ssl

port = 465  # For SSL
# Create a secure SSL context
context = ssl.create_default_context()

#######################################
# Inicio do Indice
# 1 > Recupera Imagem homepage

# Fim do Indice
#######################################

# 1 > Recupera Imagem homepage
response = requests.get('https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/library-1082309_1280.jpg')
img = Image.open(BytesIO(response.content))
response2 = requests.get('https://raw.githubusercontent.com/IP2014336/Catalogo_Infs/master/mapfre_logo_printscreen.jpg')
logo = Image.open(BytesIO(response2.content))

# 2 > Recupera dados
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

Letter_options = [
    dict(label=Letra, value=Letra)
    for Letra in dic['Letra'].unique()]

estados = ['EM PRODUÇÃO', 'DESCONTINUADO', 'EM DESENVOLVIMENTO']
estado_options = [dict(label=estado, value=estado) for estado in estados]

YesNo = ['Sim', 'Não']
YesNo_options = [dict(label=simnao, value=simnao) for simnao in YesNo]

tipos = ['Dataset', 'Informações', 'Todos']
tipo_options = [dict(label=tipo, value=tipo) for tipo in tipos]

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
    value='Maria Lainez'
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
radio_yn = dcc.RadioItems(
    id='radio_yn',
    options=YesNo_options,
    value='Sim'
)
DicQuesttypes = ['Nova definição', 'Alteração de definição atual']
DicQuesttype_options = [dict(label=DicQuesttype, value=DicQuesttype) for DicQuesttype in DicQuesttypes]
RadioDicQuesttype=dcc.RadioItems(id='RadioDicQuesttype', options=DicQuesttype_options)

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
        dcc.Tab(label='Catálogo',   value='tab-3', style={'line-height': tab_height, 'padding': '0'}),
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
            html.H1('Ajude-nos a melhorar!', style={'color': colors['redtext'], 'text-shadow': '2px 0px black'}),
            # 7.6.2 > Perguntas
            html.Div([
                html.Div([html.Br()], style={'width': '5%', 'height': '20px'}),
                html.Div([html.P("Conseguiu encontrar o que procurava?")], style={'width': '35%', 'height': '20px'}),
                html.Div([html.Br()], style={'width': '3%', 'height': '20px'}),
                html.Div([html.H3(children='Formato'), radio_yn], style=radio_style)
            ], style={'display': 'flex'}),
            html.Div([
                html.Div([html.Br()], style={'width': '5%'}),
                html.Div([html.P("Deixe-nos o seu comentário")], style={'width': '35%'}),
                html.Div([html.Br()], style={'width': '3%'}),
                # 7.6.3 > Caixa de comentario
                html.Div([
                    dcc.Textarea(
                        id='comentario',
                        value='escreva aqui',
                        style={'width': 550, 'height': 50, 'font-style': 'italic', 'backgroundColor': '#e6e6e6'},
                    )])
            ], style={'display': 'flex'}),
            html.Div([html.Br()], style={'height': '15px'}),
            html.Div([
                # 7.6.4 > Botão de submissao
                html.Div([html.Br()], style={'width': '36%'}),
                html.Div([html.Button(' Submit ', id='submitbutton5', n_clicks=0, style={})]),
                html.Div(id='trigger5', children=0, style=dict(display='none')),
                html.Div([html.Br()], style={'width': '1%'}),
                html.Div(id='container-button-basic5',
                         style={'font-style': 'italic', 'font-size': '12px', 'marginTop': '5px'})
            ], style={'display': 'flex'})
        ])
    elif tab == 'tab-7':
        return \
            html.Div([
                html.H1('Área Reservada a Data Steward(ess)!', style={'color': colors['redtext']}),
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
                    html.Div([html.Br()], style={'height': '55px'}),
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

# 11 > Define 4 scatter plots de indicadores vs score
# 11.1 > Constroi 1º gráfico
corr1 = px.bar(data_frame=logs,  x=logs['Estado'], orientation='v', barmode='stack',
               title='<b>Nº Pedidos </b> por <b>Estado', height=400, width=400, opacity=0.8,
               color_discrete_sequence=px.colors.sequential.Viridis_r)
corr1.update_layout(margin=dict(l=0, r=0, t=60, b=10, pad=0),
                    title={'y': 0.97, 'x': 0.55, 'xanchor': 'center', 'yanchor': 'top'},
                    yaxis=dict(showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    xaxis=dict(title_text="Nº Pedidos", showgrid=False, zeroline=False, titlefont=dict(size=12)),
                    titlefont=dict(size=13), showlegend=True,
                    legend_orientation="h", legend_title_text='')

@app.callback(Output('submitbutton', 'style'), [Input('submitbutton', 'n_clicks')])
def change_button_style(n_clicks):
    if n_clicks > 0:
        return grey_button_style
    else:
        return red_button_style
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
@app.callback(
    dash.dependencies.Output('container-button-basic5', 'children'),
    [dash.dependencies.Input('submitbutton5', 'n_clicks'),
     Input('trigger5', 'children'),
     Input('radio_yn', 'value'),
     Input('comentario', 'value')])
def update_output(n_clicks, trigger5, radio_yn, comentario):
    contextc = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if contextc == 'submitbutton5':
        if n_clicks == 1:
            resposta = 'peticionarios: ' + str(radio_yn) + 'ficha: ' + 'porquÊ: ' + str(comentario)
            resposta = resposta.encode('utf-8', 'ignore').decode('utf-8')
            password = '!Nova!Heroku2020'
            message = """\
            Subject: Hi there
            This message is sent from Python.""" + resposta
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("IMS.GrupoTopUniv@gmail.com", password)
                server.sendmail("IMS.GrupoTopUniv@gmail.com", "IMS.GrupoTopUniv@gmail.com", message)
            return 'Obrigada!'
        else:
            return 'Feedback had already been submitted'
        
        
if __name__ == '__main__':
    app.run_server(debug=True)
