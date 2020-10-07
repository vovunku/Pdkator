# Pdkator

Tool for converting nondeterministic finite automaton with one letter transitions and without epsilon edges to:
1) deterministic finite automaton 
2) complete deterministic finite automaton
3) minimal complete deterministic finite automaton


## How to use?
Just run main.py in interactive way or with input file. For example:
```shell script
cat tests/test2.txt | python3 pdkator.py > result.txt
```
or for interactive just
```shell script
python3 pdkator.py
```
Example of output:
```
********************
Total 8 vertexes
Start vertex is - {1}
Terminal vertexes: {{3, 5}, {3, 4, 5}, {5}}
Edges: format from -letter-> to1 | to2 ...
----------
{1} -a-> {3}
{1} -b-> 'dummy'
----------
{3} -a-> {4}
{3} -b-> {5}
----------
{4} -a-> 'dummy'
{4} -b-> {3}
----------
{3, 5} -a-> {3, 4, 5}
{3, 5} -b-> {5}
----------
{6} -a-> {5}
{6} -b-> 'dummy'
----------
{3, 4, 5} -a-> {3, 4, 5}
{3, 4, 5} -b-> {3, 5}
----------
{5} -a-> {3, 5}
{5} -b-> {6}
----------
dummy -a-> 'dummy'
dummy -b-> 'dummy'
********************
```

## Tests
To run tests:
```shell script
python3 unit_tests.py
```

## Coverage
To get coverage
```shell script
coverage run -m unittest discover
coverage html
open htmlcov/index.html
```