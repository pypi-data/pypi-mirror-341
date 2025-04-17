"""
Tests for the Beacon class.

This module contains comprehensive tests for the Beacon observer pattern
implementation, covering all major features and edge cases including error handling.
"""

import asyncio
import gc
import pytest
from unittest.mock import patch, MagicMock

from beaconpy import Beacon
from beaconpy.beacon import (
    _ErrorMessages, _BaseCallbackWrapper, _FunctionalCallbackWrapper, 
    _ClassMethodWrapper, _InstanceMethodWrapper
)


class TestCallbackWrappers:
    """Tests for the callback wrapper classes."""
    
    def test_functional_callback_wrapper(self):
        """Test the FunctionalCallbackWrapper class with regular functions."""
        def callback(sender):
            pass
        
        wrapper = _FunctionalCallbackWrapper(callback)
        
        # Check proper storage
        assert wrapper.callback_ref() is callback
        assert wrapper.callback_id == id(callback)
        
        # Test equality
        assert wrapper == callback
        assert wrapper == _FunctionalCallbackWrapper(callback)
        
        # Test inequality
        def another_callback(sender):
            pass
        assert wrapper != another_callback
        assert wrapper != _FunctionalCallbackWrapper(another_callback)
        
        # Test callback invocation
        called = False
        sender_received = None
        
        def test_callback(sender):
            nonlocal called, sender_received
            called = True
            sender_received = sender
        
        test_wrapper = _FunctionalCallbackWrapper(test_callback)
        mock_sender = MagicMock()
        test_wrapper(mock_sender)
        assert called is True
        assert sender_received is mock_sender
    
    def test_static_method_with_functional_wrapper(self):
        """Test that FunctionalCallbackWrapper works with static methods."""
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
        
        wrapper = _FunctionalCallbackWrapper(TestClass.static_method)
        
        # Check proper storage
        assert wrapper.callback_ref() is TestClass.static_method
        assert wrapper.callback_id == id(TestClass.static_method)
        
        # Test equality
        assert wrapper == TestClass.static_method
        assert wrapper == _FunctionalCallbackWrapper(TestClass.static_method)
        
        # Test inequality
        class AnotherClass:
            @staticmethod
            def static_method(sender):
                pass
        assert wrapper != AnotherClass.static_method
        assert wrapper != _FunctionalCallbackWrapper(AnotherClass.static_method)
        
        # Test callback invocation
        called = False
        sender_received = None
        
        class TestInvocation:
            @staticmethod
            def static_method(sender):
                nonlocal called, sender_received
                called = True
                sender_received = sender
        
        test_wrapper = _FunctionalCallbackWrapper(TestInvocation.static_method)
        mock_sender = MagicMock()
        test_wrapper(mock_sender)
        assert called is True
        assert sender_received is mock_sender
    
    def test_class_method_wrapper(self):
        """Test the ClassMethodWrapper class."""
        # Define class at the module level or keep a reference to prevent garbage collection
        class TestClass:
            @classmethod
            def class_method(cls, sender):
                pass
        
        # Store a reference to the class method to prevent garbage collection
        # during the test
        test_class_method = TestClass.class_method
        
        wrapper = _ClassMethodWrapper(test_class_method)
        
        # Check proper storage - now this should work
        assert wrapper.callback_ref() is test_class_method
        assert wrapper.class_ref() is TestClass
        assert wrapper.func_ref() is test_class_method.__func__     #type: ignore
        assert wrapper.callback_id == (id(TestClass), id(test_class_method.__func__))   #type: ignore
        
        # Test equality
        assert wrapper == test_class_method
        assert wrapper == _ClassMethodWrapper(test_class_method)
        
        # Test inequality
        class AnotherClass:
            @classmethod
            def class_method(cls, sender):
                pass
        
        # Also store a reference to this second class method
        another_class_method = AnotherClass.class_method
        
        assert wrapper != another_class_method
        assert wrapper != _ClassMethodWrapper(another_class_method)
        
        # Test callback invocation
        called = False
        cls_received = None
        sender_received = None
        
        class TestInvocation:
            @classmethod
            def class_method(cls, sender):
                nonlocal called, cls_received, sender_received
                called = True
                cls_received = cls
                sender_received = sender
        
        # Store yet another reference
        test_invocation_method = TestInvocation.class_method
        
        test_wrapper = _ClassMethodWrapper(test_invocation_method)
        mock_sender = MagicMock()
        test_wrapper(mock_sender)
        
        assert called is True
        assert cls_received is TestInvocation
        assert sender_received is mock_sender
    
    def test_instance_method_wrapper(self):
        """Test the InstanceMethodWrapper class."""
        class TestClass:
            def instance_method(self, sender):
                pass
        
        instance = TestClass()
        
        # Store a reference to the instance method to prevent garbage collection
        # during the test
        instance_method = instance.instance_method
        
        wrapper = _InstanceMethodWrapper(instance_method)
        
        # Check proper storage
        assert wrapper.callback_ref() is instance_method
        assert wrapper.instance_ref() is instance
        assert wrapper.func_ref() is instance_method.__func__   #type: ignore
        assert wrapper.callback_id == (id(instance), id(instance_method.__func__))  #type: ignore
        
        # Test equality
        assert wrapper == instance_method
        assert wrapper == _InstanceMethodWrapper(instance_method)
        
        # Test inequality
        another_instance = TestClass()
        another_instance_method = another_instance.instance_method
        
        assert wrapper != another_instance_method
        assert wrapper != _InstanceMethodWrapper(another_instance_method)
        
        # Test callback invocation
        class TestInvocation:
            def __init__(self):
                self.called = False
                self.sender_received = None
                
            def instance_method(self, sender):
                self.called = True
                self.sender_received = sender
        
        test_instance = TestInvocation()
        test_wrapper = _InstanceMethodWrapper(test_instance.instance_method)
        mock_sender = MagicMock()
        test_wrapper(mock_sender)
        
        assert test_instance.called is True
        assert test_instance.sender_received is mock_sender
    
    def test_factory_method(self):
        """Test the factory method that creates the appropriate wrapper type."""
        def function(sender):
            pass
        
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
            
            @classmethod
            def class_method(cls, sender):
                pass
            
            def instance_method(self, sender):
                pass
            
        instance = TestClass()
        
        # Check that appropriate wrappers are created
        wrapper1 = _BaseCallbackWrapper.create(function)
        assert isinstance(wrapper1, _FunctionalCallbackWrapper)
        
        wrapper2 = _BaseCallbackWrapper.create(TestClass.static_method)
        assert isinstance(wrapper2, _FunctionalCallbackWrapper)
        
        wrapper3 = _BaseCallbackWrapper.create(TestClass.class_method)
        assert isinstance(wrapper3, _ClassMethodWrapper)
        
        wrapper4 = _BaseCallbackWrapper.create(instance.instance_method)
        assert isinstance(wrapper4, _InstanceMethodWrapper)
    
    def test_lambda_rejection(self):
        """Test that lambda functions are rejected as callbacks."""
        # Try to create a wrapper with a lambda
        with pytest.raises(TypeError) as excinfo:
            _BaseCallbackWrapper.create(lambda sender: None)
        
        # Verify the error message
        assert str(excinfo.value) == _ErrorMessages.LAMBDA_NOT_SUPPORTED
    
    def test_hash_implementation(self):
        """Test that hash implementation works correctly for all wrapper types."""
        def callback1(sender):
            pass
        
        def callback2(sender):
            pass
        
        # Test hash consistency
        wrapper1 = _FunctionalCallbackWrapper(callback1)
        wrapper2 = _FunctionalCallbackWrapper(callback1)
        wrapper3 = _FunctionalCallbackWrapper(callback2)
        
        assert hash(wrapper1) == hash(wrapper2)
        assert hash(wrapper1) != hash(wrapper3)
    
    def test_weak_reference_behavior(self):
        """Test that wrappers use weak references and don't prevent garbage collection."""
        # Test with function
        def callback(sender):
            pass
        
        wrapper = _FunctionalCallbackWrapper(callback)
        assert wrapper.callback_ref() is callback
        
        # Remove all references to the function and force garbage collection
        callback_id = id(callback)
        del callback
        gc.collect()
        
        # Wrapper's weak reference should now be None
        assert wrapper.callback_ref() is None
        
        # Test with class method
        class TestClass:
            @classmethod
            def class_method(cls, sender):
                pass
        
        method = TestClass.class_method
        wrapper = _ClassMethodWrapper(method)
        assert wrapper.callback_ref() is method
        
        # Store original references
        class_id = id(TestClass)
        method_id = id(method)
        
        # Delete references and force garbage collection
        del TestClass
        del method
        gc.collect()
        
        # Wrapper's weak references should now be None
        assert wrapper.callback_ref() is None
        assert wrapper.class_ref() is None
        
        # Test with instance method
        class TestInstanceClass:
            def instance_method(self, sender):
                pass
        
        instance = TestInstanceClass()
        method = instance.instance_method
        wrapper = _InstanceMethodWrapper(method)
        
        # Delete references and force garbage collection
        instance_id = id(instance)
        method_id = id(method)
        del instance
        del method
        gc.collect()
        
        # Wrapper's weak references should now be None
        assert wrapper.callback_ref() is None
        assert wrapper.instance_ref() is None


