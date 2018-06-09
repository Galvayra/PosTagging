clean:
	rm -r __pycache__
	rm -r data/__pycache__

clean-dict:
	rm -r data/dict/*

clean-dataset:
	rm -r data/data/*

clean-all:
	rm -r data/dict/*
	rm -r data/data/*
