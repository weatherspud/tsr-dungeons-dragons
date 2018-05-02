stats:
	./stats.py --input-path products.csv --stats year system type setting

ve:
	virtualenv ve
	. ve/bin/activate && pip install -r requirements.txt

src_files := $(wildcard *.py)

pycodestyle:
	. ve/bin/activate && echo $(src_files) | xargs pycodestyle --max-line-length=120

pylint:
	. ve/bin/activate && echo $(src_files) | xargs pylint -E

check: pycodestyle pylint
