# #First install the packages:

# pip install reportlab fillpdf pandas

# Then run:

# python mains.py
# What files this will create

# It will create:

# sample_template.pdf → your fillable template
# filled_output.pdf → one filled sample PDF
# outputs/ → folder with many PDFs from CSV

import os
from datetime import date

import pandas as pd
from fillpdf import fillpdfs

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# ============================================================
# PATHS
# ============================================================
# Use the folder where this script is located.
# This avoids "file not found" errors.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PDF = os.path.join(BASE_DIR, "sample_template.pdf")
SINGLE_OUTPUT_PDF = os.path.join(BASE_DIR, "filled_output.pdf")
CSV_FILE = os.path.join(BASE_DIR, "data.csv")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")


# ============================================================
# STEP 1: CREATE A FILLABLE PDF TEMPLATE
# ============================================================
def create_sample_template(pdf_path: str) -> None:
    """
    Create a simple fillable PDF form using ReportLab.
    This PDF will contain:
    - customer_id text field
    - address text field
    - price text field
    - date text field
    - accept checkbox
    """

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "Sample Invoice Form")

    # Labels
    c.setFont("Helvetica", 12)
    c.drawString(50, 700, "Customer ID:")
    c.drawString(50, 650, "Address:")
    c.drawString(50, 600, "Price:")
    c.drawString(50, 550, "Date:")
    c.drawString(50, 500, "Accept Terms:")

    # Create form fields
    form = c.acroForm

    form.textfield(
        name="customer_id",
        tooltip="Customer ID",
        x=150, y=685,
        width=300, height=20,
        borderStyle="inset",
        forceBorder=True
    )

    form.textfield(
        name="address",
        tooltip="Address",
        x=150, y=635,
        width=300, height=20,
        borderStyle="inset",
        forceBorder=True
    )

    form.textfield(
        name="price",
        tooltip="Price",
        x=150, y=585,
        width=300, height=20,
        borderStyle="inset",
        forceBorder=True
    )

    form.textfield(
        name="date",
        tooltip="Date",
        x=150, y=535,
        width=300, height=20,
        borderStyle="inset",
        forceBorder=True
    )

    # Checkbox field
    # The checked value may appear as "Yes" or another export value
    # depending on the PDF form system.
    form.checkbox(
        name="accept",
        tooltip="Accept Terms",
        x=150, y=495,
        size=15,
        buttonStyle="check",
        borderStyle="solid",
        forceBorder=True
    )

    c.save()
    print(f"Created template: {pdf_path}")


# ============================================================
# STEP 2: PRINT ALL FIELD NAMES
# ============================================================
def show_field_names(pdf_path: str) -> None:
    """
    Read the PDF template and print all form field names.
    This helps you know the exact keys to use in your dictionary.
    """
    fields = fillpdfs.get_form_fields(pdf_path)
    print("\nForm fields found in template:")
    print(fields)


# ============================================================
# STEP 3: FILL ONE PDF
# ============================================================
def fill_one_pdf(template_path: str, output_path: str) -> None:
    """
    Fill one PDF using a dictionary of values.
    The dictionary keys must match the field names in the PDF.
    """

    data = {
        "customer_id": "ID1",
        "address": "My Street 20",
        "price": "500",
        "date": str(date.today()),
        # For checkboxes, the value may need to be "Yes"
        # If it does not work in your template, inspect the field value.
        "accept": "Yes"
    }

    fillpdfs.write_fillable_pdf(template_path, output_path, data)
    print(f"Filled PDF created: {output_path}")


# ============================================================
# STEP 4: FILL MANY PDFS FROM CSV
# ============================================================
def fill_pdfs_from_csv(template_path: str, csv_path: str, output_dir: str) -> None:
    """
    Read rows from a CSV file and generate one filled PDF per row.
    """

    if not os.path.exists(csv_path):
        print(f"\nCSV file not found: {csv_path}")
        print("Skipping batch PDF creation.")
        return

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    print(f"\nCSV loaded: {len(df)} rows found")

    for index, row in df.iterrows():
        # Build the dictionary for the current row
        # Column names in CSV should match the PDF field names
        data_dict = {
            "customer_id": str(row["customer_id"]),
            "address": str(row["address"]),
            "price": str(row["price"]),
            "date": str(row["date"]),
            "accept": "Yes" if str(row["accept"]).lower() == "yes" else ""
        }

        # Unique output file name for each customer
        output_path = os.path.join(
            output_dir,
            f"{row['customer_id']}_invoice.pdf"
        )

        fillpdfs.write_fillable_pdf(template_path, output_path, data_dict)
        print(f"Created: {output_path}")


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    # 1. Create a fillable template PDF
    create_sample_template(TEMPLATE_PDF)

    # 2. Show field names so you can verify them
    show_field_names(TEMPLATE_PDF)

    # 3. Fill one sample PDF
    fill_one_pdf(TEMPLATE_PDF, SINGLE_OUTPUT_PDF)

    # 4. Fill many PDFs from CSV if data.csv exists
    fill_pdfs_from_csv(TEMPLATE_PDF, CSV_FILE, OUTPUT_FOLDER)


if __name__ == "__main__":
    main()