n = 5
l = 50
run_test:
	python .\tests\TestAnyLength.py -ng $n -l $l

run_all:
	python .\tests\TestAnyLength.py -ng 5 -l 50
	python .\tests\TestAnyLength.py -ng 5 -l 100
	python .\tests\TestAnyLength.py -ng 5 -l 500
	python .\tests\TestAnyLength.py -ng 5 -l 1000
	python .\tests\TestAnyLength.py -ng 5 -l 5000
