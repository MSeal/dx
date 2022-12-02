import traceback
from typing import Any

import pandas as pd
from pandas.io.json import build_table_schema

from dx.settings import get_settings

settings = get_settings()


def test_compatibility(value: Any, as_dataframe: bool = True) -> dict:
    """
    Convenience function to test the compatibility of a given object
    with the different steps involved with the dx display modes.
    - `pandas.io.json.build_table_schema` (https://github.com/pandas-dev/pandas/blob/main/pandas/io/json/_table_schema.py)
    - `jupyter_client.jsonutil.json_clean` (https://github.com/jupyter/jupyter_client/blob/main/jupyter_client/jsonutil.py)
    - `duckdb conn.register`
    - final dx output type

    Parameters
    ----------
    value: Any
        The value to test compatibility with.
    as_dataframe: bool
        Whether to return the results as a pandas DataFrame (if `True`),
        or as a dictionary (if `False`)
    """
    result = {}
    result.update(test_build_table_schema(value))
    result.update(test_json_clean(value))
    result.update(test_db_write(value))
    result.update(test_dx_handling(value))
    if as_dataframe:
        return pd.DataFrame(result).transpose()
    return result


def test_build_table_schema(value: Any, as_dataframe: bool = False) -> dict:
    """
    Convenience function to test the compatibility of a given object
    with the pandas.io.json.build_table_schema function, which
    is called to set up the initial column schema during dx formatting.

    Parameters
    ----------
    value: Any
        The value to test compatibility with.
    as_dataframe: bool
        Whether to return the results as a pandas DataFrame (if `True`),
        or as a dictionary (if `False`)
    """
    df = pd.DataFrame({"test": [value]})
    result = {}

    try:
        schema = build_table_schema(df, index=False)
        fields = schema["fields"]
        field_type = [
            field_schema["type"] for field_schema in fields if field_schema["name"] == "test"
        ][0]
        result["pandas.io.json.build_table_schema"] = {
            "success": True,
            "type": field_type,
        }
    except Exception as e:
        result["pandas.io.json.build_table_schema"] = {
            "error": str(e),
            "success": False,
            "traceback": traceback.format_exc(),
        }

    if as_dataframe:
        return pd.DataFrame(result).transpose()
    return result


def test_json_clean(value: Any, as_dataframe: bool = False) -> dict:
    """
    Convenience function to test the compatibility of a given object
    with the jupyter_client.jsonutil.json_clean function, which
    is called during IPython.display after dx formatting.

    Parameters
    ----------
    value: Any
        The value to test compatibility with.
    as_dataframe: bool
        Whether to return the results as a pandas DataFrame (if `True`),
        or as a dictionary (if `False`)
    """
    df = pd.DataFrame({"test": [value]})
    result = {}

    try:
        from jupyter_client.jsonutil import json_clean

        clean_json = json_clean(df.to_dict("records"))
        clean_json_value = clean_json[0]["test"]
        result["jupyter_client.jsonutil.json_clean"] = {
            "success": True,
            "type": type(clean_json_value),
            "value": clean_json_value,
        }
    except Exception as e:
        result["jupyter_client.jsonutil.json_clean"] = {
            "error": str(e),
            "success": False,
            "traceback": traceback.format_exc(),
        }

    if as_dataframe:
        return pd.DataFrame(result).transpose()
    return result


def test_db_write(value: Any, as_dataframe: bool = False) -> dict:
    """
    Convenience function to test the compatibility of a given object
    inside a pandas DataFrame during registration with a duckdb connection,
    which is used during Datalink-enabled dataframe tracking for
    push-down filtering.

    Parameters
    ----------
    value: Any
        The value to test compatibility with.
    as_dataframe: bool
        Whether to return the results as a pandas DataFrame (if `True`),
        or as a dictionary (if `False`)
    """
    from dx.utils.tracking import get_db_connection  # circular import

    df = pd.DataFrame({"test": [value]})
    result = {}

    db_connection = get_db_connection()
    try:
        db_connection.register("test", df)
        db_df = db_connection.execute("SELECT * FROM test").df()
        db_df_value = db_df.iloc[0]["test"]
        result["duckdb.conn.register"] = {
            "type": type(db_df_value),
            "success": True,
            "value": db_df_value,
        }
    except Exception as e:
        result["duckdb.conn.register"] = {
            "error": str(e),
            "success": False,
            "traceback": traceback.format_exc(),
        }

    if as_dataframe:
        return pd.DataFrame(result).transpose()
    return result


def test_dx_handling(value: Any, as_dataframe: bool = False) -> dict:
    """
    Convenience function to test the compatibility of a given object
    inside a pandas DataFrame through the entire dx formatting
    and data type handling process.

    Parameters
    ----------
    value : Any
        The value to test compatibility with.
    as_dataframe : bool, optional
        Whether to return the results as a pandas DataFrame (if `True`),
        or as a dictionary (if `False`)
    """
    from dx.formatters.main import handle_format  # circular import

    df = pd.DataFrame({"test": [value]})
    result = {}

    try:
        payload, _ = handle_format(df, with_ipython_display=False)

        if settings.DISPLAY_MODE == "simple":
            dx_value = payload[settings.MEDIA_TYPE]["data"][0]["test"]
        if settings.DISPLAY_MODE == "enhanced":
            dx_value = payload[settings.MEDIA_TYPE]["data"][0][0]

        dx_schema_fields = payload[settings.MEDIA_TYPE]["schema"]["fields"]
        # should only be two fields here by default: `index` and `test`
        # but we wanted to run the entire formatting process, which doesn't need
        # an option to disable `index` from being included
        dx_schema_type = [field["type"] for field in dx_schema_fields if field["name"] == "test"][0]

        result["dx.handle_format"] = {
            "type": type(dx_value),
            "success": True,
            "value": dx_value,
            "schema_type": dx_schema_type,
        }
    except Exception as e:
        result["dx.handle_format"] = {
            "error": str(e),
            "success": False,
            "traceback": traceback.format_exc(),
        }

    if as_dataframe:
        return pd.DataFrame(result).transpose()
    return result
