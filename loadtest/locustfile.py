from locust import HttpUser, between, task


class APILoadTest(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def rag_query(self):
        self.client.post("/api/rag/query_score", json={"user_query": "BMI 如何计算?", "top_k": 3})

    @task(2)
    def text2sql_query(self):
        self.client.post("/api/text2sql/query", json={"query": "最近高风险患者数量"})

    @task(1)
    def health(self):
        self.client.get("/health")
