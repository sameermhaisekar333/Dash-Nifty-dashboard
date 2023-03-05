import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, dash_table, dcc, html 
import plotly_express as px
import os  

##################################################################



bhavavfile_path = './nifty-dataset/bhavadataset/'
nifty_category_file_path = './nifty-dataset/niftycategory/'

file_bhava_location = lambda x:bhavavfile_path + x
file_nifty_location = lambda x:nifty_category_file_path+ x
name = lambda b:( "-".join(b[1:len(b)-3]))
file_category_name_split = lambda x:x.split("-")

p1 =os.listdir(bhavavfile_path)
n1 =os.listdir(nifty_category_file_path)

category_names = list(map(name,map(lambda x:x.split("-"),n1)))


bhava_copy_file = file_bhava_location(p1[0])
nifty_files= list(map(file_nifty_location,n1))


dict_niftycategory_location = {k: v for k, v in zip(category_names, nifty_files)}
# print(dict_category_location)
##########################################################################
class Stratgery():
    def __init__(self):
        self.stlist =[]
    def addtostlist(self,value):
        self.stlist.append(value)
        
def readbhavadatafile(filepath,series):
    """
     read the file consisting of all the listed entities in NSE
    """
    df = pd.read_csv(filepath,parse_dates=['DATE1'],skipinitialspace=' ')
    # consider only EQ for Series
    df_all = df.loc[df['SERIES'].isin(series)]
    # print(df_all)
    

    index=[a for a in range(len(df_all['SYMBOL'].tolist()))]
    
    #create a new dataframe for only EQ series and column as NSE
    
    nse_all = pd.DataFrame(data=df_all['SYMBOL'].values,index=index,columns=['NSE'])
    return (nse_all,df_all)

def readnifitystrategyfile(filepath):
    """
     to read the indiviual file of different nifty stratery 
     and return a dataframe
    """
    df = pd.read_csv(filepath,skipinitialspace=' ')
    
    # the convert dataframe  columns names 'SYMBOL \n' -> 'SYMBOL'
    df.columns = df.columns.str.replace('\n','').str.replace(' ','')
    
    return(df)

def newcolumnforstrategy(nse_all,newstrategy,sc):
    stratgery= newstrategy[newstrategy.columns[0]].tolist()
    sc.addtostlist(stratgery[0])
    newstrategy.drop(0,inplace=True)   # drop first data row (as first row is nifity50(catgeroy value))
   
    new_values = stratgery[1:]
    
    column_name = stratgery[0] 
    #print(column_name,"->>>>",len(new_values))
    
    nse_all[column_name]=nse_all['NSE'].isin(new_values)

def count_for_category(df,category):
    res = df[category].value_counts()[[0,1]]
    #print("count",res[1]) 
    return res[1]
########################################################################


nse_all,bhav_all = readbhavadatafile(bhava_copy_file,series=['EQ','BE'])
sc = Stratgery()


# print(nifty_files) 
stratgery_files = nifty_files

for file in stratgery_files:
    df = pd.DataFrame()
    # print(df)
    df = readnifitystrategyfile(file)
    newcolumnforstrategy(nse_all,df,sc)

# print(nse_all)
nse_all= nse_all.replace({False: 0, True: 1})
# print(nse_all)
countsum = nse_all.drop(['NSE'],axis=1).apply("sum",axis=1)
nse_all['Count'] = countsum
# print(nse_all)
df_table = nse_all 

category_count = {nse_all.columns[0]:len(nse_all['NSE'])}
#print(nse_all.columns[1:-1])
for col in nse_all.columns[1:-1]:
    category_count.update({col :count_for_category(nse_all,col)})

# print(category_count)       


#####################################################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
app.config.suppress_callback_exceptions = True 

#######################################################################
#Layout
text_color =['success','danger','primary']
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




file_stragery = dbc.Row( 
                  add_layout(freq_indicator,category_count,color=text_color[2]) 
                    )
data_table = dash_table.DataTable(
                                id='datatable-interactivity',
                              columns=[
                                       {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}
                                       for i in df_table.columns 
                                   ], 
                             data=df_table.to_dict('records'),  # the contents of the table
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
                                page_size=15,                  # number of rows visible per page
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
                                ], 
                                style_data_conditional=[        # style_data.c refers only to data rows
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    },
                                    
                                    
                                ],  
                            )

#######################################################################
app.layout = dbc.Container(
    [   
        #row1
        dbc.Row([
        	 html.H1("Nifty" ,className="text-primary text-center bold mb-4")
        	 ],
        	 ), 
        #row2
            dbc.Row(
                [
                   # first of three
                    dbc.Col(
                        [
                            dbc.Card( 
                                [
                                    dbc.CardHeader("Category ",id='files-info'),
                                    dbc.CardBody([file_stragery],id='files-info-body',)
                                ]
                                ,color="dark", outline=True ,className="mb-4"
                            )
                        ],width={"size": 12,  },
                    ),
                    

                ]
            ),
            dbc.Row([data_table],id='table-info',className="mb-4"),
            # row 4
            dbc.Row(
            [ 
                dbc.Col(
                    [
                        dbc.Card(
                            [
                            
                            dbc.CardHeader([
                                    html.Label("{}".format("STOCKS"), 
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
                
                    ],width={"size": 12, },
                ),
            
            ] 
            ),
           
    ]
    ,fluid=True 
)





############################################################################


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
    
    df = pd.DataFrame(all_rows_data) 
    n_colors = len(df.columns)-2
    #print((n_colors))  
    #colors = px.colors.sample_colorscale("viridis", [n/(n_colors -1) for n in range(n_colors)])
    dff=df.set_index("NSE")
    dff.drop(['Count'],axis=1,inplace=True)
    # print(dff)

    fig ={}
    if  len(dff.columns)>0 :
        
                    
            fig = px.bar(
                data_frame=dff,
                        barmode="stack",
                        #template="plotly_dark", 
                        color_discrete_sequence= px.colors.sequential.Rainbow_r,
                        title="Count {}".format(len(dff) )
                    )
            
    return fig



#########################################################################
if __name__ == '__main__':
    app.run_server(debug=False,port=8052)
