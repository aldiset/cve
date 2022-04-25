from cgitb import text
import pandas as pd
from datetime import datetime
import os
import uuid

import app.base.object as Object
from app.tools.translate import TranslateText


class WriteExcelClass():

    @classmethod
    async def write_cve_to_excel(self, data: dict, lang: str = None):
        
        slug = uuid.uuid1().hex[:12]
        filename = f"Detail-Data-{data.get('id')}-{str(datetime.now().date())}_{slug}.xlsx"
        filepath = f"files/{filename}"

        if not os.path.exists('files'):
                os.makedirs('files')
        
        #capec detail data
        capec,flow = await self.capec_data(data=data.get("capec"), lang=lang)

        #Header data
        header = [f'Report detail {data.get("id")}']
        
        #requested data
        requested = {
            'key': ['Requested date', 'Requested by'],
            'value' : [str(datetime.now().date()), data.get("requested_by")],
        }

        #detail data
        detail_data = {
            'key' : ['CVE ID','CWE ID','CVSS'],
            'value' : [data.get("id"), data.get("cwe") if data.get("cwe") is not None else "Null", data.get("cvss") if data.get("cvss") is not None else "Null"],
        }

        #cvss base score
        cvss = {
        "Saverity" : ["None","Low","Medium","High","Critical"],
        "Base Score" : ["0.0","1.0-3.9","4.0-5.9","7.0-8.9","9.0-10.0"]
        }

        try:
            with pd.ExcelWriter(path=filepath, engine="openpyxl") as writer:

                #dataframe key
                dfkey1 = pd.DataFrame(requested["key"])
                dfkey2 = pd.DataFrame(detail_data["key"])    
                
                #dataframe
                df1 = pd.DataFrame(header)
                df2 = pd.DataFrame(requested["value"])
                df3 = pd.DataFrame(detail_data["value"])
                df4 = pd.DataFrame(cvss)
                df5 = pd.DataFrame(capec)
                df6 = pd.DataFrame(flow)
                
                #write to excel
                dfkey1.to_excel(writer, sheet_name=data.get("id"), header=False, index=False, startrow=2, startcol=0)
                dfkey2.to_excel(writer, sheet_name=data.get("id"), header=False, index=False, startrow=5, startcol=0)

                df1.to_excel(writer, sheet_name=data.get("id"), header=False, index=False, startrow=0, startcol=0)
                df2.to_excel(writer, sheet_name=data.get("id"), header=False, index=False, startrow=2, startcol=1)
                df3.to_excel(writer, sheet_name=data.get("id"), header=False, index=False, startrow=5, startcol=1)
                df4.to_excel(writer, sheet_name=data.get("id"), header=True, index=False, startrow=5, startcol=9)
                df5.to_excel(writer, sheet_name=data.get("id"), header=True, index=False, startrow=11, startcol=0)
                df6.to_excel(writer, sheet_name=data.get("id"), header=True, index=False, startrow=13+len(df5), startcol=0)
                
            return filepath, filename

        except Exception as e:
            if os.path.exists(filepath):
                os.unlink(filepath)
        
    @classmethod
    async def capec_data(self, data: list, lang: str = None):
        capec_id = []
        name = []
        summary = []
        solutions = []

        step1 = []
        step2 = []
        step3 = []
        step4 = []
        step5 = []
        step6 = []
        step7 = []
        step8 = []
        
        for i in data:
            capec_id.append(i.get("id")) if i.get("id") is not None else capec_id.append("Null")
            name.append(i.get("name")) if i.get("name") is not None else name.append("Null")
            summary.append(i.get("summary")) if i.get("summary") is not None else summary.append("Null")
            solutions.append(i.get("solutions")) if i.get("solutions") is not None else solutions.append("Null")

        data_capec = {
            "CAPEC ID" : capec_id,
            "Name" : name,
            "Description" : summary,
            "solution" : solutions
        }

        step_flow = {
            "Name" : name
        }

        for id in capec_id:
            object = Object.ObjectClass
            flows_data = await object.get_execution_flow(capec_id=int(id))
            
            step1.append(await TranslateText.translate_text(lang=lang, text=flows_data.step1)) if flows_data.step1 is not None else step1.append("")
            step2.append(await TranslateText.translate_text(lang=lang, text=flows_data.step2)) if flows_data.step2 is not None else step2.append("")
            step3.append(await TranslateText.translate_text(lang=lang, text=flows_data.step3)) if flows_data.step3 is not None else step3.append("")
            step4.append(await TranslateText.translate_text(lang=lang, text=flows_data.step4)) if flows_data.step4 is not None else step4.append("")
            step5.append(await TranslateText.translate_text(lang=lang, text=flows_data.step5)) if flows_data.step5 is not None else step5.append("")
            step6.append(await TranslateText.translate_text(lang=lang, text=flows_data.step6)) if flows_data.step6 is not None else step6.append("")
            step7.append(await TranslateText.translate_text(lang=lang, text=flows_data.step7)) if flows_data.step7 is not None else step7.append("")
            step8.append(await TranslateText.translate_text(lang=lang, text=flows_data.step8)) if flows_data.step8 is not None else step8.append("")

        step_flow["STEP 1"] = step1 if step1 != [] else None
        step_flow["STEP 2"] = step2 if step2 != [] else None
        step_flow["STEP 3"] = step3 if step3 != [] else None
        step_flow["STEP 4"] = step4 if step4 != [] else None
        step_flow["STEP 5"] = step5 if step5 != [] else None
        step_flow["STEP 6"] = step6 if step6 != [] else None
        step_flow["STEP 7"] = step7 if step7 != [] else None
        step_flow["STEP 8"] = step8 if step8 != [] else None

        return data_capec, step_flow