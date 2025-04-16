# socketnest-python
SocketNest Server Python Library

## Installation

```bash
pip install socketnest
# or with poetry
poetry add socketnest
```

## Usage

```python
from socketnest import Socketnest

client = Socketnest(app_id="your_app_id", secret="your_secret")
response = client.trigger(
    channel="test", event="test", data={"message": "Hello, SocketNest!"}
)
print(response.json())
```
