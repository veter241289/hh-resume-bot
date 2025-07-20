from fpdf import FPDF

def create_beautiful_pdf(resumes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    # Логотип
    try:
        pdf.image("assets/logo.png", x=10, y=10, w=30)
    except:
        pass

    pdf.cell(0, 10, txt="АНКЕТЫ С HH.RU", ln=1, align='C')
    pdf.ln(10)

    for resume in resumes:
        pdf.set_fill_color(200, 230, 255)
        pdf.cell(0, 10, txt=f"👤 {resume['name']}", ln=1, fill=True)
        pdf.cell(0, 10, txt=f"🔗 {resume['link']}", ln=2)
        pdf.ln(5)

    filename = "new_resumes.pdf"
    pdf.output(filename)
    return open(filename, "rb")