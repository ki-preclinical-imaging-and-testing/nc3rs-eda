# nc3rsEDA
Tools for NC3Rs Experimental Design Assistant (EDA).

## Python

From the main directory, use the package as follows:

    In [ ]: import nc3rEDA as ned

    In [ ]: g = ned.Graph('model')

    In [ ]: g.visualize()

    In [ ]: g.export_neo4j_create()

This will load any NC3Rs EDA file that comes in a custom JSON structure. 
The example works with the included template EDA file named `model`. 
`Graph.visualize()` produces a quick and dirty visualizion. 
`Graph.export_neo4j_create() exports to a Cypher CREATE query for direct
loading into a Neo4j database. 
This exports JSON for Neo4j's Arrows.app whiteboarding tool.

## Cypher for Neo4j

Output collected from `Graph.export_neo4j_create()` can be directly loaded into
Neo4j Browser. 

In the next iteration, this will be modified to use the Neo4j
Python API so that I can directly load into a database from the Python script.

## Arrows.app

Generate JSON for import into Arrows.app using

    In [ ]: g.export_arrows()

Once the Arrows.app file is generated, it can be loaded directly into Arrows.app using the import function. From there, generate the Cypher and run in Neo4j browser.

## Next steps

Ideally, unnecessary manual steps will be automated. This means...

- Watch and automatically load files placed in a folder
- Test for assumptions identified in notebook
    - From EDA to Python (e.g. test number of childShapes vs total nodes and edges)
    - From Python to Neo4j (e.g. test query on the database against the known entities in the Python script)
- Add versioning of EDA 
- Attach to other info from imaging studies via common nodes

These can be tracked in the repository's Issues, but writing here since it's still in an early stage of development.
