from django.conf import settings
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts=[{
    'host': settings.ELASTICSEARCH_URL,
    'port': settings.ELASTICSEARCH_PORT,
}], use_ssl=settings.ELASTICSEARCH_PORT in [443], verify_certs=False)
