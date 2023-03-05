import base64
import datetime
import io
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, dash_table, dcc, html
import plotly_express as px
import plotly.graph_objects as go
 
 
###################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
app.config.suppress_callback_exceptions = True 



#########################################################################
# Layout

file_upload_layout = dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or nifty category ',
                                html.A('Select Files')
                            ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    )
file_upload_info_layout = html.Div(id='output-data-upload')
# file_upload_store = dcc.Store(id='store-data', storage_type='memory') # 'local' or 'session'
trend_header_layout =html.Div(
                        [
                            html.P("{}".format("Trend"),
                                    className="mb-1"),     
                        ],
                        className="d-flex w-100 justify-content-between ",
                        )
def indicator_layout(key,value,color): 
    indicator =  html.Div(
                    [
                    html.P("{}".format(key),
                            className="mb-1"),
                    html.Label("{}".format(value), 
                                className="text-{} bold".format(color[key])),
                    ],
                    className="d-flex w-100 justify-content-between ",
                    )
    return indicator 
def freq_indicator(key,value,color):
   
    indicator =  dbc.Col(
                        
                dbc.CardHeader( 
                                [
                                html.Label("{}".format(key),
                                        className=""),
                                html.Label("({})".format(value), 
                                        className="text-{} bold".format(color)),  
                                ], 
                            
                ),className="mb-2"
                    
            )
    return indicator 

def add_layout(indicator,result,color):
    l = list() 
    for i,v in result.items():
        l.append(indicator(i,v,color))
    return l  

##########################################################################################
app.layout = dbc.Container(
        [
            #row1
            dbc.Row(
                [
                    dbc.Row(
                        [
                             dbc.Col(
                                [
                                    file_upload_layout
                                ]
                            ),
                             dbc.Col(
                                    file_upload_info_layout,
                            )
                        ]
                    ),
                    dbc.Row(id ='category-board-name')
                ]
            ),
            #row2
            dbc.Row(
                [
                   # first of three
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(id='category-info'),
                                    dbc.CardBody(id='category-info-body')
                                ]
                                ,color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 4,  },
                    ),
                    # second of three
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("{} ".format("Trends")),
                                    dbc.CardBody(id='trends-info-body')   
                                ]
                                ,color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 4,  },
                        
                    ),
                    # three of three
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("{} ".format("Price Level")),
                                    dbc.CardBody(id='pricelevel-info-body')   
                                ],
                                color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 4,  }, 
                        
                    )
                ]
            ),
            #row 3
            dbc.Row(
                [
                dbc.Col([
                   dbc.Card(
                            [
                            
                            dbc.CardHeader("{} ".format("Table")),
                            dbc.CardBody( id = 'table-info'),  
                            ], 
                            color="dark", outline=True,className="mb-4") 
                    ], width={"size": 12,  },
                ),
                
                ]
            ),
            # row 4
            dbc.Row(
            [ 
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            
                            dbc.CardHeader([
                                    html.Label("{}".format("Price"), 
                                            className="bold"),
                                ]),
                            dbc.CardBody(
                                [ 
                                    #fig1
                                    dcc.Graph(id='line4-fig1', figure={}),
                                ]
                            ),
                            
                            ], 
                            color="dark", outline=True,className="mb-4") 
                
                    ],width={"size": 6, },
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            
                            dbc.CardHeader([
                                    html.Label("{}".format("Volume"), 
                                            className="bold"),
                                    
                                
                                ]),
                            dbc.CardBody(
                                [ 
                                     #fig2
                                    dcc.Graph(id='line4-fig2', figure={}), 
                                ]
                            ),
                            
                            ], 
                            color="dark", outline=True,className="mb-4") 
                
                    ],width={"size": 6, },
                ),
            ]
        ),
        # row 5 
       dbc.Row( 
            [ 
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            
                            dbc.CardHeader([
                                    html.Label("{}".format("selected stock Price"), 
                                            className="bold"),
                                ]),
                            dbc.CardBody(
                                [ 
                                    #fig3
                                    dcc.Graph(id='line5-fig1', figure={}), 
                                ]
                            ),
                            
                            ], 
                            color="dark", outline=True,className="mb-4") 
                        
                    ],width={"size": 6, },
                ),
                
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            
                            dbc.CardHeader([
                                    html.Label("{}".format("selected stock Volume"), 
                                            className="bold"),
                                    
                                ]),
                            dbc.CardBody(
                                [ 
                                    #fig3
                                    dcc.Graph(id='line5-fig2', figure={}), 
                                ]
                            ),
                            
                            ], 
                            color="dark", outline=True,className="mb-4") 
                
                    ],width={"size": 6, },
                )
                
                        
              
            ]
        ),    
            
        ],fluid=True 
)






