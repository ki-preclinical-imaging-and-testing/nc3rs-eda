# nc3rsEDA
Tools for NC3Rs Experimental Design Assistant (EDA).

## Python

From the main directory, use the package as follows:

    In [ ]: import nc3rsEDA as ned

    In [ ]: g = ned.Graph('model')

    In [ ]: g.visualize()

    In [ ]: neoned = ned.Neo4jWriter(g)
    
    In [ ]: neoned.write()

        labels-added               23
        relationships-created      24
        nodes-created              23
        properties-set             93

This will load any NC3Rs EDA file using the EDA's custom JSON.
The example works with the included template EDA file named `model`. 
`Graph.visualize()` produces a quick and dirty visualizion. 
loading into a Neo4j database. 
`ned.Neo4jWriter(g) provides a writer object to handle Cypher `CREATE` and `DETACH DELETE (n)` queries directly on a specified database. 
`Graph.export_neo4j_create() exports to a Cypher CREATE query for direct
`Graph.export_arrows() exports JSON for Neo4j's Arrows.app whiteboarding tool.

## Writing to Neo4j Database

When an accessible database address and authentication are provided, the
ned.Neo4jWriter object can write directly to the database, handling all of the
proper open and close commands that Neo4j's Python Driver requires.

This results in the ability to pipe new models to the database using the
following lines and the appropriate filename:

    import nc3rsEDA 
    g = ned.Graph('model')
    neoned = ned.Neo4jWriter(g, uri='neo4j://localhost:7687', auth=("user","pass"))
    neoned.write()

Additionally, the Neo4jWriter tests the initial connection and will throw an
error if the database is unavailable. It can also be used to delete all nodes
and relationships (but due to limitations in Neo4j functionality, cannot clear
things like property keys or indexes).

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
