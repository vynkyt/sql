import re 
import copy
"""
    result = []
    and_or = ""

    if string[i:i+3] == "AND":
        and_or = "AND"
    elif string[i:i+2] =="OR":
        and_or = "OR"
    
    condition_parts = condition.split(" ")
    
    check shape of where clause here (new method/function)
    
    0. split on " "
    1. parse splitted condition from left to right:
        2. Find a condition. SOmething that has the shape (condition_column, operator, value)
            apply check()
            temp = Filter the condition using filter()
            If an AND/OR clause was seen before:
                result = temp AND/OR result
            else:
                result = temp
        3. Find AND / OR. 
            If found, prev = AND/OR
"""
class Condition:
    def __init__(self, operand: str, operator: str, value: str):
        self.operand = operand
        self.operator = operator
        self.value = value
    
    def get_operand(self) -> str:
        return self.operand
    
    def get_operator(self) -> str:
        return self.operator
    
    def get_value(self) -> str:
        return self.value

def getTable(table_name) -> list[list[str]]:
    table = []
    with open(f"{table_name}.db", 'r') as file:
        db = file.read()
        rows = db.split("\n")
        for i in range(len(rows)):
            columns = rows[i].split(", ")
            table.append(columns)
    return table

#[['Name', 'Age', 'CanDrive'], ['str', 'int', 'bool']]
def check(col: str, operator: str, value, metadata: list[list[str]]) -> list[str]:
    error_messages = []

    if col not in metadata[0]:
        error_messages.append(f"{col} does not exist. Existing columns: {metadata[0]}")
    if operator not in ["<", ">", "<=", ">=", "=", "!="]:
        error_messages.append(f"{operator} is not an operator")

    if col in metadata[0]:
        if metadata[1][metadata[0].index(col)] == "str":
            try:
                str(value)
                
            except ValueError:
            # if not isinstance(value, str):
                error_messages.append(f"{value} should be of type string")
            if operator not in ["=", "!="]:
                error_messages.append("Invalid operator for string")
        elif metadata[1][metadata[0].index(col)] == "int":
            try:
                int(value)
                
            except ValueError:
            # if not isinstance(value, int):
                error_messages.append(f"{value} should be of type integer")
        elif metadata[1][metadata[0].index(col)] == "bool":
            try:
                bool(value)
             
            except ValueError:
            # if not isinstance(value, bool):
                error_messages.append(f"{value} should be of type boolean")
    
    return error_messages

def preprocess(condition_parts: list[str], metadata: list[list[str]]) -> list[list[Condition], list[str]]:
    good_conditions = []
    and_or = [""]
    if len(condition_parts) % 2 != 0:
        i = 0
        while i < len(condition_parts):
            has_or_and = False
            if i+2 > len(condition_parts):
                return [[],["No three parts"]]
            error = check(condition_parts[i], condition_parts[i+1], condition_parts[i+2], metadata)
            if len(error) == 0:
                if i+3 < len(condition_parts):
                    if condition_parts[i+3] != "AND" and condition_parts[i+3] != "OR":
                        return [[],["There's no condition."]]
                    else:
                        and_or.append(condition_parts[i+3])
                        has_or_and = True
                else:
                    has_or_and = False
            else:
                return error
            good_conditions.append(Condition(condition_parts[i], condition_parts[i+1], condition_parts[i+2]))
            i += 3
            if has_or_and:
                i += 1
    else:
        return [[],["Length even"]]
    return [good_conditions, and_or]

def check2(values: list[str], metadata: list[list[str]]):
    error_messages = []
    for i in range(len(values) - 1):
        if metadata[1][i] == "str":
            try:
                str(values[i])
                
            except ValueError:
            # if not isinstance(value, str):
                error_messages.append(f"{values[i]} should be of type string")
        elif metadata[1][i] == "int":
            try:
                int(values[i])
                
            except ValueError:
            # if not isinstance(value, int):
                error_messages.append(f"{values[i]} should be of type integer")
        elif metadata[1][i] == "bool":
            try:
                bool(values[i])
            
            except ValueError:
            # if not isinstance(value, bool):
                error_messages.append(f"{values[i]} should be of type boolean")

    return error_messages
        
        

