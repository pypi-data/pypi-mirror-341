import pandas as pd

def join_values(list_of_values, remove_nan: bool = False):
    
    list_of_values = [
        None
        if li is None or (remove_nan and pd.isna(li))
        else li.replace("'", "''")
        if (isinstance(li, str) and "'" in li)
        else li
        for li in list_of_values
    ]
    
    return ", ".join(
        [
            f"'{valor.strip()}'"
            if isinstance(valor, str)
            else f"{int(valor)}"
            if isinstance(valor, float) and valor.is_integer()
            else "NULL"
            if valor is None
            else f"{valor}"
            for valor in list_of_values
        ]
    )