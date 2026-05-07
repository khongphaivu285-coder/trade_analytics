import pandas as pd

from config.tables import TABLES


def load_excel(table_name):

    # =========================
    # GET TABLE CONFIG
    # =========================

    config = TABLES[table_name]

    # =========================
    # LOAD EXCEL
    # =========================

    df = pd.read_excel(

        config["excel"],

        sheet_name=config["sheet"]
    )

    return df