from fastapi import APIRouter
from app.router import cve, cwe, languages, generate, capec

router = APIRouter()

router.include_router(router=cve.router, tags=["CVE"], prefix="/cve")
router.include_router(router=cwe.router, tags=["CWE"], prefix="/cwe")
router.include_router(router=languages.router, tags=["Languages"], prefix="/languages")
router.include_router(router=generate.router, tags=["Generate"], prefix="/generate")
router.include_router(router=capec.router, tags=["CAPEC"], prefix="/capec")