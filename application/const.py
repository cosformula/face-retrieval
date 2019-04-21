import os

LIBRARY_PATH = os.environ.get('LIBRARY_PATH') or '/data/library'
# TARGETS_PATH = os.environ.get('TARGETS_PATH') or './target'
# RETRIEVAL_PATH = os.environ.get('RETRIEVAL_PATH') or './retrieves'
TEMP_PATH = os.environ.get('TEMP_PATH') or '/data/temp'
DB = os.environ.get('DATABASE') or 'postgresext://postgres:postgres@postgres:5432/postgres'
# DB = os.environ.get('DATABASE') or 'postgresext+pool://postgres:postgres@postgres:5432/postgres?max_connections=100'
PHOTO_DIRNAME = 'photos'
