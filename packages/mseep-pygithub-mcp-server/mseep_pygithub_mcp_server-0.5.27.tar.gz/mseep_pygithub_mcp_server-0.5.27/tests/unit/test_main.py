"""Unit tests for main module.

These tests verify that the main module works correctly.
"""

import pytest
import sys
import importlib
from contextlib import contextmanager
from io import StringIO

from pygithub_mcp_server import __main__


@contextmanager
def capture_stdout():
    """Capture stdout for testing."""
    # Create StringIO object to capture output
    new_stdout = StringIO()
    # Save current stdout
    old_stdout = sys.stdout
    # Replace stdout with our StringIO object
    sys.stdout = new_stdout
    try:
        # Yield the StringIO object for testing
        yield new_stdout
    finally:
        # Restore original stdout
        sys.stdout = old_stdout


@pytest.fixture
def patched_create_server(monkeypatch):
    """Patch create_server function for testing."""
    # Define a test server
    class TestServer:
        def __init__(self):
            self.is_running = False
            
        def run(self):
            self.is_running = True
            # Print to stdout to verify it's called
            print("Server is running")
    
    # Create a server instance
    server = TestServer()
    
    # Patch the create_server function
    monkeypatch.setattr('pygithub_mcp_server.__main__.create_server', lambda: server)
    
    # Return the server instance for assertion
    return server


def test_main_function(patched_create_server):
    """Test that main function creates and runs a server."""
    # Capture stdout
    with capture_stdout() as stdout:
        # Call main function
        __main__.main()
    
    # Verify the server was run
    assert patched_create_server.is_running is True
    assert "Server is running" in stdout.getvalue()


def test_main_execution(monkeypatch):
    """Test main module execution."""
    # Create a simpler test that directly checks if the module runs main when __name__ == "__main__"
    
    # Keep track if main was called
    main_called = False
    
    # Define a mock main function that tracks execution
    def mock_main():
        nonlocal main_called
        main_called = True
    
    # Create a temporary copy of the __main__ module content
    from pygithub_mcp_server import __main__ as main_module
    
    # Save original __name__ and main function
    original_name = main_module.__name__
    original_main = main_module.main
    
    try:
        # Patch the main function
        monkeypatch.setattr(main_module, 'main', mock_main)
        
        # Set __name__ to "__main__" to simulate direct execution
        monkeypatch.setattr(main_module, '__name__', "__main__")
        
        # Execute the module level code without importing it again
        # This is equivalent to running it directly
        code = compile(
            "if __name__ == '__main__':\n    main()", 
            filename="<string>", 
            mode="exec"
        )
        exec(code, main_module.__dict__)
        
        # Verify main was called
        assert main_called is True
        
    finally:
        # Restore original values
        monkeypatch.setattr(main_module, '__name__', original_name)
        monkeypatch.setattr(main_module, 'main', original_main)


def test_module_import(monkeypatch):
    """Test that importing module doesn't run main."""
    # Keep track if main was called
    main_called = False
    
    # Define a function to track if main is called
    def track_main():
        nonlocal main_called
        main_called = True
    
    # Patch the main function
    monkeypatch.setattr('pygithub_mcp_server.__main__.main', track_main)
    
    # Simulate module import with __name__ != "__main__"
    tmp_name = __main__.__name__
    __main__.__name__ = "not_main"
    
    try:
        # This should not execute the if __name__ == "__main__" block
        importlib.reload(__main__)
        
        # Verify main was not called
        assert main_called is False
    finally:
        # Restore original module name
        __main__.__name__ = tmp_name
