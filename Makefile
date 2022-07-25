n = 5
l = 50
run_test:
	python .\Test\TestAnyLength.py -ng $n -l $l

run_all:
	python .\Test\TestAnyLength.py -ng 5 -l 50
	python .\Test\TestAnyLength.py -ng 5 -l 100
	python .\Test\TestAnyLength.py -ng 5 -l 500
	python .\Test\TestAnyLength.py -ng 5 -l 1000
	python .\Test\TestAnyLength.py -ng 5 -l 5000
