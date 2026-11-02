"""Streamlit UI regression for issues found by the simulated black-box review."""
import os
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
os.environ.pop("RETAIL_ENABLE_MODEL", None)
at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
at.run()

button_labels = [button.label for button in at.button]
assert "检索知识依据" in button_labels
assert "检索知识并回答" not in button_labels

at.text_input[0].set_value("帮我看看26到35岁女性在这个年龄段里贡献了多少消费？")
at.button[0].click().run()
metric_labels = {metric.label: metric.value for metric in at.metric}
assert metric_labels["占该年龄段消费额"] == "21.80%"

compare_at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
compare_at.run()
compare_at.selectbox[6].set_value("用户规模").run()
info_values = [str(item.value) for item in compare_at.info]
assert any("当前比较：全体14个年龄×性别客群 · 用户规模" in value for value in info_values)

print("PASS: denominator phrase, public RAG label and comparison focus UI regressions passed.")
