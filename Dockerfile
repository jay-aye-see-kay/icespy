# Use the official uv image with Debian base
FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:debian

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DJANGO_SETTINGS_MODULE=icespy.settings \
    PYTHONPATH=/app

# Install system dependencies and setup in one layer
RUN groupadd -r django && useradd -r -g django django

# Set working directory
WORKDIR /app

# Copy dependency files and install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy application code and setup
COPY . .
RUN chmod +x docker-entrypoint.sh && \
    mkdir -p /app/data /app/static /app/media && \
    chown -R django:django /app

# Change to non-root user
USER django

# Create volume for SQLite database and media files
VOLUME ["/app/data"]

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Set entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]

# Use gunicorn for production
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "30", "icespy.wsgi:application"]