######################################################################
labels=['0-100','101-200', '201-500','501-700','701-1K',
        '1K-1.5K','1.5K-2K','2K-3K','3K-5K','5K-7K',
        '7K-10K','10+K'] 
bins=[0,100, 200, 500,700,1000, 1500,2000,3000,5000,7000,10000,100000]
trend_value =['UP','DOWN']
day_trend = ['Advance','Decline','Unchanged']
text_color =['success','danger','primary']


def read_stratergy(df):
#   the convert dataframe  columns names 'SYMBOL \n' -> 'SYMBOL'
    df.columns = df.columns.str.replace('\n','').str.replace(' ','')
#   convert the columns value  into numeric
    columns_list = ['OPEN','HIGH','LOW','PREV.CLOSE', 'LTP',
                'VALUE', '52WH', '52WL', ]
    
    for col in columns_list:
        df[col] = pd.to_numeric(df[col].str.replace(",", ""), errors='coerce')
    df['PriceLevel'] = pd.cut(x=df['LTP'],bins=bins,labels=labels)
    
    # print(df) 
    
    return (df)

def change_column_types(df):
    
    # print(df.columns)
    # print(df.dtypes) 
    df['CHNG'] = pd.to_numeric(df["CHNG"], errors='coerce')
    df['%CHNG'] = pd.to_numeric(df["%CHNG"], errors='coerce')
    df['PriceLevel'] =pd.Categorical(df['PriceLevel'])
    # print(df.dtypes) 
    
    return df 

def advance_decline(df):
    advance = (df['CHNG'] > 0).sum() 
    decline = (df['CHNG'] < 0).sum()
    unchanged = (df['CHNG'] == 0).sum()  
    res = {k:v for k,v in zip(day_trend,list((advance,decline,unchanged)))}
    return res

def closer_to(low,current,high):
    value =""
    res1 = abs(current-high)
    res2 = abs(current-low)
    if res1 < res2 :
#         print("closer to higer")
        value = trend_value[0]
    else:
#         print("closer to lower")
        value=trend_value[1]
    return value

def add_trend_column(df):
    df['Trend'] = df.apply(lambda x: closer_to(x['52WL'],
                                                       x['LTP'],
                                                      x['52WH']), axis=1)
    return df

def trend_closer_to(df):
    res = df['Trend'].value_counts()[trend_value]
    
    # print(res)
     
    return res
def freq_counts(df): 
    present = df['PriceLevel'].unique().tolist()
    # print(type(present))
    l =[]
    for v in labels:
        if present.count(v)>0:
            l.append(v)
            
    
    freq_nif = df['PriceLevel'].value_counts()[l]
    
    # print(freq_nif) 
    
    return freq_nif
       
def add_and_modify(df):
    df = change_column_types(df)
    df.drop([0],inplace=True)
    df = add_trend_column(df)
    df['Trend'] =pd.Categorical(df['Trend'])
    # print(df.dtypes) 
    
    return df 
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    # print(decoded)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            # print(filename)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),skipinitialspace=' ')
            # print(df)
            df=read_stratergy(df)
            # print(df)
            dfjson = df.to_json(orient='split')
            return html.Div([
                html.H5(filename),
                html.H6(datetime.datetime.fromtimestamp(date)),
                dcc.Store(id='store-data',data = dfjson,storage_type='memory') # 'local' or 'session'

            ])         
        else:
            # Assume that the user uploaded an excel file 
            return html.Div([
            ' only csv  file.'
            ]),
    
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]),





    
    
   






############################################################################
#callbacks 
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'), 
              State('upload-data', 'last_modified'),
              prevent_initial_call = True)
def update_file_upload(list_of_contents, list_of_names, list_of_dates):
    # print(list_of_dates,list_of_names,list_of_contents)
    if list_of_contents is not None:
        
        a=parse_contents(list_of_contents,list_of_names,list_of_dates)
       
        # print(type(a),a)
        return(a)
     
