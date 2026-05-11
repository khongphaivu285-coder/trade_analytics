TABLES = {

    "purchase_order": {

        "excel": r"data/raw/TF_PurchaseOrder1.xlsx",

        "sheet": "TF_PurchaseOrder",

        "primary_key": "orderno",

        "table_type": "fact",

        "date_columns": [
            "orderdate2"
        ],

        "required_columns": [

            "customerid",

            "productid",

            "orderdate2",

            "orderno"
        ] 
    },

    "customer": {

        "excel": r"data/raw/TD_Customer1.xlsx",

        "sheet": "TD_Customer",

        "primary_key": "customerid",

        "table_type": "dimension",
        
        "required_columns": [

            "customerid"
        ] 
    },

    "product": {

        "excel": r"data/raw/TD_Product.xlsx",

        "sheet": "TD_Product",

        "primary_key": "productid",

        "table_type": "dimension",

        "required_columns": [

            "productid"
        ] 
    },

    "vcp": {

        "excel": r"data/raw/VCP_Master.xlsx",

        "sheet": "VCP",

        "primary_key": "customerid",

        "table_type": "fact",

        "required_columns": [

            "customerid",

            "productid"
        ] 
    }
}