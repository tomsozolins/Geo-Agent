from loguru import logger
from minio import Minio


class MinioApi(Minio):

    def get_minio_images(self):
        minio_dict = {}
        try:
            logger.info('Minio API - getting dictionary of images')
            minio_objects = self.list_objects('photos')
            for img in minio_objects:
                minio_dict.update({img.object_name.split(
                    '.')[0]: img.object_name.split('.')[1]})
            return minio_dict
        except Exception as e:
            logger.exception(
                f'Minio API - failed to get dictionary of images - {e}')