db = getTable("student")
metadata = db[:2]
# print(preprocess(["age", ">"], metadata))
# print(preprocess(["age", ">", "3", "gender"], metadata))
# print(preprocess(["age", ">", "3", "OR", "OR"], metadata))
# print(preprocess(["age", ">", "three"], metadata))
# print(preprocess(["hello", "bye", "3"], metadata))
# print(preprocess(["age", ">", "3", "gender", "OR"], metadata))
# print(preprocess(["3", "3", "3"], metadata))
# print(preprocess(["Age", ">", "3"], metadata))
# processed_condtions = preprocess(["Age", ">", "3", "AND", "Age", "<", "8"], metadata)
# conditions = processed_condtions[0]
# connectors = processed_condtions[1]
# print(conditions[0].get_operand())
# print(conditions[0].get_operator())
# print(conditions[0].get_value())
# print(connectors)

def filter(col, operator, value, metadata, table) -> list[list[str]]:
    column_index = metadata[0].index(col)
    rows = []
    for i in range(len(table)):
        match operator:
            case "<":
                if table[i][column_index] < value:
                    rows.append(table[i])
            case ">":
                if table[i][column_index] > value:
                    rows.append(table[i])
            case "<=":
                if table[i][column_index] <= value:
                    rows.append(table[i])
            case ">=":
                if table[i][column_index] >= value:
                    rows.append(table[i])
            case "=":
                if table[i][column_index] == value:
                    rows.append(table[i])
            case "!=":
                if table[i][column_index] != value:
                    rows.append(table[i])
    return rows

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def intersection(one, two) -> list[list[str]]: 
    results = []
    for i in range(len(one)):
        for j in range(len(two)):
           if one[i] == two[j]:
               results.append(one[i])
    return results

def union(one, two) -> list[list[str]]: 
    results = {}
    for row in one:
        if row: 
            results[tuple(row)] = None
    for row in two:
        if row:
            results[tuple(row)] = None
    return [list(row) for row in results.keys()]

# print(filter("Age", "=", "13", [['Name', 'Age', 'CanDrive'], ['str', 'int', 'bool']],[['John', '13', 'False'], ['Mary', '18', 'True'], ['Bob', '16', 'False']] ))

def select(query:str) -> list[list[str]]:
    after_select = query.split("SELECT ")
    column, after_from = after_select[1].split(" FROM ")
    table_name = str()
    condition_column, operator, value = "", "", ""
    if "WHERE" in after_from:
        table_name, condition = after_from.split(" WHERE ")
        # condition_column, operator, value = condition.split(" ")
    else: 
        table_name = after_from

    query_columns = column.split(", ")

    db = getTable(table_name)
    metadata = db[:2]
    table = db[2:]
    metadata_columns = metadata[0]

    result = [] 
    
    condition_parts = condition.split(" ")

    processed_conditions = preprocess(condition_parts, metadata)
    if len(processed_conditions[0]) == 0:
        print(processed_conditions[1])
        return 
    connectors = processed_conditions[1]
    processed_conditions = processed_conditions[0]

    i = 0
    while i < len(processed_conditions):
        temp = filter(processed_conditions[i].get_operand(), processed_conditions[i].get_operator(), processed_conditions[i].get_value(), metadata, table)
        
        if connectors[i] == "OR":    
            result = union(result, temp)
        elif connectors[i] == "AND":
            result = intersection(result, temp)
        else:
            result = temp
        i += 1

    #4
    if column == "*":
        return result
    wanted_columns = []

    result_table = []
    for i in range(len(metadata_columns)):
        for j in range(len(query_columns)):
           if query_columns[j] == metadata_columns[i].strip():
               wanted_columns.append(i)

    for i in range(len(result)):
        result_row = []
        for j in range(len(wanted_columns)):
            indices = wanted_columns[j]
            result_row.append(result[i][indices].strip())
        result_table.append(result_row)

    return result_table

