from fastapi import APIRouter, Query, HTTPException
from sqlalchemy import and_

from app.models.capec import Capec
from app.base.object import ObjectClass
router = APIRouter()

@router.get("/{capec_id}")
async def get_detail_capec(capec_id: int, lang: str = "en"):
    if capec_id is None:
        return HTTPException(status_code=404, detail="please check your capec id")
    filters = [and_(Capec.deleted_date.__eq__(None),(Capec.id.__eq__(capec_id)))]
    status, data = await ObjectClass().get_capec_by_id(filters, lang=lang)
    if status is False:
        return HTTPException(status_code=404, detail="Data not found")
    
    response = {
        "message":"success",
        "status": True,
        "data":data
    }
    return response