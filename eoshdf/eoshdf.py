"""
Copyright (C) 2015--2016 Jussi Leinonen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import numpy as np
from pyhdf import SD, HDF, VS


class EOSHDF(object):
    """
    Reader for HDF4 files, specifically those created by the NASA EOS data 
    systems.

    Usage instructions:

    To open a file, initialize an EOSHDF object, passing a file name to the
    constructor. For example:
    import eoshdf
    eos = eoshdf.EOSHDF("example.hdf")

    To list the available datasets, use the list_datasets method:
    eos.list_datasets()

    To read a dataset, use the read_data method, passing the dataset name:
    data = eos.read_data("example_dataset")

    NOTE: No conversion factors or missing value masking are applied to read
    data. If you need these, you must apply them manually.
    """

    def __init__(self, file_name):
        self._file_name = file_name
        self._hdf = None
        self._vs = None
        self._sd = None


    def __del__(self):
        self._close_all()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self._close_all()


    def _close_all(self):
        if self._vs is not None:
            self._vs.end()
            self._vs = None
            self._hdf.close()
            self._hdf = None
        if self._sd is not None:
            self._sd.end()
            self._sd = None


    def _open_vs(self):
        if self._vs is None:
            self._hdf = HDF.HDF(self._file_name)
            self._vs = self._hdf.vstart()
        return self._vs


    def _open_sd(self):
        if self._sd is None:
            self._sd = SD.SD(self._file_name)
        return self._sd


    def list_datasets(self):
        """
        Lists all available datasets. If you need to distinguish between
        the VS and SD interfaces, use the list_VS_datasets and 
        list_SD_datasets methods.

        Returns:
            A list of the available datasets.

            This method might list some spurious datasets. In that case, refer to 
            the data documentation to find which dataset to read.
        """

        vs_datasets = [v[0] for v in self.list_VS_datasets()]
        sd_datasets = list(self.list_SD_datasets().keys())
        return list(sorted(vs_datasets + sd_datasets))


    def read_data(self, ds_name, dtype=np.float64):
        """
        Reads a dataset. If you need to distinguish between
        the VS and SD interfaces, use the read_VS_data and 
        read_SD_data methods.

        Args:
            ds_name: The dataset name.
            dtype: The datatype for the returned array.

        Returns:
            A numpy array containing the data.

            NOTE: No conversion factors or missing value masking are applied.
            If you need these, you must apply them manually.
        """
        try:
            data = self.read_SD_data(ds_name, dtype=dtype)
        except HDF.HDF4Error:
            try:
                data = self.read_VS_data(ds_name, dtype=dtype)
            except HDF.HDF4Error:
                raise IOError("Nonexistent data set.")
        return data


    def read_VS_data(self, ds_name, dtype=np.float64):
        vs = self._open_vs()
        vd = vs.attach(ds_name)
        arr = np.array(vd[:], dtype=dtype).ravel()
        vd.detach()
        return arr


    def list_VS_datasets(self):
        vs = self._open_vs()
        return vs.vdatainfo()


    def read_SD_data(self, ds_name, dtype=np.float64):
        sd = self._open_sd()
        sds = sd.select(ds_name)
        arr = np.array(sds[:], dtype=dtype)
        sds.endaccess()
        return arr


    def list_SD_datasets(self):
        sd = self._open_sd()
        return sd.datasets()


    def read_1D_data(self, var_name, dtype=np.float64):
        return self.read_VS_data(var_name, dtype=dtype)


    def read_2D_data(self, var_name, dtype=np.float64):
        return self.read_SD_data(var_name, dtype=dtype)
