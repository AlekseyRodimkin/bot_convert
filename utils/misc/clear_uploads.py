import os
import shutil
import stat
from config_data.config import uploads_path
from loguru import logger


def main(user_id):
    """Удаляет папку uploads/<user_id>"""
    logger.debug(f'clear_uploads({user_id})')
    path = os.path.join(uploads_path, str(user_id))

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):

            for dir_name in dirs:
                os.chmod(os.path.join(root, dir_name), stat.S_IWRITE)

            for file_name in files:
                os.chmod(os.path.join(root, file_name), stat.S_IWRITE)

        shutil.rmtree(path)
