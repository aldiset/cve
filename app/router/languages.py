from fastapi import APIRouter, HTTPException
from googletrans import constants

router = APIRouter()

@router.get("")
async def get_languages_key(country: str = None):
    dict_languages = constants.LANGUAGES
    data = []
    for key, value in dict_languages.items():
        content = {
            'country' : value,
            'code' : key
        }
        if country is not None:
            if country == value:
                return content
        data.append(content)
    if country is not None:
        return HTTPException(status_code=404, detail="Data not Found")
    return data