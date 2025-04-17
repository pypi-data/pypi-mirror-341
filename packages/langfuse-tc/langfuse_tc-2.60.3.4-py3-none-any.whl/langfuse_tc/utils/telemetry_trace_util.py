from opentelemetry import trace

# 获取 Tracer 实例
tracer = trace.get_tracer(__name__)

# 在某个函数或代码块中获取 Trace ID
def get_current_trace_id():
    # 获取当前的 Span
    current_span = trace.get_current_span()

    # 检查 Span 是否有效
    if current_span is None or not current_span.is_recording():
        return None

    # 获取 Span 的上下文
    span_context = current_span.get_span_context()

    # 检查 Trace ID 是否有效
    if span_context.trace_id == 0:
        return None

    # 返回 Trace ID（以十六进制格式）
    t_id = trace.format_trace_id(span_context.trace_id)
    print(f"Current Trace ID: {t_id}")
    return t_id
# 示例调用
if __name__ == "__main__":
    with tracer.start_as_current_span("get-trace-span"):
        trace_id = get_current_trace_id()
        print(f"Current Trace ID: {trace_id}")