# ClassCodeToDiagramParser

Currently using able to parse a C# project to either Mermaid or PlantUML.


## Quickstart :
### Install requirements 
```py
pip install -r requirements.txt
```

### Config

Edit the config.json to ensure the options are what you want.
The exclude files and namespaces can be specially usefull for removing the tests functions.

The avaliable diagrams are : 
- `MermaidClassDiagram`
- `PlantUML`


The avaliable languages are : 
- `Csharp`

For more detail : take a look at `internal_config.json`

### Starting the parsing
```py
python execution.py ../path/to/project/ ./config.json
```