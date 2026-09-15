from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
import os


# ============================================
# REPORT DIRECTORY
# ============================================

REPORT_DIRECTORY = "reports/generated"


# ============================================
# CREATE REPORT DIRECTORY
# ============================================

def create_report_directory():
    """
    Create the report directory if it
    does not already exist.
    """

    os.makedirs(
        REPORT_DIRECTORY,
        exist_ok=True
    )


# ============================================
# FORMAT CURRENCY
# ============================================

def format_currency(value):
    """
    Format a number as Indian currency.
    """

    try:
        return f"₹{float(value):,.2f}"

    except (ValueError, TypeError):
        return "₹0.00"


# ============================================
# CREATE TABLE
# ============================================

def create_table(data, column_widths=None):
    """
    Create a formatted ReportLab table.
    """

    table = Table(
        data,
        colWidths=column_widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1f2937")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f3f4f6")
                ]
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    return table


# ============================================
# CREATE SALES REPORT
# ============================================

def generate_sales_report(
    analysis_results,
    filename="sales_report.pdf"
):
    """
    Generate a complete PDF sales report.

    Parameters:
        analysis_results:
            Dictionary returned by analyze_sales_data()

        filename:
            Name of the generated PDF file.

    Returns:
        Path of generated PDF.
    """

    create_report_directory()

    report_path = os.path.join(
        REPORT_DIRECTORY,
        filename
    )

    document = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=6
    )

    story = []

    # ========================================
    # TITLE
    # ========================================

    story.append(
        Paragraph(
            "SALES & BUSINESS ANALYTICS REPORT",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Sales Analytics Dashboard",
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    # ========================================
    # SUMMARY
    # ========================================

    summary = analysis_results.get(
        "summary",
        {}
    )

    story.append(
        Paragraph(
            "Sales Summary",
            heading_style
        )
    )

    summary_data = [
        ["Metric", "Value"],

        [
            "Total Revenue",
            format_currency(
                summary.get(
                    "total_revenue",
                    0
                )
            )
        ],

        [
            "Total Orders",
            str(
                summary.get(
                    "total_orders",
                    0
                )
            )
        ],

        [
            "Total Quantity Sold",
            str(
                summary.get(
                    "total_quantity",
                    0
                )
            )
        ],

        [
            "Average Order Value",
            format_currency(
                summary.get(
                    "average_order_value",
                    0
                )
            )
        ]
    ]

    story.append(
        create_table(
            summary_data,
            [3.2 * inch, 2.5 * inch]
        )
    )

    # ========================================
    # TOP PRODUCTS
    # ========================================

    top_products = analysis_results.get(
        "top_products"
    )

    if top_products is not None and not top_products.empty:

        story.append(
            Paragraph(
                "Top Products",
                heading_style
            )
        )

        product_data = [
            [
                "Product",
                "Revenue",
                "Quantity",
                "Orders"
            ]
        ]

        for _, row in top_products.iterrows():

            product_data.append([
                str(row["product_name"]),
                format_currency(row["revenue"]),
                str(row["quantity_sold"]),
                str(row["orders"])
            ])

        story.append(
            create_table(
                product_data,
                [
                    2.3 * inch,
                    1.5 * inch,
                    1.1 * inch,
                    1.0 * inch
                ]
            )
        )

    # ========================================
    # TOP CUSTOMERS
    # ========================================

    top_customers = analysis_results.get(
        "top_customers"
    )

    if top_customers is not None and not top_customers.empty:

        story.append(
            Paragraph(
                "Top Customers",
                heading_style
            )
        )

        customer_data = [
            [
                "Customer",
                "Total Spent",
                "Orders",
                "Quantity"
            ]
        ]

        for _, row in top_customers.iterrows():

            customer_data.append([
                str(row["customer_name"]),
                format_currency(
                    row["total_spent"]
                ),
                str(row["orders"]),
                str(row["quantity_purchased"])
            ])

        story.append(
            create_table(
                customer_data,
                [
                    2.3 * inch,
                    1.5 * inch,
                    1.1 * inch,
                    1.0 * inch
                ]
            )
        )

    # ========================================
    # CATEGORY PERFORMANCE
    # ========================================

    category_data_df = analysis_results.get(
        "category_performance"
    )

    if (
        category_data_df is not None
        and not category_data_df.empty
    ):

        story.append(
            Paragraph(
                "Category Performance",
                heading_style
            )
        )

        category_data = [
            [
                "Category",
                "Revenue",
                "Quantity",
                "Orders"
            ]
        ]

        for _, row in category_data_df.iterrows():

            category_data.append([
                str(row["category"]),
                format_currency(
                    row["revenue"]
                ),
                str(row["quantity_sold"]),
                str(row["orders"])
            ])

        story.append(
            create_table(
                category_data,
                [
                    2.3 * inch,
                    1.5 * inch,
                    1.1 * inch,
                    1.0 * inch
                ]
            )
        )

    # ========================================
    # PAYMENT METHOD
    # ========================================

    payment_data_df = analysis_results.get(
        "payment_methods"
    )

    if (
        payment_data_df is not None
        and not payment_data_df.empty
    ):

        story.append(
            Paragraph(
                "Payment Method Analysis",
                heading_style
            )
        )

        payment_data = [
            [
                "Payment Method",
                "Revenue",
                "Orders"
            ]
        ]

        for _, row in payment_data_df.iterrows():

            payment_data.append([
                str(row["payment_method"]),
                format_currency(
                    row["revenue"]
                ),
                str(row["orders"])
            ])

        story.append(
            create_table(
                payment_data,
                [
                    2.5 * inch,
                    1.8 * inch,
                    1.5 * inch
                ]
            )
        )

    # ========================================
    # BUILD PDF
    # ========================================

    document.build(story)

    return report_path