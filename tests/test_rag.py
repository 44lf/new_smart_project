from app.services import rag as rag_service


def test_rag_query_score(client, monkeypatch):
    async def fake_query(self, user_query, top_k, filters):
        return {
            "user_query": user_query,
            "score_result": {
                "total_score": 3,
                "nutritional_impairment_score": 1,
                "disease_severity_score": 1,
                "age_score": 1,
                "risk_level": "high",
                "recommendations": "demo",
                "assessment_basis": "demo",
            },
            "source_basis": [
                {
                    "chunk_id": "c1",
                    "file_id": "f1",
                    "snippet": "demo",
                    "score": 0.9,
                    "reason": "test",
                }
            ],
        }

    monkeypatch.setattr(rag_service.RagService, "query_score", fake_query)
    response = client.post("/api/rag/query_score", json={"user_query": "test", "top_k": 3})
    assert response.status_code == 200
    assert response.json()["score_result"]["total_score"] == 3
