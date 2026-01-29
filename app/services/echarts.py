import json
from typing import Any


def generate_echarts_option(columns: list[str], rows: list[list]) -> dict[str, Any]:
    if not rows:
        return {"title": {"text": "No data"}}
    series = []
    x_axis = [row[0] for row in rows]
    values = [row[1] for row in rows] if len(columns) >= 2 else [row[0] for row in rows]
    chart_type = "bar"
    if len(values) > 10:
        chart_type = "line"
    if len(columns) == 2 and all(isinstance(v, (int, float)) for v in values):
        chart_type = "bar"
    if len(columns) == 2 and sum(values) != 0 and len(values) <= 6:
        chart_type = "pie"
    if chart_type == "pie":
        series = [{"type": "pie", "data": [{"name": x, "value": v} for x, v in zip(x_axis, values)]}]
        option = {"tooltip": {}, "series": series}
    else:
        series = [{"type": chart_type, "data": values}]
        option = {"tooltip": {}, "xAxis": {"type": "category", "data": x_axis}, "yAxis": {}, "series": series}
    return option


def wrap_echarts_markdown(option: dict[str, Any]) -> str:
    return "echarts\n" + json.dumps(option, ensure_ascii=False)


def extract_echarts_json(text: str) -> dict[str, Any]:
    if "echarts" not in text:
        return {}
    _, payload = text.split("echarts", 1)
    payload = payload.strip()
    return json.loads(payload)
