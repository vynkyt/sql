def getTable(table_name) -> list[list[str]]:
    table = []
    db = open(f"{table_name}.db").read()
    rows = db.split("\n")
    for i in range(len(rows)):
        columns = rows[i].split(",")
        table.append(columns)
    return table

def select(query:str) -> list[list[str]]:
    after_select = query.split("SELECT ")

    column, table_name = after_select[1].split(" FROM ")

    query_columns = column.split(", ")

    db = getTable(table_name)
    metadata = db[:2]
    table = db[2:]
    metadata_columns = metadata[0]

    if column == "*":
        return table
    wanted_columns = []

    result_table = []
    for i in range(len(metadata_columns)):
        for j in range(len(query_columns)):
           if query_columns[j] == metadata_columns[i].strip():
               wanted_columns.append(i)

    for i in range(len(table)):
        result_row = []
        for j in range(len(wanted_columns)):
            indices = wanted_columns[j]
            result_row.append(table[i][indices].strip())
        result_table.append(result_row)

    return result_table


