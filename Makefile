clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-pycache:
	find . -name "__pycache__" -exec rm -rf {} +


cleanup: clean-pycache clean-pyc

.PHONY: clean-pyc \
		clean