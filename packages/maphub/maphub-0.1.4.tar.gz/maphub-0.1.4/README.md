# maphub

## Usage

### Python package
This example demonstrates how to upload a Map from the local path to a MapHub project with the name `France`.
```python 
from maphub import MapHubClient

client = MapHubClient(api_key="your-api-key")
france_project = client.create_project("France")

client.upload_map(
    map_name="France Population",
    project_id=france_project['id'],
    public=False,
    path="path/to/GIS/data.gpkg"
)
```

### CLI
Coming soon...

