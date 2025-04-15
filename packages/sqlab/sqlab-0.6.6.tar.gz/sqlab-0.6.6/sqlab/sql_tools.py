import sqlparse
from sqlparse.sql import Token, TokenList
from sqlparse.tokens import Keyword, DML, Text


def append_column(sql: str, column: str) -> str:
    """
    Append the given column to the last SELECT query of the given SQL statements.

    NB. The column cannot be inserted in the first position when the existing SELECT expressions
    start with an unqualified star: "SELECT id, * FROM table" raises an error. Hence, the SELECT
    expression is inserted after all the existing columns.
    """

    statements = list(sqlparse.parse(sql))

    # Get the last DML statement (SELECT in this case)
    for i in range(len(statements) - 1, -1, -1):
        if statements[i].get_type() == "SELECT":
            query_index = i
            last_query = statements[i]
            break
    else:
        raise ValueError("No SELECT statement found!")
    
    # Use a single iterator to find the SELECT and the next keyword
    indexed_tokens = enumerate(last_query.tokens)
    
    # Skip all tokens until we find the outer SELECT
    for (i, token) in indexed_tokens:
        if token.ttype == DML and token.value.upper() == "SELECT":
            break # SELECT found at index i
    else:
        raise ValueError("SELECT not found!")
    
    # Find the index of the next keyword, if any
    for (i, token) in indexed_tokens:
        if token.ttype == Keyword:
            idx_next_keyword = i # next keyword (probably FROM) found at index i
            break
    else: 
        idx_next_keyword = i + 1 # this is a SELECT statement without FROM
    
    # Insert the new column (as text) before the next keyword
    tokens = TokenList(last_query.tokens)
    to_insert = Token(Text, f", {column}\n")
    tokens.insert_before(idx_next_keyword, to_insert)

    # Update the SQL statements
    statements[query_index] = tokens
    return "".join(map(str, statements))

if __name__ == "__main__":
    formula = "new_col"
    sql = "select col1, col2 from table"
    result = append_column(sql, formula)
    assert result == "select col1, col2 , new_col\nfrom table"
