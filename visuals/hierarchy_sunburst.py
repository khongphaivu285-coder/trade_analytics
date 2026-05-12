from streamlit_echarts import (
    st_echarts,
    JsCode
)


# =========================================
# SUNBURST
# =========================================

def render_hierarchy_sunburst(

    df,

    title="Doanh số theo Cấu trúc Sản phẩm",

    height="420px"
):

    # =====================================
    # GROUP
    # =====================================

    grouped_df = (

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
    # BRAND LIST
    # =====================================

    brand_list = (

        grouped_df["tbd_brand_1"]
        .dropna()
        .unique()
        .tolist()
    )

    # =====================================
    # TOTAL
    # =====================================

    total_value = (
        grouped_df["ordervalue"]
        .sum()
    )

    # =====================================
    # HIERARCHY
    # =====================================

    hierarchy = []

    # =====================================
    # BRAND LOOP
    # =====================================

    for brand in brand_list:

        brand_df = (

            grouped_df[
                grouped_df["tbd_brand_1"]
                == brand
            ]
        )

        brand_value = (
            brand_df["ordervalue"]
            .sum()
        )

        # =================================
        # BRAND %
        # =================================

        brand_pct = 0

        if total_value != 0:

            brand_pct = (
                brand_value
                / total_value
            ) * 100

        line_children = []

        # =================================
        # LINE LOOP
        # =================================

        for line in (

            brand_df["tbd_line_name"]
            .dropna()
            .unique()
        ):

            line_df = (

                brand_df[
                    brand_df["tbd_line_name"]
                    == line
                ]
            )

            line_value = (
                line_df["ordervalue"]
                .sum()
            )

            # =============================
            # LINE %
            # =============================

            line_pct = 0

            if brand_value != 0:

                line_pct = (
                    line_value
                    / brand_value
                ) * 100

            flavor_children = []

            # =============================
            # FLAVOR LOOP
            # =============================

            for _, row in line_df.iterrows():

                flavor_pct = 0

                if line_value != 0:

                    flavor_pct = (
                        row["ordervalue"]
                        / line_value
                    ) * 100

                flavor_children.append({

                    "name": row["tbd_flavor"],

                    "value": round(
                        row["ordervalue"],
                        0
                    ),

                    "pct": round(
                        flavor_pct,
                        1
                    )
                })

            # =============================
            # LINE NODE
            # =============================

            line_children.append({

                "name": line,

                "value": round(
                    line_value,
                    0
                ),

                "pct": round(
                    line_pct,
                    1
                ),

                "children": flavor_children
            })

        # =================================
        # BRAND NODE
        # =================================

        hierarchy.append({

            "name": brand,

            "value": round(
                brand_value,
                0
            ),

            "pct": round(
                brand_pct,
                1
            ),

            "children": line_children
        })

    # =====================================
    # OPTION
    # =====================================

    option = {

        # =================================
        # TOOLTIP
        # =================================

        "tooltip": {

            "trigger": "item",

            "formatter": JsCode(
                """
                function(params) {

                    let pct = '';

                    if (
                        params.data.pct
                        !== undefined
                    ) {

                        pct =
                            '<br/>Đóng góp: '
                            + params.data.pct
                            + '%';
                    }

                    return (

                        '<b>'
                        + params.name
                        + '</b>'

                        + '<br/><br/>'

                        + 'Doanh số: '

                        + Number(params.value)
                            .toLocaleString('en-US')

                        + ' VNĐ'

                        + pct
                    );
                }
                """
            )
        },

        # =================================
        # TITLE
        # =================================

        "title": {

            "text": title,

            "left": "center",

            "top": 10,

            "textStyle": {

                "fontSize": 18,

                "fontWeight": 600
            }
        },

        # =================================
        # LEGEND
        # =================================

        "legend": {

            "show": True,

            "type": "scroll",

            "orient": "horizontal",

            "bottom": 8,

            "left": "center",

            "icon": "circle",

            "itemWidth": 12,

            "itemHeight": 12,

            "data": [

                {
                    "name": brand
                }

                for brand in brand_list
            ],

            "textStyle": {

                "fontSize": 11
            }
        },

        # =================================
        # SERIES
        # =================================

        "series": {

            "type": "sunburst",

            # =============================
            # IMPORTANT
            # =============================

            "selectedMode": "multiple",

            "data": hierarchy,

            # =============================
            # PIE-LIKE LAYOUT
            # =============================

            "radius": [
                "18%",
                "74%"
            ],

            "center": [
                "50%",
                "58%"
            ],

            "sort": None,

            "nodeClick": "zoomToNode",

            # =============================
            # ANIMATION
            # =============================

            "animationDuration": 250,

            "animationDurationUpdate": 250,

            # =============================
            # COLOR
            # =============================

            "colorMappingBy": "index",

            # =============================
            # STYLE
            # =============================

            "itemStyle": {

                "borderRadius": 8,

                "borderColor": "#fff",

                "borderWidth": 2
            },

            # =============================
            # EMPHASIS
            # =============================

            "emphasis": {

                "focus": "ancestor"
            },

            # =============================
            # GLOBAL LABEL
            # =============================

            "label": {

                "show": False
            },

            # =============================
            # LEVELS
            # =============================

            "levels": [

                {},

                # ==========================
                # BRAND
                # ==========================

                {

                    "r0": "18%",
                    "r": "38%",

                    "label": {

                        "show": False
                    }
                },

                # ==========================
                # LINE
                # ==========================

                {

                    "r0": "38%",
                    "r": "56%",

                    "label": {

                        "show": False
                    },

                    "itemStyle": {

                        "opacity": 0.92
                    }
                },

                # ==========================
                # FLAVOR
                # ==========================

                {

                    "r0": "56%",
                    "r": "74%",

                    "label": {

                        "show": True,

                        "position": "outside",

                        "rotate": 0,

                        "fontSize": 10,

                        "overflow": "truncate",

                        "width": 90,

                        "minAngle": 4
                    },

                    "labelLine": {

                        "show": True,

                        "length": 8,

                        "length2": 6
                    },

                    "itemStyle": {

                        "opacity": 0.82
                    }
                }
            ]
        }
    }

    # =====================================
    # RENDER
    # =====================================

    st_echarts(

        options=option,

        height=height,

        key="hierarchy_sunburst"
    )