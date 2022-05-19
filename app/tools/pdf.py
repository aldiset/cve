import uuid
import os
from datetime import datetime
import jinja2

from xhtml2pdf import pisa

class ConvertToPDF():
    @classmethod
    async def convert_to_pdf(self, cve_id: str, templates: str = "layout.html", data : dict = None):
        slug = uuid.uuid1().hex[:12]
        filename = f"Detail-Data-{cve_id}-{str(datetime.now().date())}_{slug}.pdf"
        if not os.path.exists('files'):
                os.makedirs('files')
        filepath = f"files/{filename}"

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'./templates')),
            autoescape=jinja2.select_autoescape()
        )

        try:
            template = env.get_template(templates)
            html = template.render(data)

            result_file = open(filepath, "w+b")
            pisa.CreatePDF(src=html,dest=result_file)
            result_file.close() 
            return filepath, filename
        except:
            return False, False
        
        