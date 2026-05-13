from database.connection import (

    get_connection
)

# =========================
# SALES SEMANTIC MODEL
# =========================

def sales_model():

    conn = get_connection()

    query = """

    SELECT

    -- =====================
    -- FACT
    -- =====================

     po.orderno

    ,po."số_chứng_từ"
    ,po."số_hóa_đơn"

    ,po.orderdate1
    ,po.orderdate2
    ,po.orderdate3

    ,po.ordertype1
    ,po.ordertype2

    -- =====================
    -- CALENDAR
    -- =====================

    ,YEAR(po.orderdate2) AS order_year

    ,MONTH(po.orderdate2) AS order_month

    ,LPAD(
        CAST(MONTH(po.orderdate2) AS VARCHAR),
        2,
        '0'
    )
    || ' - Tháng '
    || CAST(MONTH(po.orderdate2) AS VARCHAR)
    AS order_month_name

    ,CAST(YEAR(po.orderdate2) AS VARCHAR)
        || '-'
        || LPAD(
            CAST(MONTH(po.orderdate2) AS VARCHAR),
            2,
            '0'
        )
    AS order_year_month

    -- =====================
    -- CUSTOMER / PRODUCT
    -- =====================

    ,po.customerid
    ,po.customer_name

    ,po.productid
    ,po.tbd_productname

    -- =====================
    -- SALES
    -- =====================

    ,po.banle

    ,po.pcquantity
    ,po.csquantity

    ,po.ordervalue

    -- =====================
    -- ACTIVITY
    -- =====================

    ,po.acttype1
    ,po.acttype2

    ,po.actdetail

    -- =====================
    -- PRODUCT HIERARCHY
    -- =====================

    ,po."quy_đổi_dvt"

    ,po.tbd_brand_1
    ,po.tbd_brand_2

    ,po.tbd_line_name
    ,po.tbd_flavor
    ,po.tbd_package_name

    -- =====================
    -- CUSTOMER HIERARCHY
    -- =====================

    ,po.chain_2
    ,po.chain_3

    ,po."nhóm_khách_hàng"

    ,po."khu_vực"

    ,po."kênh"

    -- =====================
    -- OTHERS
    -- =====================

    ,po."diễn_giải_chung"

    ,po.rowunique
    ,po.isduplicate

    ,po.linekey
    ,po.hashkey

    -- =====================
    -- FROM
    -- =====================

    FROM purchase_order po
    
    LEFT JOIN customer c
        ON po.customerid = c.customerid
    
    LEFT JOIN product p
        ON po.productid = p.productid
    
    WHERE 1 = 1

        AND po.orderno IS NOT NULL
        AND po."kênh" IN ('1. MT', 'NPP LIÊN MINH')
        AND po.ordertype1 = 'BÁN'

    """

    df = conn.execute(

        query

    ).df()

    return df


# =========================
# MONTHLY SALES
# =========================

def sales_by_month(df):

    chart_df = (

        df.groupby(
            [
                "order_year",
                "order_month",
                "order_month_name"
            ],
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values(
            [
                "order_year",
                "order_month"
            ]
        )
    )

    return chart_df