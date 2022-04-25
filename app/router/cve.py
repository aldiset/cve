from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.base.object import ObjectClass
router = APIRouter()

@router.get("/{cve_id}")
async def get_detail_cve(
    lang: Optional[str] = Query(default="en",max_length=5),
    cve_id: str = None):

    object = ObjectClass()
    status, data = await object.get_details_cve_by_id(lang=lang,cve_id=cve_id)

    """Data not found"""
    if data == {} or status == False:
        return HTTPException(status_code=404, detail="Data not Found")
    
    """Response"""
    response = {
        "message": "success",
        "status": True,
        "data": data
    }
    return response