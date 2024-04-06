format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./logger
	source ./venv/bin/activate && isort ./logger
	source ./venv/bin/activate && black ./logger
