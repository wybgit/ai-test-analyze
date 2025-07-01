#!/bin/bash

# build.sh - A script to package the ai-test-analyze project into a wheel file.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Banner ---
echo "========================================="
echo "  Building ai-test-analyze Wheel Package "
echo "========================================="

# --- Clean up old builds ---
echo "Cleaning up old build artifacts..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
echo "Cleanup complete."

# --- Build the wheel ---
echo "Building the wheel package..."
python3 setup.py sdist bdist_wheel

# --- List the output ---
echo "Build process complete. Generated files:"
ls -l dist/

echo "========================================="
echo "  Package created successfully!          "
echo "========================================="
echo "You can now install the package using:"
echo "pip install dist/$(ls dist | grep .whl)"
echo ""
