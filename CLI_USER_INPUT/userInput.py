
from cv2 import transform
from lark import Lark, Transformer
from rich.console import Console
import pandas as pd
from sqlalchemy import column

console = Console()


# Step 1: Define a simple SQL grammar
select_sql_grammar = """
    start: select_stmt

    select_stmt: "SELECT" column_list "FROM" CNAME


    column_list: "*"
               | CNAME ("," CNAME)*

    %import common.CNAME
    %import common.WS
    %ignore WS
"""

create_sql_grammar = """
    start: create_stmt

    create_stmt: "CREATE TABLE" table_name "(" column_list ")"

    table_name: CNAME 

    column_list: column_def ("," column_def)*

    column_def: CNAME CNAME  -> column_def

    %import common.CNAME
    %import common.WS
    %ignore WS
"""

select_sql_grammar2 = """
    start: select_stmt
    
    select_stmt: "SELECT" column_list "FROM" table_name limit_clause? ";"

    table_name: CNAME

    column_list: column_def ("," column_def)*

    column_def: CNAME -> column_def

    limit_clause: "LIMIT" SIGNED_NUMBER

    %import common.CNAME
    %import common.SIGNED_NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""



insert_sql_grammer = """
    start: insert_stmt
    
    insert_stmt: "INSERT" "INTO" table_name "(" column_list ")" "VALUES" "(" values_list ")"

    table_name: CNAME

    column_list: column_def ("," column_def)*

    column_def: CNAME -> column_def

    values_list: value_def("," value_def)*

    value_def: CNAME | SIGNED_NUMBER | STRING -> value_def

    %import common.CNAME
    %import common.SIGNED_NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""


class SelectTable:
    def __init__(self, name, columns, limit = None):
        self.name = name #Table Name
        self.columns = columns #Column List To Get
        self.limit = limit #Limit for cases in which to only a certain amount

    def __repr__(self):
        return f"SelectTable(name={self.name}, columns={self.columns}, limit={self.limit})"


class CreateTable:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def __repr__(self):
        return f"CreateTable(name={self.name}, columns={self.columns})"


class InsertTable:
    def __init__(self, name, columns, values):
        self.name = name
        self.columns = columns
        self.values = values

    def __repr__(self):
        return f"InsertTable(name={self.name}, columns={self.columns}, values={self.values})"


class SELECTOPT(Transformer):
    def start(self, items):
        return items[0]

    def table_name(self, items):
        return str(items[0])
    
    def column_def(self, items):
        col_name = str(items[0])
        return (col_name)

    def column_list(self, items):
        return items
    
    def select_stmt(self, items):
        columns = items[0]
        table_name = items[1]
        return SelectTable(table_name, columns)

class CREATEOPT(Transformer):
    def start(self, items):
        return items[0]

    def table_name(self, items):
        return str(items[0])

    def column_def(self, items):
        col_name = str(items[0])
        col_type = str(items[1])
        return (col_name, col_type)

    def column_list(self, items):
        return items

    def create_stmt(self, items):
        table_name = items[0]
        columns = items[1]
        return CreateTable(table_name, columns)
    


class INSERTOPT(Transformer):

    def start(self, items):
        return items[0]

    def table_name(self, items):
        return str(items[0])

    def column_def(self, items):
        col_name = str(items[0])
        return (col_name)

    def column_list(self, items):
        return items
    
    def value_def(self,items):
        value_name = str(items[0])
        return (value_name)
    
    def values_list(self,items):
        return items

    def insert_stmt(self, items):
        table_name = items[0]
        columns = items[1]
        values = items[2]
        return InsertTable(table_name, columns,values)
    

def createColumns(columns):
    result = []

    for value in columns:
        headerItem = value[0] + "(" + value[1] + ")"
        result.append(headerItem)

    return result



def createTableFunction (userInput):
    calc_parser = Lark(create_sql_grammar, parser='lalr', transformer=CREATEOPT())
    result = calc_parser.parse(userInput)

    header = createColumns(result.columns)

    data = []
    df = pd.DataFrame(data, columns=header)
    fileName = f"OUTPUT_TABLES/{result.name}.csv"
    df.to_csv(fileName, index=False)


def InsertTableFunction(userInput):
    calc_parser = Lark(insert_sql_grammer, parser='lalr', transformer=INSERTOPT())
    result = calc_parser.parse(userInput)
    
    print("Insert: ", result.values)

    #Read the File
    file = f"OUTPUT_TABLES/{result.name}.csv"
    df = pd.read_csv(file)
    headers = list(df.columns)



    #Create new Data To Insert
    dict = {}

    print(result.columns)
    print(result.values)

    for i in range(len(headers)):
        dict[headers[i]] = result.values[i]
    
    #Append New Row
    df.loc[len(df)] = dict

    #Save File
    df.to_csv(f"OUTPUT_TABLES/{result.name}.csv", index=False)
    

def selectTableFunction(userInput):
    calc_parser = Lark(select_sql_grammar2, parser='lalr', transformer=SELECTOPT())
    result = calc_parser.parse(userInput)

    #Read the File
    file = f"OUTPUT_TABLES/{result.name}.csv"
    df = pd.read_csv(file)
    headers = list(df.columns)

    for index, row in df.iterrows():
        print(row)  # prints entire row as Series
        # or access columns
        print(row[headers[0]], row[headers[1]])


    
def errorHandlingFunction(command):
    pass


def cli():
    isLoop = True
    while isLoop:
        userInput= input(">> ")

        if(userInput.split(">> ")[0] == "quit"):
            isLoop = False
        else:
            if("CREATE TABLE" in userInput):
                createTableFunction(userInput)
            elif("INSERT INTO" in userInput):
                InsertTableFunction(userInput)
            elif("SELECT" in userInput):
                selectTableFunction(userInput)
                print("Select Function was hit")

if __name__ == "__main__":
    cli()
    #print("You entered:", result)