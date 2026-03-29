from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image, TableStyle, XPreformatted

# Create the invoice PDF with A4 size and margins on all sides
doc = SimpleDocTemplate(
    'invoice.pdf',
    pagesize=A4,
    rightMargin=20*mm,
    leftMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=20*mm
)

# Load default styles
styles = getSampleStyleSheet()

# This list will store all PDF elements in order
story = []

# Path to the company logo image
logo_path = 'nn_logo.jpg'

# Try to load the logo image
# If image is missing, show company name instead
try:
    logo = Image(logo_path, width=35*mm, height=35*mm)
except:
    logo = Paragraph('<b>ACME Corporation</b>', styles['Title'])

# Company address and contact details
# XPreformatted keeps line breaks exactly as written
company_info = XPreformatted(
    'ACME Corporation\n123 Market Street\nMetropolis, CA 94103\n+1 (555) 123-4567',
    styles['Normal']
)

# Header table with logo on the left and company info on the right
header = Table([[logo, company_info]], colWidths=[60*mm, 100*mm])
header.setStyle(TableStyle([
    # Align content to the top inside the cells
    ('VALIGN', (0, 0), (-1, -1), 'TOP')
]))

# Add header and some space below it
story += [header, Spacer(1, 20)]

# Add invoice title
story += [Paragraph('<b>INVOICE</b>', styles['Title']), Spacer(1, 10)]

# Invoice metadata
invoice_info = [
    ['Invoice No:', 'INV-2025-074'],
    ['Date:', '2025-11-05'],
    ['Due Date:', '2025-11-20']
]

# Customer address information
customer_info = XPreformatted(
    'John Doe\n45 Elm Avenue\nGotham, NY 10001',
    styles['Normal']
)

# Left side table: invoice details
left = Table(invoice_info, colWidths=[70, 70])

# Right side table: billing info
right = Table([[Paragraph('Bill To:', styles['Normal']), customer_info]], colWidths=[50, 120])

# Put both tables inside one bigger table so they appear side by side
info = Table([[left, right]], colWidths=[90*mm, 90*mm])
info.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP')
]))

# Add invoice info section and a bigger space below it
story += [info, Spacer(1, 80)]

# Line items sold in the invoice
items = [
    ['Description', 'Qty', 'Unit Price', 'Tax', 'Total'],
    ['Web Design Package', 1, '$1,200.00', '10%', '$1,320.00'],
    ['Hosting (12 months)', 1, '$180.00', '10%', '$198.00'],
    ['Domain (1 year)', 1, '$15.00', '0%', '$15.00'],
    ['Maintenance', 2, '$75.00', '10%', '$165.00']
]

# Create the main invoice table
table = Table(items, hAlign='LEFT', colWidths=[200, 50, 70, 50, 70])
table.setStyle(TableStyle([
    # Dark background for header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),

    # White text for header row
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

    # Align numeric columns to the right
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),

    # Bold header row
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

    # Add table borders
    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),

    # Light background for the body rows
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
]))

# Add the items table and space below it
story += [table, Spacer(1, 80)]

# Totals section at the bottom
totals = [
    ['Subtotal:', '$1,560.00'],
    ['Tax (10%):', '$156.00'],
    ['Total Due:', '$1,716.00']
]

# Create totals table and align it to the right
totals_table = Table(totals, colWidths=[370, 70], hAlign='RIGHT')
totals_table.setStyle(TableStyle([
    # Right-align amount column
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),

    # Normal font for subtotal and tax rows
    ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),

    # Bold font for the final total
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),

    # Line above the final total row
    ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
]))

# Add totals section and space below it
story += [totals_table, Spacer(1, 30)]

# Add notes heading
story.append(Paragraph('<b>Notes:</b>', styles['Heading3']))

# Notes text with line breaks
notes = (
    'Thank you for your business. Payment is due within 15 days.\n'
    'Please transfer to account #12345678, ACME Corp Bank, SWIFT: ACMEBANK.'
)

# Add notes and final spacing
story += [XPreformatted(notes, styles['Normal']), Spacer(1, 40)]

# Add copyright line at the bottom
story.append(Paragraph('© 2025 ACME Corporation', styles['Normal']))

# Build the final PDF
doc.build(story)