class TestErrorHandling:
    """Tests for error handling in the Beacon class."""
    
    def test_sync_error_handling(self):
        """Test that exceptions in synchronous observers are properly handled."""
        beacon = Beacon()
        mock_logger = MagicMock()
        
        # Create a normal observer and one that raises an exception
        normal_observer_called = False
        
        def normal_observer(sender):
            nonlocal normal_observer_called
            normal_observer_called = True
        
        def error_observer(sender):
            raise ValueError("Test exception")
        
        # Add the observers
        beacon.add_observer(normal_observer)
        beacon.add_observer(error_observer)
        
        # Patch the logger and on_sync_errors method to track calls
        with patch('beaconpy.beacon.logger', mock_logger):
            with patch.object(beacon, 'on_sync_errors') as mock_on_sync_errors:
                # Trigger notification
                with beacon.changing_state():
                    pass
                
                # Verify that both observers were called
                assert normal_observer_called is True
                
                # Verify the on_sync_errors method was called
                assert mock_on_sync_errors.called
                
                # Check that logger was not used directly (delegated to on_sync_errors)
                mock_logger.error.assert_not_called()
    
    def test_async_error_handling(self):
        """Test that exceptions in async observers are properly handled."""
        loop = asyncio.new_event_loop()
        
        try:
            asyncio.set_event_loop(loop)
            beacon = Beacon()
            mock_logger = MagicMock()
            
            async def setup_test():
                # Create a normal observer and one that raises an exception
                normal_observer_called = False
                
                def normal_observer(sender):
                    nonlocal normal_observer_called
                    normal_observer_called = True
                
                def error_observer(sender):
                    raise ValueError("Test exception")
                
                # Add the observers
                beacon.add_observer(normal_observer)
                beacon.add_observer(error_observer)
                
                # Trigger notification
                with patch('beaconpy.beacon.logger', mock_logger):
                    with beacon.changing_state():
                        pass
                    
                    # Give event loop a chance to process callbacks
                    await asyncio.sleep(0.1)
                    
                    # Verify that the normal observer was called
                    assert normal_observer_called is True
                    
                    # The error should have been logged since it was async
                    mock_logger.exception.assert_called_once()

            loop.run_until_complete(setup_test())
        finally:
            loop.close()
            asyncio.set_event_loop(None)
    
    def test_on_sync_errors_override(self):
        """Test that subclasses can override on_sync_errors method."""
        # Create a subclass with custom error handling
        class CustomBeacon(Beacon):
            def __init__(self):
                super().__init__()
                self.errors_received = []
            
            def on_sync_errors(self, errors):
                self.errors_received.extend(errors)
        
        beacon = CustomBeacon()
        
        # Create an observer that raises an exception
        def error_observer(sender):
            raise ValueError("Custom handling test")
        
        # Add the observer and trigger notification
        beacon.add_observer(error_observer)
        with beacon.changing_state():
            pass
        
        # Verify the custom error handling worked
        assert len(beacon.errors_received) == 1
        assert isinstance(beacon.errors_received[0][0], _BaseCallbackWrapper)
        assert isinstance(beacon.errors_received[0][1], ValueError)
        assert str(beacon.errors_received[0][1]) == "Custom handling test"
    
    def test_multiple_observer_errors(self):
        """Test handling of multiple observer errors in a single notification."""
        beacon = Beacon()
        
        # Create multiple observers that raise different exceptions
        def error_observer1(sender):
            raise ValueError("Error 1")
        
        def error_observer2(sender):
            raise TypeError("Error 2")
        
        def normal_observer(sender):
            normal_observer.called = True   #type: ignore
        normal_observer.called = False      #type: ignore
        
        # Add all observers
        beacon.add_observer(error_observer1)
        beacon.add_observer(error_observer2)
        beacon.add_observer(normal_observer)
        
        # Patch on_sync_errors to track calls
        with patch.object(beacon, 'on_sync_errors') as mock_on_sync_errors:
            # Trigger notification
            with beacon.changing_state():
                pass
            
            # Verify normal observer was still called
            assert normal_observer.called is True   #type: ignore
            
            # Verify on_sync_errors was called with both errors
            assert mock_on_sync_errors.call_count == 1
            errors = mock_on_sync_errors.call_args[0][0]
            assert len(errors) == 2
            
            # Check first error
            assert isinstance(errors[0][1], ValueError)
            assert str(errors[0][1]) == "Error 1"
            
            # Check second error
            assert isinstance(errors[1][1], TypeError)
            assert str(errors[1][1]) == "Error 2"


