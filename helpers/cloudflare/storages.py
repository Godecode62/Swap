from storages.backends.s3 import S3Storage

class MediaFilesStorage(S3Storage):
    location = 'media'