def insert(query):
    before_values, valueswbracket = query.split(" VALUES (")
    values, nothing = valueswbracket.split(")")
    nothing, table_name = before_values.split("INTO ")
    db = getTable(table_name)
    metadata = db[:2]
    listed_values = values.split(", ")
    if len(listed_values) == len(metadata[0]):
        errors = check2(listed_values, metadata)
        if len(errors) == 0:
            with open(f"{table_name}.db", 'a') as file:
                file.write(f"\n{values}")
        else:
            return errors
    else:
        return "Insufficient columns for one row."
    
def update(query):
    # UPDATE table_name SET col = 'value, ...', col2 = "..." WHERE condition
    result = []

    beforeset, afterset = query.split(" SET ")
    x, table_name = beforeset.split("UPDATE ")
    colnvalues , condition = afterset.split(" WHERE ")
    colmultinvalues = colnvalues.split(", ")
    colmulti = []
    values = []

    for i in range(len(colmultinvalues)):
        h, y = colmultinvalues[i].split(" = ")
        colmulti.append(h)
        values.append(y)
    condition_parts = condition.split(" ")
    metadata_columns = metadata[0]

    db = getTable(table_name)

    processed_conditions = preprocess(condition_parts, metadata)
    if len(processed_conditions[0]) == 0:
        print(processed_conditions[1])
        return 
    connectors = processed_conditions[1]
    processed_conditions = processed_conditions[0]

    i = 0
    while i < len(processed_conditions):
        temp = filter(processed_conditions[i].get_operand(), processed_conditions[i].get_operator(), processed_conditions[i].get_value(), metadata, db)
        
        if connectors[i] == "OR":    
            result = union(result, temp)
        elif connectors[i] == "AND":
            result = intersection(result, temp)
        else:
            result = temp
        i += 1

    i = 0
    result_table = []
    wanted_columns = []

    # for i in range(len(colmulti)):
    #     errors = check2(colmulti, metadata)
    #     if len(errors) > 0:
    #         print(errors)
    #         return
    result
    for i in range(len(metadata_columns)):
        for j in range(len(colmulti)):
            if colmulti[j] == metadata_columns[i].strip():
                wanted_columns.append(i)

    db_string = ""

    for k in range(len(db)):
        for z in range(len(db[k])):
            db_string += str(db[k][z]) 
            if k < len(db[k]) - 1:
                db_string += str(", ")# Ensure the item is a string
        db_string += "\n"

    i = 0 
    for i in range(len(result)):
        for j in range(len(wanted_columns)):
            new = copy.deepcopy(result[i])
            new[wanted_columns[j]] = values[j]
            result_string = ""
            new_string = ""
            for k in range(len(result[i])):
                result_string += str(result[i][k]) 
                if k < len(result[i]) - 1:
                    result_string += str(", ") # Ensure the item is a string
            for y in range(len(new)):
                new_string += str(new[y]) 
                if y < len(new) - 1:
                    new_string += str(", ") # Ensure the item is a string

            db_string = re.sub(result_string, new_string+'\n', db_string)

    with open(f"{table_name}.db", 'w') as f:
        f.write(f"{db_string}\n")
    

# print(select("SELECT Name, Age FROM student WHERE Name = John AND Age = 13"))
# print(select("SELECT Age, Height FROM student WHERE Age > 13 AND Height < 174"))
# print(select("SELECT * FROM student WHERE Name = Bob OR Name = John AND Age = 16"))
# print(insert("INSERT INTO student VALUES (hi, 10)"))
print(update("UPDATE student SET Age = 15 WHERE Name = John"))