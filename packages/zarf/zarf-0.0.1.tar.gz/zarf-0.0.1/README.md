# Python Dependency Container

A lightweight, flexible dependency injection container for Python with strict typing support.

## Installation

```bash
pip install zarf
```

## Features

- **Simple API** - Just four main methods: `register`, `resolve`, `can_resolve`, and `unregister`
- **Type-Safe** - Full type hints for modern Python development
- **Flexible Registration** - Register types, instances, or factory functions
- **Named Services** - Support for multiple implementations of the same interface
- **Zero Dependencies** - Pure Python implementation with no external dependencies

## Basic Usage

```python
from zarf import Container

# Create the container
container = Container()

# Register a concrete class
container.register(UserService)

# Register with a factory function
container.register(DatabaseService, lambda: DatabaseService("connection_string"))

# Register a specific instance
logger = ConsoleLogger()
container.register(ILogger, logger)

# Register with a name
container.register(ILogger, FileLogger("app.log"), "file_logger")

# Resolve services
user_service = container.resolve(UserService)
db = container.resolve(DatabaseService)
logger = container.resolve(ILogger)
file_logger = container.resolve(ILogger, "file_logger")

# Check if services exist
if container.can_resolve(CacheService):
    cache = container.resolve(CacheService)

# Remove a service
container.unregister(ILogger, "file_logger")
```

## Detailed Examples

### Registering Services

The container supports multiple registration patterns:

```python
# 1. Register a concrete class (will be instantiated when resolved)
container.register(ServiceA)

# 2. Register with a factory function
container.register(ServiceB, lambda: ServiceB("some_config"))

# 3. Register an instance directly
service_c = ServiceC()
container.register(ServiceC, service_c)

# 4. Register with an interface type and named implementations
container.register(IRepository, SqlRepository(), "sql")
container.register(IRepository, MongoRepository(), "mongo")
```

### Dependency Injection

Implement dependency injection patterns:

```python
# Register base services
container.register(ILogger, ConsoleLogger())
container.register(IDatabase, SqlDatabase("connection_string"))

# Register a service with dependencies
container.register(UserService, lambda: UserService(
    container.resolve(ILogger),
    container.resolve(IDatabase)
))

# Resolve the service (with all dependencies injected)
user_service = container.resolve(UserService)
```

### Working with Interfaces

Create clean architecture with proper dependency inversion:

```python
# Define an interface
class INotificationService:
    def send(self, message: str) -> None:
        pass

# Define implementations
class EmailNotificationService(INotificationService):
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")

class SmsNotificationService(INotificationService):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")

# Register implementations with names
container.register(INotificationService, EmailNotificationService(), "email")
container.register(INotificationService, SmsNotificationService(), "sms")

# Use the services
email_service = container.resolve(INotificationService, "email")
sms_service = container.resolve(INotificationService, "sms")

email_service.send("Hello from email!")
sms_service.send("Hello from SMS!")
```

## API Reference

### Container Class

#### `__init__()`
Initialize a new dependency container.

#### `register(service_type, implementation=None, name=None)`
Register a service in the container.
- `service_type`: The type/interface being registered
- `implementation`: Either an instance or a factory function (optional)
- `name`: Optional name to distinguish multiple implementations
- Returns: Container instance (for fluent API)

#### `resolve(service_type, name=None)`
Resolve a service from the container.
- `service_type`: The type/interface to resolve
- `name`: Optional name for named implementations
- Returns: Instance of the requested service
- Raises: KeyError if service not found

#### `can_resolve(service_type, name=None)`
Check if a service can be resolved.
- `service_type`: The type/interface to check
- `name`: Optional name for named implementations
- Returns: Boolean indicating if service is registered

#### `unregister(service_type, name=None)`
Remove a service registration.
- `service_type`: The type/interface to unregister
- `name`: Optional name for named implementations
- Returns: Boolean indicating if something was removed

## Type Hinting

The container provides full type hinting support for modern Python development:

```python
from typing import Protocol

class IUserRepository(Protocol):
    def get_user(self, user_id: int) -> dict:
        ...

class UserRepository:
    def get_user(self, user_id: int) -> dict:
        return {"id": user_id, "name": "Test User"}

# Register and use with full type support
container.register(IUserRepository, UserRepository())
repo = container.resolve(IUserRepository)  # Properly typed as IUserRepository
user = repo.get_user(1)  # IDE provides proper completion
```

## Requirements

- Python 3.6+

## License

MIT License