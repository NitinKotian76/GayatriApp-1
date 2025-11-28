#!/bin/bash

set -e

if ["$1"='test']; then
	./test.sh
else
	./deploy.sh
fi
