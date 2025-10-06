from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from elasticsearch import Elasticsearch
import logging.config
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger
from typing import Any, Dict
import os

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['service'] = 'bioverse-api'

def setup_logging():
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': CustomJsonFormatter,
                'format': '%(timestamp)s %(level)s %(name)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': 'ext://sys.stdout'
            },
            'elasticsearch': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/app.log',
                'maxBytes': 1024 * 1024,  # 1MB
                'backupCount': 5,
                'formatter': 'json'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'elasticsearch'],
                'level': 'INFO'
            }
        }
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)

def setup_monitoring(app):
    # Set up Prometheus metrics
    Instrumentator().instrument(app).expose(app)
    
    # Set up OpenTelemetry tracing
    trace.set_tracer_provider(TracerProvider())
    
    # Configure OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4317",  # Jaeger OTLP gRPC endpoint
        insecure=True
    )
    
    # Add BatchSpanProcessor to the tracer provider
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )

def setup_elasticsearch():
    # Configure Elasticsearch client
    es_client = Elasticsearch(
        hosts=[{'host': 'elasticsearch', 'port': 9200}],
        basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD', 'changeme'))
    )
    return es_client

# Create index template for logs
def create_log_index_template(es_client):
    template_name = "bioverse-logs"
    template_body = {
        "index_patterns": ["bioverse-logs-*"],
        "template": {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "level": {"type": "keyword"},
                    "service": {"type": "keyword"},
                    "message": {"type": "text"},
                    "logger": {"type": "keyword"},
                    "path": {"type": "keyword"}
                }
            }
        }
    }
    
    es_client.indices.put_index_template(name=template_name, body=template_body)