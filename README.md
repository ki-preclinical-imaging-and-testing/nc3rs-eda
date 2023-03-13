# nc3rsEDA
Tools for NC3Rs Experimental Design Assistant

## Usage

From the main directory, this package can be used as follows:

    In [1]: import nc3rEDA as ned

    In [2]: g = ned.Graph('model')

    In [3]: g.visualize()

    In [4]: g.export_arrows(fpath="test.arrows", indent=2)
