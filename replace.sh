#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ABSOLUTE_PATH2="$DIR/site-packages/openai/_types.py"

sed -i '' 's|FileContent = Union\[IO\[bytes\], bytes, PathLike\[str\]\]|FileContent = Union\[IO\[bytes\], bytes, PathLike\]|' "$ABSOLUTE_PATH2"	
