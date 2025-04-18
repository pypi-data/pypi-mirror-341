import pytest
from . import Container  # Assuming the Container class is in container.py


# Define test classes
class IService:
    def execute(self):
        pass


class ServiceA(IService):
    def execute(self):
        return "ServiceA executed"


class ServiceB(IService):
    def execute(self):
        return "ServiceB executed"


class ServiceWithDependency:
    def __init__(self, dependency=None):
        self.dependency = dependency

    def execute(self):
        if self.dependency:
            return f"ServiceWithDependency used {self.dependency.execute()}"
        return "ServiceWithDependency executed"


def FunctionA():
    return "FunctionA executed"

def FunctionB():
    return "FunctionB executed"


@pytest.fixture
def container():
    """Create a fresh container for each test."""
    return Container()


class TestContainerRegistration:
    def test_register_class(self, container):
        # Register a class
        container.register(ServiceA)
        assert container.can_resolve(ServiceA)

    def test_register_named_implementation(self, container):
        # Register with a name
        container.register(IService, ServiceA(), "serviceA")
        assert container.can_resolve(IService, "serviceA")

    def test_register_factory(self, container):
        # Register with a factory function
        container.register(ServiceA, lambda: ServiceA())
        assert container.can_resolve(ServiceA)

    def test_register_instance(self, container):
        # Register an instance
        instance = ServiceA()
        container.register(ServiceA, instance)

        # Resolve should return the exact same instance
        resolved = container.resolve(ServiceA)
        assert resolved is instance

    def test_register_multiple_implementations(self, container):
        # Register multiple implementations of the same interface
        container.register(IService, ServiceA(), "A")
        container.register(IService, ServiceB(), "B")

        assert container.can_resolve(IService, "A")
        assert container.can_resolve(IService, "B")
        assert not container.can_resolve(IService)  # No default implementation

    def test_register_overwrite(self, container):
        # Register and then overwrite
        container.register(ServiceA, lambda: ServiceA())
        first_instance = container.resolve(ServiceA)

        # Overwrite with a different instance
        specific_instance = ServiceA()
        container.register(ServiceA, specific_instance)

        second_instance = container.resolve(ServiceA)
        assert second_instance is specific_instance
        assert first_instance is not second_instance


class TestContainerResolution:
    def test_resolve_class(self, container):
        container.register(ServiceA)
        service = container.resolve(ServiceA)
        assert isinstance(service, ServiceA)
        assert service.execute() == "ServiceA executed"

    def test_resolve_factory(self, container):
        container.register(ServiceA, lambda: ServiceA())
        service = container.resolve(ServiceA)
        assert isinstance(service, ServiceA)

    def test_resolve_instance(self, container):
        instance = ServiceA()
        container.register(ServiceA, instance)
        resolved = container.resolve(ServiceA)
        assert resolved is instance

    def test_resolve_function(self, container):
        container.register('test_function', FunctionA)
        resolved = container.resolve('test_function')
        assert resolved == FunctionA()

    def test_resolve_named(self, container):
        container.register(IService, ServiceA(), "A")
        container.register(IService, ServiceB(), "B")

        service_a = container.resolve(IService, "A")
        service_b = container.resolve(IService, "B")

        assert isinstance(service_a, ServiceA)
        assert isinstance(service_b, ServiceB)
        assert service_a.execute() == "ServiceA executed"
        assert service_b.execute() == "ServiceB executed"

    def test_resolve_with_dependency(self, container):
        # Set up a ServiceA instance
        service_a = ServiceA()
        container.register(ServiceA, service_a)

        # Register a factory that uses ServiceA
        container.register(ServiceWithDependency,
                           lambda: ServiceWithDependency(container.resolve(ServiceA)))

        # Resolve and test
        service = container.resolve(ServiceWithDependency)
        assert service.execute() == "ServiceWithDependency used ServiceA executed"

    def test_resolve_missing_raises_error(self, container):
        with pytest.raises(KeyError):
            container.resolve(ServiceA)

    def test_resolve_named_missing_raises_error(self, container):
        container.register(IService, ServiceA(), "A")
        with pytest.raises(KeyError):
            container.resolve(IService, "B")  # B is not registered


class TestContainerCanResolve:
    def test_can_resolve_registered(self, container):
        container.register(ServiceA)
        assert container.can_resolve(ServiceA) is True

    def test_can_resolve_unregistered(self, container):
        assert container.can_resolve(ServiceA) is False

    def test_can_resolve_named(self, container):
        container.register(IService, ServiceA(), "A")
        assert container.can_resolve(IService, "A") is True
        assert container.can_resolve(IService, "B") is False


class TestContainerUnregister:
    def test_unregister_existing(self, container):
        container.register(ServiceA)
        assert container.can_resolve(ServiceA) is True

        result = container.unregister(ServiceA)
        assert result is True
        assert container.can_resolve(ServiceA) is False

    def test_unregister_missing(self, container):
        result = container.unregister(ServiceA)
        assert result is False

    def test_unregister_named(self, container):
        container.register(IService, ServiceA(), "A")
        container.register(IService, ServiceB(), "B")

        # Unregister one implementation
        result = container.unregister(IService, "A")
        assert result is True
        assert container.can_resolve(IService, "A") is False
        assert container.can_resolve(IService, "B") is True

        # Unregister the other implementation
        result = container.unregister(IService, "B")
        assert result is True
        assert container.can_resolve(IService, "B") is False


class TestContainerEdgeCases:
    def test_register_with_none_implementation(self, container):
        # Testing when implementation parameter is None
        container.register(ServiceA, None)
        service = container.resolve(ServiceA)
        assert isinstance(service, ServiceA)

    def test_resolve_same_type_different_registrations(self, container):
        # Register the same type with different names
        container.register(ServiceA, ServiceA())
        container.register(ServiceA, ServiceA(), "named")

        # Should be different instances
        default = container.resolve(ServiceA)
        named = container.resolve(ServiceA, "named")

        assert default is not named
        assert isinstance(default, ServiceA)
        assert isinstance(named, ServiceA)

    def test_factory_creates_new_instance_each_time(self, container):
        container.register(ServiceA, lambda: ServiceA())

        instance1 = container.resolve(ServiceA)
        instance2 = container.resolve(ServiceA)

        assert instance1 is not instance2
        assert isinstance(instance1, ServiceA)
        assert isinstance(instance2, ServiceA)