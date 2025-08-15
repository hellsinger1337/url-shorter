#!/bin/sh

echo "DEBUG: PYTHONPATH=$PYTHONPATH"
echo "DEBUG: Listing /app"
ls -la /app
echo "DEBUG: Listing /app/src"
ls -la /app/src
echo "DEBUG: python -c 'import sys; print(sys.path)'"
python -c "import sys; print(sys.path)"

exec "$@"
