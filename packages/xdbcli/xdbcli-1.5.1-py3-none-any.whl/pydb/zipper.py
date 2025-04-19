import os
import gzip
import shutil


class Zip:
    """
    Class to compress and decompress files.
    """
    def __init__(self, filename):
        self.filename = filename

    def compress(self, output=None):
        """
        Return file with gz compress
        :param output: filename to compress data.
        """
        if output is not None:
            output_filename = output
        else:
            output_filename = f'{self.filename}.gz'

        with open(self.filename, "rb") as input_file:
            with gzip.open(output_filename, "wb") as output_file:
                shutil.copyfileobj(input_file, output_file)
        return self._get_stat(output_filename)

    def decompress(self):
        """
        Return file with gz decompress
        """
        output_filename = self.filename[:-3]

        with open(output_filename, "wb") as output_file:
            with gzip.open(self.filename, "rb") as input_file:
                shutil.copyfileobj(input_file, output_file)
        return self._get_stat(output_filename)

    def _get_stat(self, file: str):
        return {self.filename: os.stat(self.filename).st_size, file: os.stat(file).st_size}
