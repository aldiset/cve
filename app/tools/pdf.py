import uuid
import os
from datetime import datetime
import jinja2
from PyPDF2 import PdfFileMerger
from xhtml2pdf import pisa


class ConvertToPDF():
    @classmethod
    async def convert_to_pdf(self, cve_id: str, templates: str = "layout.html", data : dict = None):
        filepdf = []

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'./templates')),
            autoescape=jinja2.select_autoescape()
        )

        try:

            first_page = env.get_template("first_page.html")
            second_page = env.get_template("second_page.html")
            three_page = env.get_template("three_page.html")

            first = first_page.render(data.get("first_data"))
            second = second_page.render(data.get("second_data"))
            three = three_page.render(data.get("three_data"))

            if first:
                first_name = self.filename()
                filepath = f"files/{first_name}"
                result_file = open(filepath, "w+b")
                pisa.CreatePDF(src=first,dest=result_file)
                result_file.close()
                filepdf.append(filepath)
            if second:
                second_name = self.filename()
                filepath = f"files/{second_name}"
                result_file = open(filepath, "w+b")
                pisa.CreatePDF(src=second,dest=result_file)
                result_file.close()
                filepdf.append(filepath)
            if three:
                three_name = self.filename()
                filepath = f"files/{three_name}"
                result_file = open(filepath, "w+b")
                pisa.CreatePDF(src=three,dest=result_file)
                result_file.close()
                filepdf.append(filepath)
            
            filename = self.filename(cve_id=cve_id)
            filepath = f"files/{filename}"
            

            merger = PdfFileMerger()

            for pdf in filepdf:
                merger.append(pdf)
            merger.write(filepath)
            merger.close()
            return filepath, filename

        except:
            return False, False
    
    @classmethod
    def filename(self, cve_id: str = "null"):
        slug = uuid.uuid1().hex[:12]
        filename = f"Detail-Data-{cve_id}-{str(datetime.now().date())}_{slug}.pdf"
        if not os.path.exists('files'):
                os.makedirs('files')
        return filename
        
        