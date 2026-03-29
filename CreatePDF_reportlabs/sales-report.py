from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

# Create a PDF document named "report.pdf"
# pagesize should be A4
doc = SimpleDocTemplate('report.pdf', pagesize=A4)

# Load default built-in text styles like Title, Normal, Heading1, etc.
styles = getSampleStyleSheet()

# Create a title paragraph using the Title style
title = Paragraph('Sales Report 2025', styles['Title'])

# Sample sales data for 3 products across 4 quarters
sales_data = {
    'Alpha': [100, 120, 140, 120],
    'Beta': [70, 60, 60, 50],
    'Gamma': [200, 200, 200, 340]
}

# Table data must be a list of rows
# Each row is also a list
table_data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],   # Header row
    ['Alpha'] + sales_data['Alpha'],       # Product name + Alpha values
    ['Beta'] + sales_data['Beta'],         # Product name + Beta values
    ['Gamma'] + sales_data['Gamma']        # Product name + Gamma values
]

# Create the table and apply styling
table = Table(
    table_data,
    style=[
        # Add grid lines around all cells
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),

        # Make the first row bold (the header row)
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]
)

# Create a drawing area for the chart
chart = Drawing(400, 200)

# Create a vertical bar chart
bar_chart = VerticalBarChart()

# Add the sales data to the chart
bar_chart.data = [
    sales_data['Alpha'],
    sales_data['Beta'],
    sales_data['Gamma']
]

# Label the x-axis with quarter names
bar_chart.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4']

# Set the lowest value on the y-axis
bar_chart.valueAxis.valueMin = 0

# Set the highest value on the y-axis slightly above the maximum number
# This gives some empty space above the tallest bar
bar_chart.valueAxis.valueMax = max(max(series) * 1.1 for series in bar_chart.data)

# Set the step size for y-axis labels
bar_chart.valueAxis.valueStep = 50

# Add the bar chart to the drawing
chart.add(bar_chart)

# Build the PDF in this order:
# 1. title
# 2. space
# 3. table
# 4. chart
doc.build([title, Spacer(0, 12), table, chart])