from streamlit_echarts import (
    st_echarts,
    JsCode
)

import pandas as pd


# =========================================
# PRODUCT FLAVOR BAR
# STACKED BAR WITH NEGATIVE VALUE
# =========================================

def render_product_flavor_bar_chart(

    df,

    title="Doanh số theo Vị và Dòng sản phẩm",

    height="420px"
):

    # =====================================
    # GROUP
    # =====================================

    chart_df = (

        df.groupby(

            [
                "tbd_brand_1",
                "tbd_line_name",
                "tbd_flavor"
            ],

            as_index=False

        )["ordervalue"]
        .sum()
    )

    # =====================================
    # CLEAN
    # =====================================

    chart_df["tbd_brand_1"] = (
        chart_df["tbd_brand_1"]
        .fillna("Unknown")
        .astype(str)
    )

    chart_df["tbd_line_name"] = (
        chart_df["tbd_line_name"]
        .fillna("Unknown")
        .astype(str)
    )

    chart_df["tbd_flavor"] = (
        chart_df["tbd_flavor"]
        .fillna("Unknown")
        .astype(str)
    )

    # =====================================
    # FLAVOR TOTAL
    # =====================================

    flavor_total_df = (

        chart_df.groupby(
            "tbd_flavor",
            as_index=False
        )["ordervalue"]
        .sum()
        .sort_values(
            "ordervalue",
            ascending=False
        )
    )

    # =====================================
    # FLAVOR LIST
    # =====================================

    flavor_list = (
        flavor_total_df[
            "tbd_flavor"
        ]
        .tolist()
    )

    # =====================================
    # SERIES NAME
    # =====================================

    chart_df["series_name"] = (

        chart_df["tbd_brand_1"]

        + " - "

        + chart_df["tbd_line_name"]
    )

    # =====================================
    # LINE LABEL
    # =====================================

    chart_df["line_label"] = (
        chart_df["tbd_line_name"]
    )

    # =====================================
    # SERIES LIST
    # =====================================

    series_list = (

        chart_df["series_name"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================
    # SERIES
    # =====================================

    series = []

    for series_name in series_list:

        series_data = []

        series_df = (

            chart_df[
                chart_df["series_name"]
                == series_name
            ]
        )

        for flavor in flavor_list:

            # =============================
            # FLAVOR DF
            # =============================

            flavor_df = (

                series_df[

                    series_df[
                        "tbd_flavor"
                    ] == flavor
                ]
            )

            # =============================
            # VALUE
            # =============================

            value = float(

                flavor_df[
                    "ordervalue"
                ].sum()
            )

            # =============================
            # LINE NAME
            # =============================

            line_name = ""

            if len(flavor_df) > 0:

                line_name = (

                    flavor_df[
                        "line_label"
                    ]
                    .iloc[0]
                )

            # =============================
            # FLAVOR TOTAL
            # =============================

            flavor_total = float(

                chart_df[

                    chart_df[
                        "tbd_flavor"
                    ] == flavor

                ]["ordervalue"]
                .sum()
            )

            # =============================
            # FLAVOR %
            # =============================

            flavor_pct = 0

            if flavor_total != 0:

                flavor_pct = (
                    value
                    / flavor_total
                ) * 100

            # =============================
            # LINE TOTAL
            # =============================

            line_total = 0

            if line_name != "":

                line_total = float(

                    chart_df[

                        chart_df[
                            "tbd_line_name"
                        ] == line_name

                    ]["ordervalue"]
                    .sum()
                )

            # =============================
            # LINE %
            # =============================

            line_pct = 0

            if line_total != 0:

                line_pct = (
                    value
                    / line_total
                ) * 100

            # =============================
            # DATA
            # =============================

            series_data.append({

                "value": value,

                "line_name": line_name,

                "line_pct": float(line_pct),

                "flavor_pct": float(flavor_pct),

                "flavor_name": flavor,

                # =========================
                # NEGATIVE COLOR
                # =========================

                "itemStyle": {

                    "color":

                        "#EE6666"

                        if value < 0

                        else None
                }
            })

        # =================================
        # SERIES APPEND
        # =================================

        series.append({

            "name": series_name,

            "type": "bar",

            # KEEP STACK
            "stack": "total",

            "barMaxWidth": 42,

            "barMinHeight": 2,

            "emphasis": {

                "focus": "series"
            },

            "data": series_data
        })

    # =====================================
    # OPTION
    # =====================================

    option = {

        # =================================
        # TITLE
        # =================================

        "title": {

            "text": title,

            "left": "center"
        },

        # =================================
        # TOOLTIP
        # =================================

        "tooltip": {

            "trigger": "axis",

            "confine": True,

            "axisPointer": {

                "type": "shadow"
            },

            "formatter": JsCode(
                """
                function(params) {

                    let flavorName =
                        params[0].axisValue;

                    let result =

                        '<b>'
                        + flavorName
                        + '</b><br/><br/>';

                    let total = 0;

                    // =====================
                    // TOTAL
                    // =====================

                    params.forEach(function(item) {

                        total += Number(
                            item.data.value || 0
                        );
                    });

                    // =====================
                    // DETAIL
                    // =====================

                    params.forEach(function(item) {

                        let data =
                            item.data || {};

                        let value =
                            Number(
                                data.value || 0
                            );

                        let lineName =
                            data.line_name || '';

                        let linePct =
                            Number(
                                data.line_pct || 0
                            );

                        let flavorPct =
                            Number(
                                data.flavor_pct || 0
                            );

                        let flavorLabel =
                            data.flavor_name || '';

                        if(value !== 0) {

                            result +=

                                item.marker

                                + ' '

                                + item.seriesName

                                + '<br/>'

                                + 'Doanh thu YTD: '

                                + Number(value)
                                    .toLocaleString('en-US')

                                + ' VNĐ'

                                + '<br/>'

                                + 'Đóng góp '

                                + flavorPct.toFixed(2)

                                + '% của vị '

                                + flavorLabel

                                + '<br/>'

                                + 'Đóng góp '

                                + linePct.toFixed(2)

                                + '% của Brand '

                                + lineName

                                + '<br/><br/>';
                        }
                    });

                    // =====================
                    // TOTAL TEXT
                    // =====================

                    result +=

                        '<b>Total: '

                        + Number(total)
                            .toLocaleString('en-US')

                        + ' VNĐ</b>';

                    return result;
                }
                """
            )
        },

        # =================================
        # LEGEND
        # =================================

        "legend": {

            "type": "scroll",

            "bottom": 0
        },

        # =================================
        # GRID
        # =================================

        "grid": {

            "left": "3%",

            "right": "4%",

            "top": 80,

            "bottom": 80,

            "containLabel": True
        },

        # =================================
        # X AXIS
        # =================================

        "xAxis": {

            "type": "category",

            "data": flavor_list,

            "axisLabel": {

                "rotate": 35
            }
        },

        # =================================
        # Y AXIS
        # =================================

        "yAxis": {

            "type": "value",

            "scale": True,

            "axisLine": {

                "show": True
            },

            "splitLine": {

                "show": True
            }
        },

        # =================================
        # SERIES
        # =================================

        "series": series
    }

    # =====================================
    # RENDER
    # =====================================

    st_echarts(

        options=option,

        height=height,

        key="product_flavor_bar_chart"
    )