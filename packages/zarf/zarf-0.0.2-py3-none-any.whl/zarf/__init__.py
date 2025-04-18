from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union, cast

T = TypeVar('T')
TImpl = TypeVar('TImpl')

# Define common types used in the container
ServiceType = Type[T]
ServiceFactory = Callable[[], T]
ServiceImplementation = Union[T, ServiceFactory[T]]


class Container:
    def __init__(self) -> None:
        """Initialize an empty dependency container."""
        self._registry: Dict[str, Any] = {}

    # Define complete overloads for Register method
    def register(self, service_type: Union[str, ServiceType], implementation: Optional[ServiceImplementation[T]] = None,
                 name: Optional[str] = None):
        """
        Register a service in the container.

        Args:
            service_type: The type/interface being registered
            implementation: Either an instance or a factory function that creates the instance
                           If None, service_type itself will be treated as the implementation
            name: Optional name to distinguish multiple implementations of the same type

        Returns:
            self for fluent API
        """
        key = self._get_key(service_type, name)

        if implementation is None:
            # If no implementation provided, use service_type as the implementation
            # (useful when service_type is a concrete class)
            self._registry[key] = service_type
        else:
            self._registry[key] = implementation

    def resolve(self, service_type: Union[str, ServiceType], name: Optional[str] = None) -> T:
        """
        Resolve a service from the container.

        Args:
            service_type: The type/interface to resolve
            name: Optional name if multiple implementations exist

        Returns:
            Instance of the requested service

        Raises:
            KeyError: If the requested service is not registered
        """
        key = self._get_key(service_type, name)

        if key not in self._registry:
            raise KeyError(f"No registration found for {service_type.__name__}{' with name ' + name if name else ''}")

        implementation = self._registry[key]

        # If implementation is callable (factory/class), invoke it
        if callable(implementation) and not isinstance(implementation, type(lambda: None).__class__):
            # It's a class, not a lambda or function
            return cast(T, implementation())
        elif callable(implementation):
            # It's a factory function/lambda
            return cast(T, implementation())
        else:
            # It's an instance, return as is
            return cast(T, implementation)

    def can_resolve(self, service_type: Union[str, ServiceType], name: Optional[str] = None) -> bool:
        """
        Check if a service can be resolved from the container.

        Args:
            service_type: The type/interface to check
            name: Optional name if multiple implementations exist

        Returns:
            bool: True if the service can be resolved, False otherwise
        """
        key = self._get_key(service_type, name)
        return key in self._registry

    def unregister(self, service_type: Union[str, ServiceType], name: Optional[str] = None) -> bool:
        """
        Remove a service registration from the container.

        Args:
            service_type: The type/interface to unregister
            name: Optional name if multiple implementations exist

        Returns:
            bool: True if something was removed, False if not found
        """
        key = self._get_key(service_type, name)
        if key in self._registry:
            del self._registry[key]
            return True
        return False

    @staticmethod
    def _get_key(service_type: Union[str, ServiceType], name: Optional[str] = None) -> str:
        """Generate a unique key for the registry based on type and name."""
        if isinstance(service_type, str):
            return f"callable-{service_type}:{name}" if name else f"callable-{service_type}"
        type_name = service_type.__name__ if hasattr(service_type, "__name__") else str(service_type)
        return f"{type_name}:{name}" if name else type_name


_current = Container()

def current() -> Container:
    global _current
    return _current
