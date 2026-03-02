## Table Visualization for Datawrapper

### Overview

The `Table` class has been added to the Datawrapper Python library, enabling you to create and manage tabular data visualizations using the same object-oriented patterns as the existing chart implementations.

### Quick Start

```python
import pandas as pd
from datawrapper import Table

# Create sample data
df = pd.DataFrame({
    "Country": ["USA", "China", "India"],
    "Population": [331000000, 1412000000, 1380000000],
    "GDP_Trillion": [22.94, 17.73, 3.29]
})

# Create and configure a table
table = Table(
    title="Countries by Population and GDP",
    data=df,
    source_name="World Bank",
    byline="Data Team"
)

# Create the table in Datawrapper
table.create()

# Update and publish
table.title = "Updated Title"
table.update().publish()
```

### Core Features

#### 1. **Basic Table Creation**

```python
from datawrapper import Table

table = Table(
    title="Sales Data",
    data=df,  # pandas DataFrame or list of dicts
    source_name="Sales DB",
    byline="Analytics Team",
    intro="This shows quarterly sales performance",
    notes="Data updated weekly"
)
```

#### 2. **Column Ordering**

Control the display order of columns using column indices (0-based):

```python
table = Table(
    title="Reordered Table",
    data=df,
    column_order=[2, 0, 1]  # Show columns in this order
)

serialized = table.serialize_model()
# The metadata will include: column-order: [2, 0, 1]
```

#### 3. **Column Formatting**

Configure number formatting, alignment, and other column-specific settings:

```python
table = Table(
    title="Formatted Table",
    data=df,
    column_formats=[
        {
            "column": "Population",
            "type": "number",
            "number-format": "n0",  # No decimal places
            "number-divisor": 0
        },
        {
            "column": "GDP_Trillion",
            "type": "number",
            "number-format": "n2",  # 2 decimal places
            "number-prepend": "$"    # Prepend $ symbol
        },
        {
            "column": "Country",
            "type": "text"
        }
    ]
)
```

### API Operations

All standard chart operations are supported:

```python
# Create a new table
table.create()

# Update configuration
table.title = "New Title"
table.update()

# Publish to be visible to others
table.publish()

# Get an existing table by ID
existing_table = Table.get(chart_id="abc123")

# Duplicate a table
duplicated = table.duplicate()

# Fork from another table
forked = table.fork()

# Delete the table
table.delete()

# Export to various formats
png_bytes = table.export_png(zoom=2)
pdf_bytes = table.export_pdf(mode="rgb")
svg_bytes = table.export_svg(plain=True)

# Get the published URL
url = table.get_url()

# Get embed code
embed_code = table.get_embed_code()
```

### Advanced Configuration

#### Metadata Management

```python
table.language = "de-DE"  # German
table.theme = "datawrapper"
table.forkable = True  # Allow others to fork

# Publishing options
table.get_the_data = False
table.download_image = True
table.download_pdf = False
table.embed = True
```

#### Data Management

```python
# Update the data
import pandas as pd
new_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
table.data = new_data
table.update()

# Get data from API
existing_table = Table.get(chart_id="abc123")
data = existing_table.data  # Returns pandas DataFrame
```

### Serialization/Deserialization

The Table class handles conversion between Python objects and Datawrapper API format:

```python
# Serialize to API format
api_dict = table.serialize_model()
csv_data = table.serialize_data()

# Deserialize from API response
table = Table.deserialize_model(api_response)
```

### Comparison with Legacy API

| Aspect | Object-Oriented API (New) | Legacy API |
|--------|--------------------------|-----------|
| **Type Safety** | Full type hints, IDE autocomplete | String-based, minimal validation |
| **Configuration** | Pythonic, field-based | Method calls with multiple parameters |
| **Method Chaining** | Supported (`.create().update().publish()`) | Not supported |
| **Documentation** | Rich docstrings with examples | Limited |
| **Maintenance** | Modern design pattern | Deprecated |
| **Recommended** | ✅ Yes | ❌ No |

