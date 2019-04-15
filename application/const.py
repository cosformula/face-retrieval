import os

LIBRARY_PATH = os.environ.get('LIBRARY_PATH') or './library'
TARGETS_PATH = os.environ.get('TARGETS_PATH') or './target'
RETRIEVAL_PATH = os.environ.get('RETRIEVAL_PATH') or './retrieves'
TEMP_PATH = os.environ.get('TEMP_PATH') or './data/temp'
DB = os.environ.get('DATABASE')
PHOTO_DIRNAME = 'photos'
