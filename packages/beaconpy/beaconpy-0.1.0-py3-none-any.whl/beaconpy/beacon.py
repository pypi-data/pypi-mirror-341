"""
beaconpy - A Python Observer Pattern Implementation

This module provides a Beacon class that implements the observer pattern,
allowing objects to register callbacks that will be notified when the state changes.
It's designed to be a Pythonic implementation of the Dart 'Antenna' mixin.
"""

import asyncio
import inspect
import logging
import weakref
from contextlib import contextmanager
from typing import Any, Callable, List, Optional, Tuple


# Configure the logger
logger = logging.getLogger(__name__)


# Error messages as constants
class _ErrorMessages:
    """Container for error messages used in the Beacon class."""
    LAMBDA_NOT_SUPPORTED = "Lambda functions are not supported as callbacks because they may be unexpectedly garbage collected"


class _BaseCallbackWrapper:
    """
    Base class for all callback wrapper types.
    
    This abstract base class defines the interface that all callback wrapper
    implementations must support, providing a uniform way to work with different
    types of callbacks.
    """
    
    def __init__(self, callback: Callable[['Beacon'], None]):
        """
        Initialize a base callback wrapper.
        
        Args:
            callback: The callback to wrap.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        if _BaseCallbackWrapper.is_lambda(callback):
            raise TypeError(_ErrorMessages.LAMBDA_NOT_SUPPORTED)
    
    def __eq__(self, other: Any) -> bool:
        """
        Compare this wrapper with another wrapper or callback.
        
        Args:
            other: Another CallbackWrapper or a callback function.
            
        Returns:
            bool: True if they represent the same callback, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement __eq__")
    
    def __hash__(self) -> int:
        """
        Calculate a hash value for use in dictionaries.
        
        Returns:
            int: A hash based on the callback's identity.
        """
        raise NotImplementedError("Subclasses must implement __hash__")
    
    def __call__(self, sender: 'Beacon') -> None:
        """
        Call the wrapped callback, if it still exists.
        
        Args:
            sender: The Beacon instance that triggered the notification.
            
        If the original callback has been garbage collected, this method does nothing.
        """
        raise NotImplementedError("Subclasses must implement __call__")
    
    @staticmethod
    def is_lambda(func: Callable) -> bool:
        """
        Check if a function is a lambda function.
        
        Args:
            func: The function to check.
            
        Returns:
            bool: True if the function is a lambda function, False otherwise.
        """
        return inspect.isfunction(func) and func.__name__ == '<lambda>'
    
    @staticmethod
    def is_class_method(func: Callable) -> bool:
        """
        Check if a callable is a class method.
        
        Args:
            func: The callable to check.
            
        Returns:
            bool: True if the callable is a class method, False otherwise.
        """
        return (inspect.ismethod(func) and 
                func.__self__ is not None and 
                isinstance(func.__self__, type))
    
    @staticmethod
    def is_instance_method(func: Callable) -> bool:
        """
        Check if a callable is an instance method.
        
        Args:
            func: The callable to check.
            
        Returns:
            bool: True if the callable is an instance method, False otherwise.
        """
        return (inspect.ismethod(func) and 
                func.__self__ is not None and 
                not isinstance(func.__self__, type))
    
    @staticmethod
    def create(callback: Callable[['Beacon'], None]) -> '_BaseCallbackWrapper':
        """
        Factory method to create the appropriate wrapper type for a callback.
        
        Args:
            callback: The callback to wrap.
            
        Returns:
            _BaseCallbackWrapper: A specific subclass instance that can handle the callback type.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        if _BaseCallbackWrapper.is_lambda(callback):
            raise TypeError(_ErrorMessages.LAMBDA_NOT_SUPPORTED)
            
        if _BaseCallbackWrapper.is_class_method(callback):
            return _ClassMethodWrapper(callback)
            
        if _BaseCallbackWrapper.is_instance_method(callback):
            return _InstanceMethodWrapper(callback)
            
        # All other callable types (functions and static methods) use the _FunctionalCallbackWrapper
        return _FunctionalCallbackWrapper(callback)


class _FunctionalCallbackWrapper(_BaseCallbackWrapper):
    """
    A wrapper for functional callbacks, including regular functions and static methods.
    
    This wrapper handles any callback that behaves like a simple function without requiring
    special binding or reconstruction. It uses weak references to allow functions to be
    garbage collected when no longer used elsewhere.
    """
    
    def __init__(self, callback: Callable[['Beacon'], None]):
        """
        Initialize a new _FunctionalCallbackWrapper instance.
        
        Args:
            callback: The function or static method to wrap.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        super().__init__(callback)
        self.callback_ref = weakref.ref(callback)
        self.callback_id = id(callback)
    
    def __eq__(self, other: Any) -> bool:
        """
        Compare this wrapper with another wrapper or function/static method.
        
        Args:
            other: Another wrapper or a callable.
            
        Returns:
            bool: True if they represent the same callback, False otherwise.
        """
        if isinstance(other, _BaseCallbackWrapper):
            # Compare with another wrapper
            return self.callback_id == other.__hash__()
        else:
            # Compare with a direct function or static method
            try:
                # For methods that might have a __func__ attribute
                if hasattr(other, '__func__'):
                    return self.callback_id == id(other.__func__)
                # For regular functions and static methods accessed through a class
                return self.callback_id == id(other)
            except (TypeError, AttributeError):
                return False
    
    def __hash__(self) -> int:
        """
        Calculate a hash value for the wrapped callback.
        
        Returns:
            int: A hash based on the callback's identity.
        """
        return self.callback_id
    
    def __call__(self, sender: 'Beacon') -> None:
        """
        Call the wrapped callback with the sender, if it still exists.
        
        Args:
            sender: The Beacon instance that triggered the notification.
            
        If the callback has been garbage collected, this method does nothing.
        """
        callback = self.callback_ref()
        if callback is not None:
            callback(sender)


