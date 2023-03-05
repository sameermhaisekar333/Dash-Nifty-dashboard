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
                                'Drag and Drop or  sec_bhavdata_full_',
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
                                    dbc.CardHeader("{} ".format("Trends")),
                                    dbc.CardBody(id='trends-info-body')
                                ]
                                ,color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 4,  },
                    ),
                    # second of three
                   
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
                        ],width={"size": 8,  },  
                        
                    )
                ]
            ),
            dbc.Row(
                [
                     dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("{} ".format("Series ")),
                                    dbc.CardBody(id='serieslevel-info-body')   
                                ]
                                ,color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 12,  },
                        
                    ),
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

day_trend = ['Advance','Decline','Unchanged']
text_color =['success','danger','primary']


def read_stratergy(df):

    columns_list = ['DELIV_QTY','DELIV_PER']
    
    for col in columns_list:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['PriceLevel'] = pd.cut(x=df['CLOSE_PRICE'],bins=bins,labels=labels)
    df['SERIES']= pd.Categorical(df['SERIES'])
    
    # print(df) 
    
    return (df)

def change_column_types(df):
    

    df['PriceLevel'] =pd.Categorical(df['PriceLevel'])
    df['SERIES'] =pd.Categorical(df['SERIES'])
    df['DATE1'] = pd.to_datetime(df['DATE1'], errors='coerce').dt.strftime('%d-%m-%Y')
    # df['DATE1'] = df['DATE1'].dt.strftime('%d-%m-%Y') 
  
                                   
    # print("-------",df.dtypes)  
    
    return df 

def advance_decline(df):
    advance = (df['CLOSE_PRICE'] > df['OPEN_PRICE']).sum() 
    decline = (df['CLOSE_PRICE'] < df['OPEN_PRICE']).sum()
    unchanged = (df['CLOSE_PRICE'] == df['OPEN_PRICE']).sum()  
    res = {k:v for k,v in zip(day_trend,list((advance,decline,unchanged)))}
    return res 



def series_freq(df):
    series_resut = df['SERIES'].value_counts()
    return series_resut

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
    
    return df 

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    # print(decoded)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            # print(filename)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),skipinitialspace=' ',parse_dates=['DATE1'])
            # print(df)
            df=read_stratergy(df)
            # print(df)
            # print(df.dtypes)
            dfjson = df.to_json(orient='split',date_format='iso')#date_format='iso', )
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
    # Input('store-data','data'),  
    Input('upload-data', 'filename'), 
    prevent_initial_call = True 
)
def update_category_board(content): 
   
    res = dbc.Col(
            html.H1("{}".format(content),
                    className='text-center text-primary mb-4'),
                    width=12)
    
    return  res
    
@app.callback(
    Output('trends-info-body','children'),
    Input('store-data','data'),
    Input('upload-data', 'filename'),
    prevent_initial_call = True
)
def update_trend_layout(data,contents):
    dff = pd.read_json(data, orient='split')
    
    df = add_and_modify(dff)
    # print(dff.dtypes)
    
    ad_result = advance_decline(df)
    
   
    
    
    res = dbc.ListGroup(
    [ 
        
        dbc.ListGroupItem(add_layout(
                            indicator_layout,
                            ad_result,
                            color = { k:v for (k,v) in zip(ad_result.keys(), text_color)}),
                            
                            ), 
         
    ],
    
    )       
    return res

@app.callback(
    Output('serieslevel-info-body','children'),
    Input('store-data','data'),
    Input('upload-data', 'filename'), 
    prevent_initial_call = True
)
def update_serieslevel_layout(data,contents):
    dff = pd.read_json(data, orient='split')
    df = add_and_modify(dff) 
    
    series = series_freq(df)
    
    
    res = dbc.Row( 
                  add_layout(freq_indicator,series,color=text_color[2]) 
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
        
    dff = pd.read_json(data, orient='split',)
    
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
                                                'column_id': '%SERIES',
                                                'filter_query': '{%SERIES} = EQ'
                                            },
                                            'backgroundColor': '#3D9970',
                                            # 'color': 'red', 
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
    if "SYMBOL" in dff and "CLOSE_PRICE" in dff: 
        fig = px.line(
                          data_frame=dff,
                          x="SYMBOL",
                          y='CLOSE_PRICE', 
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
    if "SYMBOL" in dff and "TTL_TRD_QNTY" in dff:
        fig = px.line(
                          data_frame=dff,
                          x="SYMBOL",
                          y='TTL_TRD_QNTY',
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
        if (("SYMBOL" in dff) and ("CLOSE_PRICE" in dff )  ):  
            fig = go.Figure()
        
            
            fig.add_trace(
                        go.Bar(
                            name ='CLOSE_PRICE',
                            x=df_selected_rows["SYMBOL"],
                            y=df_selected_rows['CLOSE_PRICE'],
                            
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
        
        if (("SYMBOL" in dff)  and("TTL_TRD_QNTY" in dff)  and("DELIV_QTY" in dff) ): 
            fig = go.Figure() 
    
            fig.add_trace(
                go.Scatter(
                   
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['TTL_TRD_QNTY'],  
                    name="Total traded Quantity",
                    mode="markers",
                    marker=dict(color="Green", size=8,symbol=[5]),
                )
            )
            fig.add_trace(
                go.Scatter(
                    
                    x=df_selected_rows['SYMBOL'],
                    y=df_selected_rows['DELIV_QTY'],  
                    name="Delivery Quantity",
                    mode="markers",
                    marker=dict(color="blue", size=8,symbol=[5]), 
                )
            )


            
            
            fig.update_layout(
                            {"title": "Count {}".format(len(slctd_row_indices))
                            })
        
    return fig

    
##############################################################################


if __name__ == '__main__':
    app.run_server(debug=False,port=8051) 
