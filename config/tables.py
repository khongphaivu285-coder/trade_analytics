TABLES = {

    "purchase_order": {

        "excel": r"data/raw/TF_PurchaseOrder1.xlsx",

        "sheet": "TF_PurchaseOrder",

        "primary_key": "rowUnique",

        "table_type": "fact"
    },

    "customer": {

        "excel": r"data/raw/TD_Customer1.xlsx",

        "sheet": "TD_Customer",

        "primary_key": "CustomerID",

        "table_type": "dimension"
    },

    "product": {

        "excel": r"data/raw/TD_Product.xlsx",

        "sheet": "TD_Product",

        "primary_key": "ProductID",

        "table_type": "dimension"
    },

    "vcp": {

        "excel": r"data/raw/VCP_Master.xlsx",

        "sheet": "VCP",

        "primary_key": "rowUnique",

        "table_type": "fact"
    }
}