@app.callback(
    Output('category-board-name','children'),
    Input('store-data','data'),  
    Input('upload-data', 'filename'), 
    prevent_initial_call = True 
)
def update_category_board(data,content): 
    # if listcontents is not None:
    dff = pd.read_json(data, orient='split')
    df =change_column_types(dff)
    category = df.iloc[0] 
    # print(category,"----")  
    res = dbc.Col(
            html.H1("{}".format(category['SYMBOL']),
                    className='text-center text-primary mb-4'),
                    width=12)
    
    return  res
    
@app.callback(
    Output("category-info","children"),
    Input('store-data','data'),
    Input('upload-data', 'filename'),
    prevent_initial_call = True
)
def update_category_info(data,content):
    dff = pd.read_json(data, orient='split')
    # print(dff) 
    df = change_column_types(dff)
    category = df.iloc[0]
    # print(category)
    res = html.Div(
        [
           
             html.Label("{}".format(category['SYMBOL']),
                    className="mb-1"),
          
        ],
        className="d-flex w-100 justify-content-between ",
        )
    return res
    
@app.callback(
    Output('category-info-body','children'),
    Input('store-data','data'),
    Input('upload-data', 'filename'),
    prevent_initial_call = True
)
def update_category_body(data,content):
    dff = pd.read_json(data, orient='split')
    df = change_column_types(dff)
    category = df.iloc[0]
    category_high_low = dict({'HIGH':category['HIGH'], 
                        'LOW':category['LOW'],
                        'OPEN':category['OPEN']})
    category52WHL = dict({'52WH':category['52WH'],
                    '52WL':category['52WL']})
    
    res = dbc.ListGroup(
        [ 
         
            dbc.ListGroupItem([
                html.Label( "{} ".format('LTP'), className=" bold"),
                html.Label( "{} ".format(category['LTP'],
                                        ), 
                            className="text-{} bold".format(text_color[1] if category['CHNG'] < 0 else text_color[0])),
                html.Label("{}".format(category['CHNG'],  
                                        ), 
                            className="text-{} bold".format(
                                text_color[1] if category['CHNG'] < 0 else text_color[0])),
                html.Label(" % {}".format( 
                                        category['%CHNG'], 
                                        ),  
                                className="text-{} bold".format(  
                                text_color[1] if category['%CHNG'] < 0 else text_color[0])),
            ],className="d-flex w-100 justify-content-between "),
             
            dbc.ListGroupItem(add_layout(
                                indicator_layout,
                                category_high_low,
                                color = { k:v for (k,v) in zip(category_high_low.keys(), text_color)},
                                )
                                ),
            dbc.ListGroupItem(add_layout(
                                indicator_layout,
                                category52WHL,
                                color = { k:v for (k,v) in zip(category52WHL.keys(), text_color)},
                                )), 
        ], 
        
        )
    return res 
 
@app.callback(
    Output('trends-info-body','children'),
    Input('store-data','data'),
    Input('upload-data', 'filename'),
    prevent_initial_call = True
)
def update_trend_layout(data,contents):
    dff = pd.read_json(data, orient='split')
    df = add_and_modify(dff)
    trend_res = trend_closer_to(df)
    ad_result = advance_decline(df)
    
    trend52WHLStocks =dict({'Stocks-closer-52WH':trend_res[0],
                        'Stocks-closer-52WL':trend_res[1]}) 
    
    
    res = dbc.ListGroup(
    [ 
        
        dbc.ListGroupItem(add_layout(
                            indicator_layout,
                            ad_result,
                            color = { k:v for (k,v) in zip(ad_result.keys(), text_color)}),
                            
                            ), 
        dbc.ListGroupItem(add_layout(
                            indicator_layout,
                        trend52WHLStocks ,
                        color = { k:v for (k,v) in zip(trend52WHLStocks.keys(), text_color)},
                                )),    
    ],
    
    )       
    return res

@app.callback(
    Output('pricelevel-info-body','children'),
    Input('store-data','data'),
    Input('upload-data', 'filename'), 
    prevent_initial_call = True
)
def update_pricelevel_layout(data,contents):
    dff = pd.read_json(data, orient='split')
    df = add_and_modify(dff) 
    
    priecefreq = freq_counts(df)
    
    
    res = dbc.Row( 
                  add_layout(freq_indicator,priecefreq,color=text_color[2]) 
                    )
    return res 

 
