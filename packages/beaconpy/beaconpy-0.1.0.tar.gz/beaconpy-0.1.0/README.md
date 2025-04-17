# beaconpy

A Pythonic implementation of the observer pattern, inspired by the Dart 'Antenna' mixin, with robust memory management and error handling.

## Features

- Weak references to callbacks (prevents memory leaks)
- Support for various callback types (functions, static methods, class methods, instance methods)
- Batch operations with a single notification
- Protection against reentrant notifications
- Control over whether notifications are sent
- Asynchronous scheduling of callbacks
- Automatic cleanup of stale observers
- Robust error handling that ensures all observers get notified even if some raise exceptions

## Installation

```bash
pip install beaconpy
```

## Usage

### Basic Usage

```python
from beaconpy import Beacon

# Create a class that extends Beacon
class Counter(Beacon):
    def __init__(self):
        super().__init__()
        self._count = 0
    
    @property
    def count(self):
        return self._count
    
    def increment(self):
        # Use the context manager to trigger notifications
        with self.changing_state():
            self._count += 1

# Create an observer function
def on_counter_changed(sender):
    print(f"Counter changed! New value: {sender.count}")

# Create a counter and register the observer
counter = Counter()
counter.add_observer(on_counter_changed)

# Increment the counter - this will trigger the observer
counter.increment()  # Prints: "Counter changed! New value: 1"

# Remove the observer when no longer needed
counter.remove_observer(on_counter_changed)
```

### Context Managers

The library provides three context managers for different notification behaviors:

```python
# Normal state change with notification
with beacon.changing_state():
    # Make changes to state here
    # Observers will be notified after the block

# Change state without notification
with beacon.changing_state_without_notification():
    # Make silent changes to state here
    # No observers will be notified

# Batch changes with a single notification
with beacon.batch_changing_state():
    # Make multiple changes to state here
    # Only one notification will be sent after all changes
```

### Supported Callback Types

beaconpy supports various types of callbacks:

```python
# Regular functions
def function_callback(sender):
    print("Function called")

# Static methods
class ExampleClass:
    @staticmethod
    def static_method_callback(sender):
        print("Static method called")

# Class methods
class ExampleClass:
    @classmethod
    def class_method_callback(cls, sender):
        print(f"Class method called on {cls.__name__}")

# Instance methods
class ExampleClass:
    def instance_method_callback(self, sender):
        print("Instance method called")

# Add as observers
example = ExampleClass()
beacon.add_observer(function_callback)
beacon.add_observer(ExampleClass.static_method_callback)
beacon.add_observer(ExampleClass.class_method_callback)
beacon.add_observer(example.instance_method_callback)
```

## Important Limitations

- Lambda functions are not supported as callbacks because they may be unexpectedly garbage collected
- `functools.partial` objects, dynamically created functions, and factory-created functions should be avoided for similar reasons

## Custom Error Handling

You can override the `on_sync_errors` method to customize error handling:

```python
class CustomBeacon(Beacon):
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def on_sync_errors(self, errors):
        # Store errors for later analysis
        self.errors.extend(errors)
        # You can also call the parent implementation if needed
        # super().on_sync_errors(errors)
```

## License

MIT
