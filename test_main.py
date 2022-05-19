import pytest
from httpx import AsyncClient

from main import app

@pytest.mark.anyio
async def test_cve():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:9999") as ac:
        response = await ac.get("/api/vuln/cve/c")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_cwe():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:9999") as ac:
        response = await ac.get("/api/vuln/cwe/CWE-89")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_capec():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:9999") as ac:
        response = await ac.get("/api/vuln/capec/7")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_generate_file():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:9999") as ac:
        response_pdf = await ac.get("/api/vuln/generate/CVE-2022-21664/pdf")
        response_excel = await ac.get("/api/vuln/generate/CVE-2022-21664/excel")
    assert response_pdf.status_code == 200
    assert response_excel.status_code == 200