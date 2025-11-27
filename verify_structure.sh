#!/bin/bash
set -e

# Standard MCP Server Setup Pattern
# Validates structure before and after manual file additions

PROJECT_NAME="constellation-composition-mcp"
PACKAGE_NAME="constellation_composition_mcp"

echo "Verifying structure for ${PROJECT_NAME}..."
echo ""

ERRORS=0
WARNINGS=0

# Check required directories
echo "Checking directories..."
REQUIRED_DIRS=(
    "src/${PACKAGE_NAME}"
    "tests"
    "docs"
    "examples"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir (missing)"
        ((ERRORS++))
    fi
done
echo ""

# Check required files
echo "Checking required files..."
REQUIRED_FILES=(
    "pyproject.toml"
    "README.md"
    "LICENSE"
    ".gitignore"
    "src/${PACKAGE_NAME}/__init__.py"
    "src/${PACKAGE_NAME}/__main__.py"
    "tests/__init__.py"
    "tests/run_tests.sh"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        ((ERRORS++))
    fi
done
echo ""

# Check large files that should be added manually
echo "Checking large files (should be added manually)..."
LARGE_FILES=(
    "src/${PACKAGE_NAME}/server.py"
)

for file in "${LARGE_FILES[@]}"; do
    if [ -f "$file" ]; then
        size=$(wc -l < "$file" 2>/dev/null || echo "0")
        echo "  ✓ $file (${size} lines)"
    else
        echo "  ⚠ $file (not yet added - add manually)"
        ((WARNINGS++))
    fi
done
echo ""

# Check test executability
echo "Checking test runner..."
if [ -x "tests/run_tests.sh" ]; then
    echo "  ✓ tests/run_tests.sh is executable"
else
    echo "  ✗ tests/run_tests.sh is not executable"
    ((ERRORS++))
fi
echo ""

# Validate pyproject.toml
echo "Validating pyproject.toml..."
if python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))" 2>/dev/null; then
    echo "  ✓ pyproject.toml is valid TOML"
else
    echo "  ✗ pyproject.toml has syntax errors"
    ((ERRORS++))
fi
echo ""

# Check Python syntax for existing files
echo "Checking Python syntax..."
for file in src/${PACKAGE_NAME}/*.py tests/*.py; do
    if [ -f "$file" ]; then
        if python -m py_compile "$file" 2>/dev/null; then
            echo "  ✓ $file"
        else
            echo "  ✗ $file (syntax error)"
            ((ERRORS++))
        fi
    fi
done
echo ""

# Summary
echo "═══════════════════════════════════════"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ Structure verification PASSED"
    echo "   Ready for: pip install -e '.[dev]'"
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  Structure verification PASSED with warnings"
    echo "   Warnings: $WARNINGS (large files not yet added)"
    echo "   Add server.py manually, then re-run verification"
else
    echo "❌ Structure verification FAILED"
    echo "   Errors: $ERRORS"
    echo "   Warnings: $WARNINGS"
    echo "   Fix errors before proceeding"
    exit 1
fi
echo "═══════════════════════════════════════"
echo ""