### Examples

#### Example 1: Simple Table with Formatting

```python
import pandas as pd
from datawrapper import Table

df = pd.DataFrame({
    "Product": ["Laptop", "Mouse", "Monitor"],
    "Price": [999.99, 29.99, 349.99],
    "Stock": [42, 156, 89]
})

table = Table(
    title="Product Inventory",
    data=df,
    source_name="Warehouse DB",
    byline="Inventory Team",
    column_formats=[
        {"column": "Price", "type": "number", "number-format": "n2", "number-prepend": "$"},
        {"column": "Stock", "type": "number", "number-format": "n0"}
    ]
)

table.create().publish()
print(f"Published at: {table.get_url()}")
```

#### Example 2: Reordering and Filtering Columns

```python
# Create table with custom column order
table = Table(
    title="Key Metrics",
    data=df,
    column_order=[1, 2, 0]  # Show Price, Stock, Product
)

table.create()
```

#### Example 3: Managing Existing Tables

```python
# Fetch and update an existing table
table = Table.get(chart_id="xyz789")
print(f"Current title: {table.title}")

# Update configuration
table.byline = "Updated by: New Team"
table.source_name = "New Source"
table.update()

# Publish the changes
table.publish()
```

### Error Handling

```python
try:
    table = Table.get(chart_id="invalid_id")
except Exception as e:
    print(f"Error fetching table: {e}")

try:
    table.publish()
except ValueError as e:
    # Will raise if chart_id is not set
    print(f"Cannot publish: {e}")
```

### Migration from Legacy API

**Before (Legacy API - Deprecated):**
```python
from datawrapper import Datawrapper

dw = Datawrapper(access_token="YOUR_TOKEN")
chart_id = dw.create_chart(title="My Table", chart_type="tables")
dw.add_data(chart_id=chart_id, data=df)
dw.update_chart(chart_id=chart_id, title="Updated Title")
dw.publish_chart(chart_id=chart_id)
```

**After (Object-Oriented API - Recommended):**
```python
from datawrapper import Table

table = Table(title="My Table", data=df)
table.create().update().publish()
```

### Implementation Details

#### File Structure

- **[datawrapper/charts/table.py](datawrapper/charts/table.py)** - Main Table class
  - Extends `BaseChart` for core functionality
  - Supports column ordering and formatting
  - Full serialization/deserialization support

#### Integration Points

- Inherits from `BaseChart` for common operations (create, update, publish, delete, export)
- Uses existing serializer patterns (e.g., `ColumnFormat` model)
- Follows Pydantic v2 patterns with aliasing for API field names
- Supports method chaining and fluent interfaces

#### API Compatibility

The implementation follows Datawrapper API v3 specification:
- Chart type: `"tables"`
- Metadata structure: Same as other visualizations (data, describe, visualize, publish, annotate)
- Column configuration through `column-order` and `column-format` fields

### Testing

Comprehensive tests are included in [tests/unit/models/charts/test_table.py](tests/unit/models/charts/test_table.py) covering:

- ✅ Basic table creation
- ✅ Column ordering
- ✅ Column formatting
- ✅ Serialization/deserialization
- ✅ Data conversion (CSV)
- ✅ Method chaining
- ✅ Empty data handling

All tests pass successfully.

### Future Enhancements

Possible future additions:
- Built-in table sorting configuration
- Conditional formatting options
- Column filtering/hiding UI configuration
- Search/filter options for interactive tables
- Pagination settings

### Support and Questions

For issues or questions:
1. Review the [Datawrapper API documentation](https://developer.datawrapper.de/)
2. Check the inline docstrings in [table.py](datawrapper/charts/table.py)
3. Review the test examples in [test_table.py](tests/unit/models/charts/test_table.py)
4. See the `.clinerules` file for API guidelines and patterns
