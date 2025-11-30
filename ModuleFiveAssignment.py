# DASH Framework for Jupyter
from jupyter_dash import JupyterDash
from dash import dcc, html
from dash.dependencies import Input, Output
JupyterDash.infer_jupyter_proxy_config()

# URL Lib to make sure that our input is 'sane'
import urllib.parse
import json

from CRUD_Python_Module import AnimalShelter

# Build App
app = JupyterDash(__name__)
app.layout = html.Div([
    # This element generates an HTML Heading with your name
    html.H1("Module 5 Asssignment - Dylan Harmon"),
    # This Input statement sets up an Input field for the username.
    dcc.Input(
            id="input_user".format("text"),
            type="text",
            placeholder="input type {}".format("text")),
    # This Input statement sets up an Input field for the password.
    # This designation masks the user input on the screen.
    dcc.Input(
            id="input_passwd".format("password"),
            type="password",
            placeholder="input type {}".format("password")),
    # Create a button labeled 'Submit'. When the button is pressed
    # the n_clicks value will increment by 1. 
    html.Button('Submit', id='submit-val', n_clicks=0),
    # Generate a horizontal line separating our input from our
    # output element
    html.Hr(),
    # This sets up the output element for the dashboard. The
    # purpose of the stlye option is to make sure that the 
    # output will function like a regular text area and accept
    # newline ('\n') characters as line-breaks.
    html.Div(id="query-out", style={'whiteSpace': 'pre-line'}),
    #TODO: insert unique identifier code here. Please Note: 
    # when you insert another HTML element here, you will need to 
    # add a comma to the previous line.
    html.H1("Dylan Harmon's Module Five Authentication")
    
])

# Define callback to update output-block
# NOTE: While the name of the callback function doesn't matter,
# the order of the parameters in the callback function are the
# same as the order of Input methods in the @app.callback
# For the callback function below, the callback is grabing the
# information from the input_user and input_password entries, and
# then the value of the submit button (has it been pressed?)
@app.callback(
    Output('query-out', 'children'),
    [Input('input_user', 'value'),
     Input('input_passwd', 'value'),
    Input(component_id='submit-val', component_property='n_clicks')]
)
def update_figure(inputUser,inputPass,n_clicks):
    # This is used as a trigger to make sure that the callback doesn't
    # try and connect to the database until after the submit button
    # is pressed. Otherwise, every time a character was added to the 
    # username or password field, an attempt would be made to connect to 
    # the daabase with an incorrect username and password.
    if n_clicks > 0:
        #Encode username and password
        username = urllib.parse.quote_plus(inputUser or "")
        password = urllib.parse.quote_plus(inputPass or "")
        
        #Instantiate CRUD Object
        crud = AnimalShelter(user=username, pwd=password)
        
        #Define Test Query
        query = {"color": 'Black Tabby'}
        
        #Example Query
        try:
            results = crud.ready(query)
        except Exception as e:
            return f"DB Error: {e}"
        
        
        if not results:
            return "Not found"
        
        # Make results readble
        formatted_results = []
        for i, doc in enumerate(results[:5], start=1):
            doc_str = json.dumps(doc, default=str)
            formatted_results.append(f"Result {i}: {doc_str}")
                
        return "\n\n".join(formatted_results)
        
        

        

# Run app and display result inline in the notebook, note, if you have previously run a prior app, the default port of 8050 may not be available, if so, try setting an alternate port.
app.run_server()