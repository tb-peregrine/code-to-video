.PHONY: install test clean demo help

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

install-dev:  ## Install in development mode with dev tools
	pip install -r requirements.txt -r requirements-dev.txt
	pip install -e .

test:  ## Run tests
	python test_utility.py

demo:  ## Generate demo video from example.md
	python code_to_video.py example.md demo.mp4 --typing-speed 40 --font-size 18

demo-fast:  ## Generate demo video with fast typing
	python code_to_video.py example.md demo-fast.mp4 --typing-speed 80 --font-size 16

demo-light:  ## Generate demo video with light theme
	python code_to_video.py example.md demo-light.mp4 --theme light --typing-speed 40

clean:  ## Clean up generated files
	rm -f *.mp4
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/

package:  ## Build package for distribution
	python setup.py sdist bdist_wheel

lint:  ## Run linting with flake8
	@if [ -f venv/bin/activate ]; then \
		source venv/bin/activate && flake8 code_to_video.py test_utility.py --max-line-length=100; \
	else \
		flake8 code_to_video.py test_utility.py --max-line-length=100; \
	fi

format:  ## Format code with autopep8
	@if [ -f venv/bin/activate ]; then \
		source venv/bin/activate && autopep8 --in-place --aggressive --max-line-length=100 *.py; \
	else \
		autopep8 --in-place --aggressive --max-line-length=100 *.py; \
	fi 