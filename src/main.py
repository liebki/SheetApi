# pylint: disable=C0103,W0602,W0603
"""
sheet2api - simply turn any xlsx or csv file into a small rest api.
"""

import os
import fastapi
import pandas as pd

FILE_MISSING_ERROR = "Reloading failed, file was not found under this path."
NO_FILE_ERROR = "No file loaded, please use /reload/xlsx or /reload/csv"
NO_FILE_ERROR_CODE = 404

# xlsx = 1, csv = 0
mode = 0
csv_sep = ";"

data = None
app = fastapi.FastAPI(
    title="sheet2api",
    description="simply turn any xlsx or csv file into a small rest api.",
    version="0.0.1",
    contact={
        "url": "https://github.com/liebki/sheet2api",
    },
    license_info={
        "name": "GNU General Public License v3.0",
    },
)


def no_file_error():
    """
    Function to throw error when no file is loaded before calling
    """

    return fastapi.HTTPException(status_code=NO_FILE_ERROR_CODE, detail=NO_FILE_ERROR)


# Function to load data from xlsx
def get_data(path: str) -> pd.DataFrame:
    """
    Function to load data from xlsx

    Args:
        path (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    if mode == 1:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, sep=csv_sep)

    df.reset_index(drop=True, inplace=True)
    return df


# Root endpoint
@app.get("/")
def get_root():
    """
    Root endpoint

    Returns:
        str: _description_
    """
    return {"content": "sheet2api"}


# Endpoint to get all headers
@app.get("/headers")
def headers():
    """
    Endpoint to get all headers

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """

    global data
    if data is not None:
        return {"content:": list(data)}

    raise no_file_error()


# Endpoint to reload the CSV file with a ?file= argument
@app.get("/reload/csv/")
def reload_data_csv(file: str, sep: str):
    """
    Endpoint to reload the CSV file with a ?file= argument

    Args:
        file (str): _description_

    Returns:
        _type_: _description_
    """

    try:
        if not os.path.exists(file):
            return {"content": FILE_MISSING_ERROR }

        global mode
        mode = 0

        global csv_sep
        csv_sep = sep

        global data
        data = get_data(file)

        return {"content": "Reloaded csv successfully."}
    except fastapi.HTTPException as e:
        return {"content": f"Reloading csv failed:\n{e.detail}"}


# Endpoint to reload the xlsx file with a ?file= argument
@app.get("/reload/xlsx/")
def reload_data_xlsx(file: str):
    """
    Endpoint to reload the xlsx file with a ?file= argument

    Args:
        file (str): _description_

    Returns:
        _type_: _description_
    """

    try:
        if not os.path.exists(file):
            return {"content": FILE_MISSING_ERROR}

        global mode
        mode = 1

        global data
        data = get_data(file)

        return {"content": "Reloaded xlsx successfully."}
    except fastapi.HTTPException as e:
        return {"content": f"Reloading xlsx failed:\n{e.detail}"}


# Endpoint to get the count of items
@app.get("/count")
def get_count():
    """
    Endpoint to get the count of items

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """

    global data
    if data is not None:
        return {"content": str(len(data))}

    raise no_file_error()


# Endpoint to get a full column by header name
@app.get("/fullcol/{row}")
def full_col(row: str):
    """
    Endpoint to get a full column by header name

    Args:
        row (str): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """

    global data
    if data is not None:
        return {"content": data[row].tolist()}

    raise no_file_error()


# Endpoint to get a list of all rows
@app.get("/allrows")
def all_rows():
    """
    Endpoint to get full rows by count

    Args:
        row (int): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """
    item_liste = []
    global data
    if data is not None:
        for item in range(len(data)):
            row = full_row_base(item)
            item_liste.append(row)

        return {"content": item_liste}

    raise no_file_error()


# Endpoint to get a list of full rows by count
@app.get("/fullrows/{count}")
def full_rows(count: int):
    """
    Endpoint to get full rows by count

    Args:
        row (int): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """
    item_liste = []
    global data
    if data is not None:
        for item in range(count):
            row = full_row_base(item)
            item_liste.append(row)

        return {"content": item_liste}

    raise no_file_error()


# Endpoint to get a full row by index
@app.get("/fullrow/{row}")
def full_row(row: int):
    """
    Endpoint to get a full row by index

    Args:
        row (int): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """
    return {"content": full_row_base(row)}


# Base def to get rows by index/count
def full_row_base(number: int):
    """
    Base def to get rows by index/count

    Args:
        row (int): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """
    global data
    if data is not None:
        row_data = data.iloc[number]
        return row_data.to_dict()

    raise no_file_error()


# Endpoint to get a certain cell by header and index
@app.get("/item/{header}/{index}")
def get_item(header: str, index: int):
    """
    Endpoint to get a certain cell by header and index

    Args:
        header (str): _description_
        index (int): _description_

    Raises:
        no_file_error: _description_

    Returns:
        _type_: _description_
    """

    global data
    if data is not None:
        return {"content": data[header][index]}

    raise no_file_error()
