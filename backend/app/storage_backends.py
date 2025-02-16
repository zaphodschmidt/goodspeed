from django.db import models

from storages.backends.s3 import S3File
from storages.backends.s3boto3 import S3Boto3Storage


class ImageStorage(S3Boto3Storage):
    location = "images"