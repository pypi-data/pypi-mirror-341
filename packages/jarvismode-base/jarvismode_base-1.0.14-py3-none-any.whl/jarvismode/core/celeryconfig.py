# celeryconfig.py
import os

jarvismode_redis_host = os.environ.get("JARVISMODE_REDIS_HOST")
jarvismode_redis_port = os.environ.get("JARVISMODE_REDIS_PORT")
# broker default user

if jarvismode_redis_host and jarvismode_redis_port:
    broker_url = f"redis://{jarvismode_redis_host}:{jarvismode_redis_port}/0"
    result_backend = f"redis://{jarvismode_redis_host}:{jarvismode_redis_port}/0"
else:
    # RabbitMQ
    mq_user = os.environ.get("RABBITMQ_DEFAULT_USER", "jarvismode")
    mq_password = os.environ.get("RABBITMQ_DEFAULT_PASS", "jarvismode")
    broker_url = os.environ.get("BROKER_URL", f"amqp://{mq_user}:{mq_password}@localhost:5672//")
    result_backend = os.environ.get("RESULT_BACKEND", "redis://localhost:6379/0")
# tasks should be json or pickle
accept_content = ["json", "pickle"]
