#!/usr/bin/env python3
"""
This script checks routes in a FastAPI application.
"""

import sys
import importlib.util
import inspect
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter

def load_module_from_file(file_path, module_name="dynamic_module"):
    """Load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        print(f"Could not load spec for {file_path}")
        return None
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def print_route_info(app: FastAPI):
    """Print information about all routes defined in the FastAPI app."""
    print(f"FastAPI Application: {app}")
    print(f"Title: {app.title}")
    print(f"Description: {app.description}")
    print("=" * 50)
    print("Routes:")
    
    def print_routes(routes, prefix=""):
        for route in routes:
            if isinstance(route, APIRoute):
                print(f"  {prefix}{route.path}")
                print(f"    Methods: {', '.join(route.methods)}")
                print(f"    Name: {route.name}")
                print(f"    Endpoint: {route.endpoint.__name__}")
                print(f"    From module: {route.endpoint.__module__}")
                print(f"    Summary: {route.summary}")
                print(f"    Description: {route.description}")
                print("    ---")
            elif isinstance(route, APIRouter):
                print(f"  Router: {route.prefix}")
                print_routes(route.routes, prefix=prefix + route.prefix)
    
    print_routes(app.routes)

def find_fastapi_app(module):
    """Find a FastAPI application instance in a module."""
    for name, obj in inspect.getmembers(module):
        if isinstance(obj, FastAPI):
            return obj
    return None

def main():
    """Main function to check FastAPI routes."""
    # Check both possible main.py files
    app_file = "/Users/douglaskahn/Documents/job-tracker/app/main.py"
    backend_file = "/Users/douglaskahn/Documents/job-tracker/backend/main.py"
    
    # Load app main.py
    print("Checking app/main.py...")
    app_module = load_module_from_file(app_file, "app_main")
    if app_module:
        app_instance = find_fastapi_app(app_module)
        if app_instance:
            print_route_info(app_instance)
        else:
            print("No FastAPI instance found in app/main.py")
    else:
        print("Failed to load app/main.py")
    
    print("\n" + "=" * 70 + "\n")
    
    # Load backend main.py
    print("Checking backend/main.py...")
    backend_module = load_module_from_file(backend_file, "backend_main")
    if backend_module:
        backend_instance = find_fastapi_app(backend_module)
        if backend_instance:
            print_route_info(backend_instance)
        else:
            print("No FastAPI instance found in backend/main.py")
    else:
        print("Failed to load backend/main.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
