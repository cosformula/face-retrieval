import uuid
import os
import re
import io
import mimetypes


class ImageStore(object):

    _CHUNK_SIZE_BYTES = 4096
    _IMAGE_NAME_PATTERN = re.compile(
        '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.[a-z]{2,4}$'
    )

    def __init__(self, storage_path, uuidgen=uuid.uuid4, fopen=io.open):
        self._storage_path = storage_path
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, path, image_stream, image_content_type):
        ext = mimetypes.guess_extension(image_content_type)
        name = '{uuid}{ext}'.format(uuid=self._uuidgen(), ext=ext)
        image_path = os.path.join(self._storage_path, path, name)

        with self._fopen(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        return name

    def open(self, path):
        # Always validate untrusted input!
        # if not self._IMAGE_NAME_PATTERN.match(name):
        #     raise IOError('File not found')
        image_path = os.path.join(self._storage_path, path)
        # image_path = os.path.join(self._storage_path, library, 'photos', name)
        stream = self._fopen(image_path, 'rb')
        stream_len = os.path.getsize(image_path)

        return stream, stream_len
