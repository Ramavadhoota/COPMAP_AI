#!/bin/bash
cd /workspaces/COPMAP_AI/copmap-poc
echo "=== Checking installed packages ==="
pip list 2>&1 | grep -E "torch|transformers|sentence|chromadb|numpy" || echo "Running pip list..."
pip list 2>&1 | tail -20

echo ""
echo "=== Testing imports ==="
python3 << 'EOF'
try:
    import numpy
    print(f"✓ numpy {numpy.__version__}")
except ImportError as e:
    print(f"✗ numpy: {e}")

try:
    import torch
    print(f"✓ torch {torch.__version__}")
except ImportError as e:
    print(f"✗ torch: {e}")

try:
    import transformers
    print(f"✓ transformers {transformers.__version__}")
except ImportError as e:
    print(f"✗ transformers: {e}")

try:
    import sentence_transformers
    print(f"✓ sentence-transformers {sentence_transformers.__version__}")
except ImportError as e:
    print(f"✗ sentence-transformers: {e}")

try:
    import chromadb
    print(f"✓ chromadb installed")
except ImportError as e:
    print(f"✗ chromadb: {e}")
EOF