class _ClassMethodWrapper(_BaseCallbackWrapper):
    """
    A wrapper for class method callbacks.
    
    This wrapper handles the special case of class methods, which are bound to a class
    rather than an instance and need special handling for reconstruction and identity.
    """
    
    def __init__(self, callback: Callable[['Beacon'], None]):
        """
        Initialize a new _ClassMethodWrapper instance.
        
        Args:
            callback: The class method to wrap.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        super().__init__(callback)
        self.callback_ref = weakref.ref(callback)
        self.class_ref = weakref.ref(callback.__self__)  #type: ignore
        self.func_ref = weakref.ref(callback.__func__)  #type: ignore
        # Use a tuple of IDs for the class and function as the unique identifier
        self.callback_id = (id(callback.__self__), id(callback.__func__))   #type: ignore
    
    def __eq__(self, other: Any) -> bool:
        """
        Compare this wrapper with another wrapper or class method.
        
        Args:
            other: Another wrapper or a class method.
            
        Returns:
            bool: True if they represent the same class method, False otherwise.
        """
        if isinstance(other, _ClassMethodWrapper):
            # Compare with another class method wrapper
            return self.callback_id == other.callback_id
        elif isinstance(other, _BaseCallbackWrapper):
            # Different wrapper types can't be equal
            return False
        else:
            # Compare with a direct class method
            try:
                if (inspect.ismethod(other) and other.__self__ is not None and
                        isinstance(other.__self__, type)):
                    return self.callback_id == (id(other.__self__), id(other.__func__))
                return False
            except (TypeError, AttributeError):
                return False
    
    def __hash__(self) -> int:
        """
        Calculate a hash value for the wrapped class method.
        
        Returns:
            int: A hash based on the class method's identity.
        """
        return hash(self.callback_id)
    
    def __call__(self, sender: 'Beacon') -> None:
        """
        Call the wrapped class method with the sender, if it still exists.
        
        Args:
            sender: The Beacon instance that triggered the notification.
            
        This reconstructs the class method from its component parts if they still exist.
        If any component has been garbage collected, this method does nothing.
        """
        cls = self.class_ref()
        func = self.func_ref()
        
        if cls is not None and func is not None:
            # Pass the class as first argument and sender as second argument
            func(cls, sender)


class _InstanceMethodWrapper(_BaseCallbackWrapper):
    """
    A wrapper for instance method callbacks.
    
    This wrapper handles instance methods, which are bound to a specific object instance
    and need special handling for weak references and identity.
    """
    
    def __init__(self, callback: Callable[['Beacon'], None]):
        """
        Initialize a new _InstanceMethodWrapper instance.
        
        Args:
            callback: The instance method to wrap.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        super().__init__(callback)
        self.callback_ref = weakref.ref(callback)
        self.instance_ref = weakref.ref(callback.__self__)  #type: ignore
        self.func_ref = weakref.ref(callback.__func__)      #type: ignore
        # Use a tuple of IDs for the instance and function as the unique identifier
        self.callback_id = (id(callback.__self__), id(callback.__func__))   #type: ignore
    
    def __eq__(self, other: Any) -> bool:
        """
        Compare this wrapper with another wrapper or instance method.
        
        Args:
            other: Another wrapper or an instance method.
            
        Returns:
            bool: True if they represent the same instance method, False otherwise.
        """
        if isinstance(other, _InstanceMethodWrapper):
            # Compare with another instance method wrapper
            return self.callback_id == other.callback_id
        elif isinstance(other, _BaseCallbackWrapper):
            # Different wrapper types can't be equal
            return False
        else:
            # Compare with a direct instance method
            try:
                if (inspect.ismethod(other) and other.__self__ is not None and
                        not isinstance(other.__self__, type)):
                    return self.callback_id == (id(other.__self__), id(other.__func__))
                return False
            except (TypeError, AttributeError):
                return False
    
    def __hash__(self) -> int:
        """
        Calculate a hash value for the wrapped instance method.
        
        Returns:
            int: A hash based on the instance method's identity.
        """
        return hash(self.callback_id)
    
    def __call__(self, sender: 'Beacon') -> None:
        """
        Call the wrapped instance method with the sender, if it still exists.
        
        Args:
            sender: The Beacon instance that triggered the notification.
            
        This reconstructs the instance method from its component parts if they still exist.
        If any component has been garbage collected, this method does nothing.
        """
        instance = self.instance_ref()
        func = self.func_ref()
        
        if instance is not None and func is not None:
            # Call the function with the instance as first argument and sender as second argument
            func(instance, sender)