@app.callback(
    Output("table-info",'children'),
    Input('store-data', 'data'),
    Input('upload-data','filename'),
    prevent_initial_call = True
)
def update_table(data,content):
        
    dff = pd.read_json(data, orient='split')
    
    dff = pd.read_json(data, orient='split')
    df = add_and_modify(dff) 
   
        
    res = dash_table.DataTable(
                                id='datatable-interactivity',
                              columns=[
                                       {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}
                                       for i in df.columns 
                                   ], 
                             data=df.to_dict('records'),  # the contents of the table
                                editable=False,              # allow editing of data inside all cells
                                filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                                sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                                sort_mode="single",         # sort across 'multi' or 'single' columns
                                column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                                row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                                # row_deletable=True,         # choose if user can delete a row (True) or not (False)
                                selected_columns=[],        # ids of columns that user selects
                                selected_rows=[],           # indices of rows that user selects
                                page_action="native",       # all data is passed to the table up-front or not ('none')
                                page_current=0,             # page number that user is on
                                page_size=15,                 # number of rows visible per page
                                fixed_rows={'headers': True},
                                style_table={'height': '450px', 'overflowY': 'auto'}, 
                                style_cell={                # ensure adequate header width when text is shorter than cell's text
                                    'minWidth': 150, 'maxWidth': 150, 'width': 150
                                },

                                style_data={                # overflow cells' content into multiple lines
                                    'whiteSpace': 'normal',
                                    'height': 'auto'
                                },
                                
                                style_cell_conditional=[            # style_cell_c. refers to the whole table
                                    {
                                        'if': {'column_id': c},
                                        'textAlign': 'left'
                                    } for c in ['SYMBOL',]
                                    
                                ], 
                                style_data_conditional=[        # style_data.c refers only to data rows
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    },
                                    {
                                            'if': {
                                                'column_id': '%CHNG',
                                                'filter_query': '{%CHNG} < 0'
                                            },
                                            # 'backgroundColor': '#3D9970',
                                            'color': 'red',
                                    },
                                    {
                                            'if': {
                                                'column_id': 'CHNG',
                                                'filter_query': '{CHNG} < 0'
                                            },
                                            # 'backgroundColor': '#3D9970',
                                            'color': 'red',
                                    },
                                ], 

                                
                            )
    
    return(res)


@app.callback(
    Output(component_id='line4-fig1', component_property='figure'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells'),
    
    
    # Input('store-data', 'data'),
    # Input('upload-data','filename'),
     ], 
    
    prevent_initial_call = True 
)
def update_fig1(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell,
               #data,content
               ):
    # print('***************************************************************************')
    # print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    # print('---------------------------------------------')
    # print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    # print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    # print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    # print('---------------------------------------------')
    # print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    # print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    # print("---------------------------------------------")
    # print("Complete data of active cell: {}".format(actv_cell))
    # print("Complete data of all selected cells: {}".format(slctd_cell))
    
    dff = pd.DataFrame(all_rows_data)

    fig ={}
    if "SYMBOL" in dff and "LTP" in dff:
        fig = px.line(
                          data_frame=dff,
                          x="SYMBOL",
                          y='LTP',
                          color="PriceLevel", symbol="PriceLevel",
                          category_orders={"PriceLevel":labels},
                          color_discrete_sequence=px.colors.sequential.Rainbow_r,
                          title="Count {}".format(len(dff))
                      
                      )
    return fig

@app.callback(
    Output(component_id='line4-fig2', component_property='figure'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells'),
     
    #  Input('store-data', 'data'),
    #  Input('upload-data','filename'),
     ],
    
    prevent_initial_call = True
    
)
def update_fig2(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell,
            #    data,content
               ):
    # print('***************************************************************************')
    # print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    # print('---------------------------------------------')
    # print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    # print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    # print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    # print('---------------------------------------------')
    # print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    # print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    # print("---------------------------------------------")
    # print("Complete data of active cell: {}".format(actv_cell))
    # print("Complete data of all selected cells: {}".format(slctd_cell))
    
    dff = pd.DataFrame(all_rows_data)

    fig ={}
    if "SYMBOL" in dff and "VOLUME(shares)" in dff:
        fig = px.line(
                          data_frame=dff,
                          x="SYMBOL",
                          y='VOLUME(shares)',
                          color="PriceLevel", symbol="PriceLevel",
                          category_orders={"PriceLevel":labels},
                          color_discrete_sequence=px.colors.sequential.Rainbow_r,
                        #   labels={"did online course": "% of Pop took online course"}
                         title="Count {}".format(len(dff))
                      )
    return fig


