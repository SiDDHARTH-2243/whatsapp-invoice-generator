from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime

def generate_invoice(client_name: str, job_description: str, amount: str, output_path: str = "test_invoice.pdf") -> bool:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)

        pdf.set_font("helvetica", "", 12)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        pdf.cell(0, 10, f"Date: {current_date}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        pdf.ln(10)

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(40, 10, "Client:", border=0)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 10, client_name, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(40, 10, "Job Description:", border=0)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 10, job_description, border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("helvetica", "B", 12)
        pdf.cell(40, 10, "Amount:", border=0)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 10, f"{amount}", border=0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.output(output_path)
        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    print("Testing PDF Generation...")
    success = generate_invoice("Rahul", "Oil Change", "1500")
    if success:
        print("Success: 'test_invoice.pdf' generated with zero warnings.")