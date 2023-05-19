from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.tools.pdf import ConvertToPDF
from app.tools.remove import RemoveFile
from app.base.object import ObjectClass

router = APIRouter()

object = ObjectClass
templates = Jinja2Templates(directory="templates")

@router.get("/{cve_id}/excel", response_description='xlsx')
async def get_detail_cve_to_excel(
    background_task: BackgroundTasks,
    lang: str = "en",
    cve_id: str = None,
    requested_by: str = "Guest",
    ):

    filepath, filename = await object.get_details_cve_by_id(lang=lang,cve_id=cve_id,requested_by=requested_by, file=True)

    """Data not found"""
    if filepath == "" and filename == "":
        return HTTPException(status_code=404, detail="Data not Found")
    
    background_task.add_task(RemoveFile.remove_file,filepath)
    return FileResponse(path=filepath, media_type="application/octet-stream",filename=filename)

@router.get("/{cve_id}/pdf", response_description=".pdf")
async def get_detail_cve_to_pdf(background_task: BackgroundTasks, lang: str = "en", cve_id: str = None, requested_by: str = "guest"):
    definition = await object.get_definition_data(lang=lang)
    data, capecs = await object.get_data_to_pdf(lang=lang, cve_id=cve_id)
    if data in [""]:
        return HTTPException(status_code=404, detail="Data not Found")
        
    context={
        "first_data":{
            "requested_by": requested_by,
            "requested_date": datetime.now().date(),
            "definitions":definition
        },
        "second_data":{
            "cve": data.get("id"),
            "cwe": data.get("cwe"),
            "cvss": data.get("cvss"),
            "datas":data.get("capec") if data.get("capec") is not None else []
        },
        "three_data":{
            "capecs":capecs
        }
    }

    filepath, filename = await ConvertToPDF.convert_to_pdf(cve_id=cve_id,data=context)
    if filepath is False and filename is False:
        return HTTPException(status_code=404, detail="Data not Found")

    background_task.add_task(RemoveFile.remove_file,filepath)
    return FileResponse(path=filepath, media_type="application/pdf",filename=filename)