@app.callback(
    Output(component_id='line5-fig1', component_property='figure'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells'),
    #  Input('store-data', 'data'),
    #  Input('upload-data','filename'),
    ],
    
   
)
def update_fig3(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell,
            #    data,content
               ):
    # print('***************************************************************************')
    # print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    # print('---------------------------------------------')
    # print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    # print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    # print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    # print('---------------------------------------------')
    # print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices)) 
    # print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    # print("---------------------------------------------")
    # print("Complete data of active cell: {}".format(actv_cell))
    # print("Complete data of all selected cells: {}".format(slctd_cell))
    
    dff = pd.DataFrame(all_rows_data)
    # print("-------",dff)
    # print(slctd_row_indices,slct_rows_names,slctd_rows,order_of_rows_indices)
    # print("&&&&&&",dff.iloc[slctd_row_indices]) 
    
    fig ={} 
    if  (slctd_row_indices) !=None:
        df_selected_rows = dff.iloc[slctd_row_indices]
        if (("SYMBOL" in dff) and ("LTP" in dff ) and  ("HIGH" in dff ) 
            and ("OPEN" in dff) and ("LOW" in dff)  ):  
            fig = go.Figure()
        
            
            fig.add_trace(
                        go.Bar(
                        
                            x=df_selected_rows["SYMBOL"],
                            y=df_selected_rows['LTP'],
                            name ='LTP',
                            
                        )
                        ) 
            
            fig.add_trace(
                go.Scatter(
                
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['52WH'],  
                    name="52WH",
                    mode="markers",
                    marker=dict(color="Green", size=8,symbol=[5]), 
                )
            )
            
            
            
            fig.add_trace(
                go.Scatter(
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['HIGH'],  
                    name="HIGH",
                    mode="markers",
                    marker=dict(color="darkgreen", size=8,symbol=[19]),
                )
            )
            fig.add_trace(
                go.Scatter(
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['OPEN'],  
                    name="OPEN",
                    mode="markers",
                    marker=dict(color="orange", size=8,symbol=[24]),
                )
            )
            fig.add_trace(
                go.Scatter(
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['LOW'],  
                    name="LOW",
                    mode="markers",
                    marker=dict(color="Red", size=8,symbol=[20]),
                )
            )
            fig.add_trace(
                go.Scatter(
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['52WL'],  
                    name="52WL",
                    mode="markers",
                    marker=dict(color="Red", size=8,symbol=[6]),
                )
            )
            fig.update_layout(
                            {"title": "Count {}".format(len(slctd_row_indices))
                            })
                            
    return fig

@app.callback(
    Output(component_id='line5-fig2', component_property='figure'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells'),
    #  Input('store-data', 'data'),
    #  Input('upload-data','filename'),
     ],
    
    
    prevent_initial_call = True,
     
    
)
def update_fig4(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows, 
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell,
            #    data,contents
               ):
    # print('***************************************************************************')
    # print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    # print('---------------------------------------------')
    # print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    # print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    # print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    # print('---------------------------------------------')
    # print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    # print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    # print("---------------------------------------------")
    # print("Complete data of active cell: {}".format(actv_cell))
    # print("Complete data of all selected cells: {}".format(slctd_cell))
    # print(data)
    
    dff = pd.DataFrame(all_rows_data)
    # print(slctd_rows,slctd_row_indices)
    # print(dff.iloc[slctd_row_indices])
    fig ={} 
    if  (slctd_row_indices) !=None:
        df_selected_rows = dff.iloc[slctd_row_indices]
        
        if (("SYMBOL" in dff)  and("VOLUME(shares)" in dff) ): 
            fig = go.Figure() 
            
            
            fig.add_trace(
                    go.Pie(
                        
                        labels=df_selected_rows['SYMBOL'],
                        values=df_selected_rows['VOLUME(shares)'],
                        
                        hole=.3,
                    
                    )
                ) 
            fig.update_layout(
                            {"title": "Count {}".format(len(slctd_row_indices))
                            })
        
    return fig

    
##############################################################################


if __name__ == '__main__':
    app.run_server(debug=False,port=8050)  
