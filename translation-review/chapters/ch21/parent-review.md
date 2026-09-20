# 父任务复核

本行全角链接括号使解析器误把整句中文当作 URL。为完成中文校正，单独修复为 Markdown 链接语法，保持原来的可见目标地址 https://research.swtch.com/deps 不变。明确记录解析链接字段的唯一差异，不把它混作未声明的润色。

恢复 import versus reimplement 的比较关系，以及 more often than not 的频率含义；没有读取、改写或更新外部文章内容。

原子代理清单保存在 `subagent-edits.json`。当前结果以全书校验器 `tools/book_review.py` 为准。
