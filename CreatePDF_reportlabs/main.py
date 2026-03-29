from reportlab.pdfgen import canvas

c = canvas.Canvas('simple.pdf')

c.drawString(100, 750, 'What is going on!')
c.save()
