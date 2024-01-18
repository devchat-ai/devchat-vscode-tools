#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ABSOLUTE_PATH2="$DIR/site-packages/openai/_types.py"
NETWORKX_ATLAS="$DIR/site-packages/networkx/generators/atlas.py"

# sed -i '' 's|FileContent = Union\[IO\[bytes\], bytes, PathLike\[str\]\]|FileContent = Union\[IO\[bytes\], bytes, PathLike\]|' "$ABSOLUTE_PATH2"	

sed -i '' 's|importlib\.resources|importlib_resources|' "$NETWORKX_ATLAS"	

