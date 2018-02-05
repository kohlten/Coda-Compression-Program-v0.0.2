.PHONY: all

all:
	python "setup.py" "coda.py"
	python "setup.py" "folder.py"
	python "setup.py" "extract.py"

.PHONY: clean

clean:
	rm -Rf build

.PHONY: fclean

fclean:
	make clean
	rm -Rf dist

.PHONY: re

re:
	make fclean
	make all
