# EOSHDF

This is a simple reader for HDF4, particularly NASA's EOS HDF4, files. It makes data access easy without the technicalities of the PyHDF library.

## Example

Open a file (in this case, "example.hdf"):

    from eoshdf import EOSHDF
    with EOSHDF("example.hdf") as eos:
        ...

The `with` syntax is not mandatory, so you can do this instead of the above:

    eos = EOSHDF("example.hdf")

To list datasets in the opened file:

    eos.list_datasets()

To read a dataset "example":

    data = eos.read_data("example")

The above defaults to returning 64-bit floating point values. To read it as integers instead:

    data = eos.read_data("example", dtype=int)

## Warning

Some EOS HDF4 file specifications define conversion factors and missing values for datasets. These are *not* automatically applied. If you need to use these, refer to the dataset documentation and do it manually.
