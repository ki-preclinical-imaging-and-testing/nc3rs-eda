# nc3rsEDA
Tools for NC3Rs Experimental Design Assistant (EDA).

## Python

From the main directory, use the package as follows:

    In [1]: import nc3rEDA as ned

    In [2]: g = ned.Graph('model')

    In [3]: g.visualize()

    In [4]: g.export_arrows(fpath="test.arrows", indent=2)

This will load any NC3Rs EDA file that comes in a custom JSON structure. The example works with the included template EDA file named `model`. We can visualize the graph (poorly, but as a good test) using `Graph.visualize()`, and we can export to an Arrows.app using `Graph.export_arrows`.

## Arrows.app

Once the Arrows.app file is generated, it can be loaded directly into Arrows.app using the import function. From there, generate the Cypher and run in Neo4j browser.

## Next steps

Ideally, unnecessary manual steps will be automated. This means...

- Generate Cypher directly from this script
- Watch and automatically load files placed in a folder
- Test for assumptions identified in notebook
    - From EDA to Python (e.g. test number of childShapes vs total nodes and edges)
    - From Python to Neo4j (e.g. test query on the database against the known entities in the Python script)
- Add versioning of EDA 
- Attach to other info from imaging studies via common nodes

These can be tracked in the repository's Issues, but writing here since it's still in an early stage of development.
