FROM postgres:18-alpine

# Optional: custom config
COPY config/postgres.conf /etc/postgresql/postgresql.conf

# Ensure Postgres uses the custom config (if provided)
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
