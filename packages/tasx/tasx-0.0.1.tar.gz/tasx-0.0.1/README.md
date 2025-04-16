# TASX Client SDK

## Installation

```
pip install tasx
```

## Getting Started

Import the TASX library and initialize the client:

```python
import tasx

client = tasx.get_client(
    api_base="tasx.tiptreesystems.com/api/v1",
    api_key="your_api_key_here"
)
```

Note: The API base and key can also be set via environment variables.

## Task Management

### Creating a new task

```python
task = client.create_task(
    title="My New Task",
    description="This is a test task",
    status="pending"
)
```

### Retrieving a task

```python
task = client.get_task(task_id)
```

### Updating a task

```python
updated_task = client.update_task(
    task_id,
    status="in_progress"
)
```

### Deleting a task

```python
client.delete_task(task_id)
```

## Search Functionality

```python
import tasx.enums

import tasx.interface_models

search_results = client.search_tasks(
    query="test",
    limit=10,
    sort_by=tasx.SortBy.CREATED_AT,
    sort_order=tasx.enums.SortOrder.DESC
)

for task in search_results.items:
    print(f"Task: {task.name}, Status: {task.status}")
```

## Error Handling

```python
from tasx.exceptions import TasxAPIError, TaskNotFoundError

try:
    task = client.get_task(task_id)
except TaskNotFoundError:
    print(f"Task {task_id} not found")
except TasxAPIError as e:
    print(f"API error occurred: {e}")
```

## Asynchronous Support

TASX also supports asynchronous operations:

```python
import asyncio
import tasx


async def main():
    async_client = await tasx.get_async_client(
        api_base="tasx.tiptreesystems.com/api/v1",
        api_key="your_api_key_here"
    )

    task = await async_client.create_task(
        title="Async Task",
        description="This is an asynchronous task"
    )

    search_results = await async_client.search_tasks(query="async")
    for task in search_results.items:
        print(f"Found task: {task.name}")


if __name__ == "__main__":
    asyncio.run(main())
```

For more detailed documentation, please refer to the [TASX API Documentation](https://docs.tasx.tiptreesystems.com).