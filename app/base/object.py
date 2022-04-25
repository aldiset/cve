from sqlalchemy import and_
from fastapi.encoders import jsonable_encoder

from app.services.circl import CirlLu
from app.services.opencve import OpenCve
from app.tools.excel import WriteExcelClass
from app.database import session_manager
from app.base.crud import CRUDCAPEC, CRUDDefinition
from app.models.capec import ExecuteFlow
from app.models.definition import Definition
from app.tools.translate import TranslateText

class ObjectClass():
    @classmethod
    async def get_details_cve_by_id(self,lang: str = None, cve_id: str = None, requested_by: str = None, file: bool = False):
        try:
            status, data = await CirlLu.get_cve_detail(lang=lang,cve_id=cve_id)
            if status is True:
                data["requested_by"] = requested_by

                if file is True:
                    filepath, filename = await WriteExcelClass.write_cve_to_excel(data=data, lang=lang)
                    return filepath, filename
                
                data = {
                    "cve_id": data.get("id"),
                    "cwe_id": data.get("cwe"),
                    "cvss_score": data.get("cvss"),
                    "capec": data.get("capec"),
                    "description": data.get("description")
                }
                return True, data

        except:
            return False,""
    
    @classmethod
    async def get_details_cwe_by_id(self,lang: str = None, cwe_id: str = None):
        try:
            status, data = await OpenCve.get_cwe_detail(cwe_id=cwe_id, lang=lang)
            data = {
                "cwe_id": data.get("id"),
                "name": data.get("name"),
                "description": data.get("description")
            }
            return status, data
        except:
            return False, {}
    
    @classmethod
    async def get_execution_flow(self, capec_id: int = None):
        filters = [and_(ExecuteFlow.deleted_date.__eq__(None))]
        if capec_id is not None:
            filters.append(and_(ExecuteFlow.capec_id.__eq__(capec_id)))
        with session_manager() as db:
            datas = CRUDCAPEC.get_by_id(db=db, filters=filters)

        return datas
    
    @classmethod
    async def get_definition_data(self, lang: str, id: int = None):
        filters = [and_(Definition.deleted_date.__eq__(None))]
        if id is not None:
            filters.append(and_(Definition.id.__eq__(id)))
        with session_manager() as db:
            datas = await CRUDDefinition.get_data(db=db, filters=filters)
            for data in datas:
                data.value = await TranslateText.translate_text(lang=lang, text=data.value)


        return datas
    
    @classmethod
    async def get_data_to_pdf(self, lang: str = "en", cve_id: str = None):
        try:
            capecs = []
            status, data = await CirlLu.get_cve_detail(lang=lang,cve_id=cve_id)
            if status is True:
                capec_list = data.get("capec") if data.get("capec") is not None else []
                if capec_list != []:
                    for c in capec_list:
                        capec_data = await self.get_execution_flow(capec_id=c.get("id"))
                        capecs.append(jsonable_encoder(capec_data))
            
            #translate
            if lang != "en" and capecs != []:
                for capec in capecs:
                    for key, value in capec.items():
                        if key != "id" or key != "capec_id" or key != "created_date" or key != "updated_date" or key!= "deleted_date":
                            capec[key] = await TranslateText.translate_text(lang=lang, text=value)

            return data, capecs

        except:
            return "",""
    
    @classmethod
    async def get_capec_by_id(self, filters, lang: str = None):
        with session_manager() as db:
            data = await CRUDCAPEC.get_capec_by_id(db=db, filters=filters)
            if data is not False:
                return True, data
            else:
                return data, {}