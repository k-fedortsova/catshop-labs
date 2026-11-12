FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
RUN useradd --system --uid 10001 --no-create-home appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data
COPY --from=builder /opt/venv /opt/venv
COPY app.py .
ENV PATH="/opt/venv/bin:$PATH"
ENV PORT=8080
USER 10001:10001
EXPOSE 8080
CMD ["python", "app.py"]
