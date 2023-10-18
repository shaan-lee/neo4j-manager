# Doing what?
- this repository does managing neo4j cypher query to use easy

# How to use?
- you can use easy like below code
### usecase
```
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        add_node(
            driver, node_values={"table": "manager", "values": {"name": "wrapr"}}
        )
    
        get_node(
            driver, node_values=   {"table": "manager", "values": {"name": "wrapr"}}
        )

        set_relationship(
            driver,
            from_node_values={"table": "User", "values": {"name": "shaan"}},
            to_node_values={"table": "User", "values": {"name": "lee"}},
            relationship="is_same_people"
        )
```
### Return value
- EagerResult