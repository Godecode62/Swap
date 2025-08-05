# from storages.backends.s3 import S3Storage

# class MediaFilesStorage(S3Storage):
#     location = 'media'

from storages.backends.s3boto3 import S3Boto3Storage


class MediaFilesStorage(S3Boto3Storage):
    location = 'media'