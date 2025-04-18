# FWSDK - FactWeavers Python SDK

**FWSDK** is a Python SDK that enables easy interaction with the FactWeavers platform. It supports operations like listing entities, creating silver and gold entities, deleting entities, and managing their schedules — all via Python.

---

## 📦 Installation

Install via pip (after publishing to PyPI):

```bash
pip install fdc_sdk
```

Or install locally for development:

```bash
pip install .
```

---

## 🚀 Quick Start

```python
from fdc_sdk import FWClient

# Initialize the client
client = FWClient(
    base_url="https://dev.factweavers.com",
    org="1",
    secret_key="your_secret_token_here"
)

# List all bronze entities
entities = client.list_all_entities(layer="bronze")
print(entities)

# Create a silver entity
client.create_silver_entity(
    entity_name="Landmark_combined",
    sql_query="""
        SELECT a, b, c FROM Landmark_raw_nav
        UNION
        SELECT a, b, c FROM Landmark_raw_bc
    """
)

# Create a gold entity
client.create_gold_entity(
    entity_name="Landmark_gold_summary",
    sql_query="SELECT * FROM Landmark_combined WHERE region = 'US'"
)

# Delete an entity
client.delete_entity("Landmark_gold_summary")

# Disable schedule for an entity
client.disable_schedule("Landmark_combined")
```

---

## 📚 API Methods

### `FWClient(base_url, org, secret_key)`
Creates a client to interact with the FactWeavers backend.

---

### `list_all_entities(layer="BRONZE", q="", sort_by="updated_at", sort_order="asc")`
Fetch all entities from a specific layer. Internally fetches the total count and retrieves paginated results.

---

### `create_silver_entity(entity_name, sql_query)`
Create a new silver entity by passing the entity name and SQL query.

---

### `create_gold_entity(entity_name, sql_query)`
Create a new gold entity with the specified SQL logic.

---

### `delete_entity(entity_name)`
Delete an existing entity using its name.

---

### `disable_schedule(entity_name)`
Disable the schedule for a specific entity.

---

## 🔐 Authentication

Your `secret_key` must be valid and authorized for the target organization. All requests use the format:

```
Authorization: Bearer <secret_key>
X-Organization: <org>
```

---

## 🧪 Testing

Use a sample script like the following to test locally:

```python
from fdc_sdk import FWClient

client = FWClient("https://dev.factweavers.com", "1", "your_token")
print(client.list_all_entities("bronze"))
```

---

## 🤝 Contributions

We welcome contributions! Please fork the repo and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License © 2025 FactWeavers