class TestObserverManagement:
    """Tests for adding, removing, and checking observers."""

    def test_add_observer_all_types(self):
        """Test that adding observers of all supported types works correctly."""
        beacon = Beacon()
        
        # Regular function
        def function(sender):
            pass
        
        # Create a class with various method types
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
                
            @classmethod
            def class_method(cls, sender):
                pass
                
            def instance_method(self, sender):
                pass
        
        # Create an instance for instance method
        instance = TestClass()
        
        # Test adding each type of observer
        assert beacon.add_observer(function) is True
        assert beacon.add_observer(TestClass.static_method) is True
        assert beacon.add_observer(TestClass.class_method) is True
        assert beacon.add_observer(instance.instance_method) is True
        
        # Verify all observers are present
        assert beacon.is_being_observed(function) is True
        assert beacon.is_being_observed(TestClass.static_method) is True
        assert beacon.is_being_observed(TestClass.class_method) is True
        assert beacon.is_being_observed(instance.instance_method) is True
        
        # Check the total number of observers
        assert len(beacon._observers) == 4
    
    def test_add_duplicate_observers_all_types(self):
        """Test that adding already present observers of all types returns False."""
        beacon = Beacon()
        
        # Regular function
        def function(sender):
            pass
        
        # Create a class with various method types
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
                
            @classmethod
            def class_method(cls, sender):
                pass
                
            def instance_method(self, sender):
                pass
        
        # Create an instance for instance method
        instance = TestClass()
        
        # Add each type of observer first
        beacon.add_observer(function)
        beacon.add_observer(TestClass.static_method)
        beacon.add_observer(TestClass.class_method)
        beacon.add_observer(instance.instance_method)
        
        # Adding again should return False for all types
        assert beacon.add_observer(function) is False
        assert beacon.add_observer(TestClass.static_method) is False
        assert beacon.add_observer(TestClass.class_method) is False
        assert beacon.add_observer(instance.instance_method) is False
    
    def test_remove_observer_all_types(self):
        """Test that removing observers of all types works correctly."""
        beacon = Beacon()
        
        # Regular function
        def function(sender):
            pass
        
        # Create a class with various method types
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
                
            @classmethod
            def class_method(cls, sender):
                pass
                
            def instance_method(self, sender):
                pass
        
        # Create an instance for instance method
        instance = TestClass()
        
        # Add each type of observer first
        beacon.add_observer(function)
        beacon.add_observer(TestClass.static_method)
        beacon.add_observer(TestClass.class_method)
        beacon.add_observer(instance.instance_method)
        
        # Removing each should return True
        assert beacon.remove_observer(function) is True
        assert beacon.remove_observer(TestClass.static_method) is True
        assert beacon.remove_observer(TestClass.class_method) is True
        assert beacon.remove_observer(instance.instance_method) is True
        
        # Observers should no longer be present
        assert beacon.is_being_observed(function) is False
        assert beacon.is_being_observed(TestClass.static_method) is False
        assert beacon.is_being_observed(TestClass.class_method) is False
        assert beacon.is_being_observed(instance.instance_method) is False
        
        # Check the total number of observers is now 0
        assert len(beacon._observers) == 0
    
    def test_remove_nonexistent_observer_all_types(self):
        """Test that removing non-existent observers of all types returns False."""
        beacon = Beacon()
        
        # Regular function
        def function(sender):
            pass
        
        # Create a class with various method types
        class TestClass:
            @staticmethod
            def static_method(sender):
                pass
                
            @classmethod
            def class_method(cls, sender):
                pass
                
            def instance_method(self, sender):
                pass
        
        # Create an instance for instance method
        instance = TestClass()
        
        # Removing observers that were never added should return False for all types
        assert beacon.remove_observer(function) is False
        assert beacon.remove_observer(TestClass.static_method) is False
        assert beacon.remove_observer(TestClass.class_method) is False
        assert beacon.remove_observer(instance.instance_method) is False
    
    def test_lambda_handling(self):
        """Test lambda function handling."""
        beacon = Beacon()
        
        # Test add_observer with a lambda - should raise TypeError
        lambda_fn = lambda sender: None     #noqa: E731
        with pytest.raises(TypeError) as excinfo:
            beacon.add_observer(lambda_fn)
        assert str(excinfo.value) == _ErrorMessages.LAMBDA_NOT_SUPPORTED
        
        # Test remove_observer with a lambda - should just return False, not raise
        assert beacon.remove_observer(lambda_fn) is False
        
        # Test is_being_observed with a lambda - should return False, not raise
        assert beacon.is_being_observed(lambda_fn) is False
    
    def test_notification_all_types(self):
        """Test notification of all observer types."""
        beacon = Beacon()
        
        # Track which observers were called
        function_called = False
        static_called = False
        class_called = False
        instance_called = False
        
        # Store the received senders to verify they are passed correctly
        function_sender = None
        static_sender = None
        class_sender = None
        instance_sender = None
        
        # Regular function
        def function(sender):
            nonlocal function_called, function_sender
            function_called = True
            function_sender = sender
        
        # Create a class with various method types
        class TestClass:
            @staticmethod
            def static_method(sender):
                nonlocal static_called, static_sender
                static_called = True
                static_sender = sender
                
            @classmethod
            def class_method(cls, sender):
                nonlocal class_called, class_sender
                class_called = True
                class_sender = sender
                
            def instance_method(self, sender):
                nonlocal instance_called, instance_sender
                instance_called = True
                instance_sender = sender
        
        # Create an instance for instance method
        instance = TestClass()
        
        # Add all types of observers
        beacon.add_observer(function)
        beacon.add_observer(TestClass.static_method)
        beacon.add_observer(TestClass.class_method)
        beacon.add_observer(instance.instance_method)
        
        # Make a state change to trigger notification
        with beacon.changing_state():
            pass
        
        # Verify all observers were called
        assert function_called is True
        assert static_called is True
        assert class_called is True
        assert instance_called is True
        
        # Verify the sender was passed correctly to all observers
        assert function_sender is beacon
        assert static_sender is beacon
        assert class_sender is beacon
        assert instance_sender is beacon
    
    def test_sender_parameter_with_context_managers(self):
        """Test that sender is passed correctly with different context managers."""
        # Test with changing_state
        beacon1 = Beacon()
        sender_received1 = None
        
        def callback1(sender):
            nonlocal sender_received1
            sender_received1 = sender
        
        beacon1.add_observer(callback1)
        with beacon1.changing_state():
            pass
        
        assert sender_received1 is beacon1
        
        # Test with batch_changing_state
        beacon2 = Beacon()
        sender_received2 = None
        
        def callback2(sender):
            nonlocal sender_received2
            sender_received2 = sender
        
        beacon2.add_observer(callback2)
        with beacon2.batch_changing_state():
            pass
        
        assert sender_received2 is beacon2
        
        # Test with changing_state_without_notification
        beacon3 = Beacon()
        sender_received3 = None
        callback3_called = False
        
        def callback3(sender):
            nonlocal sender_received3, callback3_called
            sender_received3 = sender
            callback3_called = True
        
        beacon3.add_observer(callback3)
        with beacon3.changing_state_without_notification():
            pass
        
        # Callback should not be called, so sender should remain None
        assert callback3_called is False
        assert sender_received3 is None
    
    def test_cleanup_stale_observers(self):
        """Test that stale observers are properly cleaned up."""
        beacon = Beacon()
        
        # Create a class that will be used for testing
        class TestClass:
            def instance_method(self, sender):
                pass
        
        # Create an instance and register its method
        instance = TestClass()
        beacon.add_observer(instance.instance_method)
        
        # Verify the observer is present
        assert len(beacon._observers) == 1
        
        # Delete the instance to make the observer stale
        del instance
        gc.collect()
        
        # Trigger the cleanup mechanism by making a state change
        with beacon.changing_state():
            pass
        
        # Verify the stale observer was cleaned up
        assert len(beacon._observers) == 0
    
    def test_async_notification(self):
        """Test that async notification works properly."""
        # Create a new event loop instead of trying to get the current one
        loop = asyncio.new_event_loop()
    
        try:
            # Set the new loop as the current event loop
            asyncio.set_event_loop(loop)
        
            beacon = Beacon()
            callback_called = False
            sender_received = None
        
            def callback(sender):
                nonlocal callback_called, sender_received
                callback_called = True
                sender_received = sender
        
            beacon.add_observer(callback)
        
            # Run the async notification in the event loop
            async def run_test():
                with beacon.changing_state():
                    pass
            
                # Small delay to ensure the callback has been processed
                await asyncio.sleep(0.01)
        
            loop.run_until_complete(run_test())
        
            # Verify the callback was called and received the correct sender
            assert callback_called is True
            assert sender_received is beacon
        finally:
            # Clean up: close the loop and reset the event loop policy
            loop.close()
            asyncio.set_event_loop(None)