class Beacon:
    """
    An implementation of the observer pattern that manages callbacks and notifications.
    
    This class allows objects to register callbacks that will be notified when state changes.
    It uses weak references to prevent memory leaks and provides flexible notification control.
    
    Key features:
    - Weak references to callbacks (prevents memory leaks)
    - Support for various callback types (functions, static methods, class methods, instance methods)
    - Batch operations with a single notification
    - Protection against reentrant notifications
    - Control over whether notifications are sent
    - Asynchronous scheduling of callbacks
    - Automatic cleanup of stale observers
    - Robust error handling that ensures all observers get notified even if some raise exceptions
    
    Note:
        When subclassing Beacon, consider implementing `__eq__` and `__hash__` if 
        observers need to distinguish between different instances of your class.
        This is particularly important if observers subscribe to multiple sources
        and need to perform different actions based on which source triggered the notification.
    
    Important Limitations:
    While this implementation supports multiple callback types (functions, static methods,
    class methods, and instance methods), it has several limitations regarding callback types:
    
    1. Lambda functions are explicitly rejected. This is because lambdas can be garbage 
       collected unexpectedly when their defining scope ends, causing callbacks to silently 
       disappear.
       
    2. The following function types should also be avoided, as they can lead to similar 
       memory management and identity issues:
       
       - functools.partial objects: These create new function objects that may not be 
         properly retained in memory.
         
       - Dynamically created functions (using exec or eval): These often lack proper 
         module association and may be prematurely garbage collected.
         
       - Functions returned by other functions (factory-created functions or closures): 
         These can have unstable identity (a new function object is created each time 
         the factory is called) and may be garbage collected if not stored in stable 
         variables.
         
    For reliable observer callbacks, use:
    - Named functions defined at module level
    - Instance methods of objects with stable lifetimes
    - Class methods
    - Static methods
    
    Error Handling:
    - All observers are responsible for handling their own exceptions.
    - Exceptions in one observer will not prevent other observers from being notified.
    - In synchronous mode, uncaught exceptions are collected and passed to on_sync_errors().
    - In asynchronous mode, exceptions are handled by the event loop.
    - Subclasses can override on_sync_errors() to customize exception handling.
    """
    
    def __init__(self):
        """Initialize a new Beacon instance."""
        # Dictionary to store callback wrappers
        self._observers = {}  # Regular dict instead of WeakValueDictionary
        self._next_key = 0  # For generating unique keys
        
        # Control flags
        self._total_calls = 0  # Track reentrant calls
        self._inside_batch_operation = False  # Batch mode flag
        self._notifications_on_hold = False  # For stealth changes
    
    def add_observer(self, callback: Callable[['Beacon'], None]) -> bool:
        """
        Register a callback to be notified when state changes.
        
        Args:
            callback: A function to call when state changes. Must be a regular function,
                     not a lambda function. The function must accept one parameter:
                     the Beacon instance that triggered the notification.
            
        Returns:
            bool: True if the callback was added, False if it was already present.
            
        Raises:
            TypeError: If callback is a lambda function.
        """
        try:
            # Use the factory method to create the appropriate wrapper
            wrapper = _BaseCallbackWrapper.create(callback)
            
            if not self.is_being_observed(callback):
                key = self._next_key
                self._next_key += 1
                self._observers[key] = wrapper
                return True
            return False
        except TypeError:
            # Re-raise any TypeError from the wrapper (e.g., for lambda functions)
            raise
    
    def remove_observer(self, callback: Callable[['Beacon'], None]) -> bool:
        """
        Remove a callback from the notification list.
        
        Args:
            callback: The callback to remove.
            
        Returns:
            bool: True if the callback was removed, False if it wasn't found or if
                 the callback is a lambda function (which can't be registered).
        """
        # For lambda functions, just return False (they can't be registered anyway)
        if _BaseCallbackWrapper.is_lambda(callback):
            return False
            
        key = self._find_key(callback)
        if key is not None:
            del self._observers[key]
            return True
        return False
    
    def is_being_observed(self, callback: Callable[['Beacon'], None]) -> bool:
        """
        Check if a callback is already registered as an observer.
        
        Args:
            callback: The callback to check.
            
        Returns:
            bool: True if the callback is registered, False otherwise.
        """
        return self._find_key(callback) is not None
    
    @contextmanager
    def changing_state(self):
        """
        Context manager for changing state with notification.
        
        Usage:
            with beacon.changing_state():
                # Make state changes here
        """
        self._total_calls += 1
        try:
            yield
        finally:
            self._notify_all_observers()
            self._total_calls -= 1
    
    @contextmanager
    def changing_state_without_notification(self):
        """
        Context manager for changing state without notification.
        
        Usage:
            with beacon.changing_state_without_notification():
                # Make silent state changes here
        """
        self._notifications_on_hold = True
        try:
            yield
        finally:
            self._notifications_on_hold = False
    
    @contextmanager
    def batch_changing_state(self):
        """
        Context manager for batch changes with a single notification at the end.
        
        Usage:
            with beacon.batch_changing_state():
                # Make multiple state changes here
                # Only one notification will be sent
        """
        self._inside_batch_operation = True
        self._total_calls += 1
        try:
            yield
        finally:
            self._inside_batch_operation = False
            self._notify_all_observers()
            self._total_calls -= 1
    
    def _find_key(self, callback: Callable[['Beacon'], None]) -> Optional[int]:
        """
        Find the key associated with a callback.
        
        Args:
            callback: The callback to find.
            
        Returns:
            Optional[int]: The key if found, None otherwise.
        """
        for key, existing_wrapper in self._observers.items():
            if existing_wrapper == callback:
                return key
        return None
    
    def _should_notify_observers(self) -> Tuple[Optional[asyncio.AbstractEventLoop], bool]:
        """
        Determine if observers should be notified and get the appropriate event loop.
        
        Returns:
            tuple: (event_loop, should_notify)
                - event_loop: The asyncio event loop if available, None if using synchronous execution
                - should_notify: Boolean indicating if observers should be notified
        """
        should_notify = (
            self._total_calls == 1 and 
            not self._inside_batch_operation and 
            not self._notifications_on_hold
        )
        
        # If we shouldn't notify, we don't need a loop
        if not should_notify:
            return None, False
        
        # Try to get the running event loop for async notification
        try:
            loop = asyncio.get_running_loop()
            return loop, True
        except RuntimeError:
            # No running loop, will use synchronous execution
            return None, True

    def _notify_single_observer(self, callback_wrapper: _BaseCallbackWrapper, 
                               loop: Optional[asyncio.AbstractEventLoop] = None) -> Optional[Exception]:
        """
        Notify a single observer, either synchronously or asynchronously.
        
        Args:
            callback_wrapper: The CallbackWrapper instance to notify
            loop: The asyncio event loop for async notification, or None for sync
            
        Returns:
            Optional[Exception]: If in sync mode and an exception occurs, returns the exception.
                                None otherwise or in async mode.
        """
        if loop:
            # Async notification
            def counter_wrapper():
                self._total_calls += 1
                try:
                    callback_wrapper(self)  # Pass self as the sender
                except Exception as e:
                    # In async mode, the event loop will handle the exception
                    logger.exception(f"Async observer raised an exception: {e}")
                finally:
                    self._total_calls -= 1
            
            loop.call_soon(counter_wrapper)
            return None
        else:
            # Sync notification
            self._total_calls += 1
            try:
                callback_wrapper(self)  # Pass self as the sender
                return None
            except Exception as e:
                # In sync mode, capture the exception and return it
                return e
            finally:
                self._total_calls -= 1

    def on_sync_errors(self, errors: List[Tuple[_BaseCallbackWrapper, Exception]]) -> None:
        """
        Handle exceptions that occurred during synchronous notifications.
        
        This method is called when one or more observers raise uncaught exceptions
        during synchronous notification. The default implementation logs the errors.
        Subclasses can override this method to provide custom error handling.
        
        Args:
            errors: A list of tuples, each containing a callback wrapper and the exception it raised.
        """
        for wrapper, exception in errors:
            # Default behavior is to log the exception
            callback = wrapper.callback_ref() if hasattr(wrapper, 'callback_ref') else None     #type: ignore
            callback_str = str(callback) if callback else "Unknown callback (garbage collected)"
            logger.error(f"Observer {callback_str} raised an exception: {exception}", exc_info=exception)

    def _notify_all_observers(self) -> None:
        """
        Notify all observers if conditions are right and clean up stale observers.
        
        This method sends notifications when appropriate and removes any stale
        observers whose callbacks have been garbage collected. It also handles
        exceptions from observers to ensure all observers get notified even if
        some raise exceptions.
        """
        # Get notification settings
        loop, should_notify = self._should_notify_observers()
        
        # Process all observers in a single pass
        stale_observer_keys = []
        sync_errors = []  # List to collect errors from synchronous notifications
        
        for key, wrapper in self._observers.items():
            # Check if the callback is stale based on the wrapper type
            if isinstance(wrapper, (_ClassMethodWrapper, _InstanceMethodWrapper)):
                is_stale = (wrapper.func_ref() is None or 
                           (isinstance(wrapper, _ClassMethodWrapper) and wrapper.class_ref() is None) or
                           (isinstance(wrapper, _InstanceMethodWrapper) and wrapper.instance_ref() is None))
            else:
                is_stale = wrapper.callback_ref() is None
            
            if is_stale:
                # Mark for cleanup
                stale_observer_keys.append(key)
                continue
                
            # Notify if appropriate
            if should_notify:
                error = self._notify_single_observer(wrapper, loop)
                if error is not None:
                    # Only collect errors in synchronous mode
                    sync_errors.append((wrapper, error))
        
        # Remove stale observers
        for key in stale_observer_keys:
            del self._observers[key]
            
        # Handle any synchronous errors if there are any
        if sync_errors:
            self.on_sync_errors(sync_errors) 