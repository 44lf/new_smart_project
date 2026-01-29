from app.services import text2sql as text2sql_service


def test_text2sql_query(client, monkeypatch):
    async def fake_query(self, question):
        return {"sql": "SELECT 1", "columns": ["1"], "rows": [[1]]}

    monkeypatch.setattr(text2sql_service.Text2SQLService, "query", fake_query)
    response = client.post("/api/text2sql/query", json={"query": "count"})
    assert response.status_code == 200
    assert response.json()["sql"].lower().startswith("select")