class TestContextManagers:
    """Test the various context managers provided by the Beacon class."""
    
    def test_changing_state(self):
        """Test the changing_state context manager."""
        called = [False]
        
        def observer(sender):
            called[0] = True
        
        beacon = Beacon()
        beacon.add_observer(observer)
        
        # State change should trigger notification
        with beacon.changing_state():
            pass
        
        assert called[0] is True
        
    def test_changing_state_without_notification(self):
        """Test the changing_state_without_notification context manager."""
        called = [False]
        
        def observer(sender):
            called[0] = True
        
        beacon = Beacon()
        beacon.add_observer(observer)
        
        # State change without notification should not trigger
        with beacon.changing_state_without_notification():
            pass
        
        assert called[0] is False
        
    def test_batch_changing_state(self):
        """Test the batch_changing_state context manager."""
        call_count = [0]
        
        def observer(sender):
            call_count[0] += 1
        
        beacon = Beacon()
        beacon.add_observer(observer)
        
        # Batch operation should trigger exactly one notification
        with beacon.batch_changing_state():
            # These would normally trigger separate notifications
            pass
        
        assert call_count[0] == 1
    
    def test_nested_context_managers(self):
        """Test nested context managers to ensure proper behavior."""
        call_count = [0]
        
        def observer(sender):
            call_count[0] += 1
        
        beacon = Beacon()
        beacon.add_observer(observer)
        
        # Test: changing_state containing batch_changing_state
        with beacon.changing_state():
            # This inner batch operation shouldn't trigger a notification
            with beacon.batch_changing_state():
                pass
        
        # Just one notification from the outer changing_state
        assert call_count[0] == 1
        
        # Reset counter
        call_count[0] = 0
        
        # Test: batch_changing_state containing changing_state
        with beacon.batch_changing_state():
            # This inner state change shouldn't trigger a notification
            with beacon.changing_state():
                pass
        
        # Just one notification from the outer batch_changing_state
        assert call_count[0] == 1
        
        # Reset counter
        call_count[0] = 0
        
        # Test: changing_state_without_notification containing changing_state
        with beacon.changing_state_without_notification():
            # This inner state change shouldn't trigger a notification
            # since notifications are on hold
            with beacon.changing_state():
                pass
        
        # No notifications should have occurred
        assert call_count[0] == 0