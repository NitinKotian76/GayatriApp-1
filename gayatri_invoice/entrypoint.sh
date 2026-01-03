#!/bin/bash

set -e

if [ "$TEST" = "test" ]; then
	exec ./test.sh
else
	exec ./deploy.sh
fi
