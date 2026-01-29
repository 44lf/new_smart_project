from app.services import knowledge as knowledge_service


def test_knowledge_upload(client, monkeypatch):
    async def fake_upload(self, filename, content, uploader):
        return {"file_id": "file-1", "chunks": 1, "failed_chunks": 0, "elapsed_ms": 10}

    monkeypatch.setattr(knowledge_service.KnowledgeService, "upload_file", fake_upload)
    response = client.post(
        "/api/knowledge/upload",
        files={"file": ("demo.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["file_id"] == "file-1"
