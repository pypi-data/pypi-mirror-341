# ksiterate
Python module for iteration over product of given parameter values

# Description

This library provides a class *Iteration*, which implements iteration over a product of given parameters.

Example 1:
```python
itspec = [
	{
		'A':[1, 2, 3],
		'B':[10, 11, 12],
		'C':[20, 21]
	},
	];


it = ksiterate.Iteration(itspec);

for i in it.iterate():
	print(i);
```
This code ireates over every possible combination of values defined for parameters *A*, *B* anc *C*: (1, 10, 20), (1, 10, 21), (1, 11, 20), ...

It is also possible to split the iteration into inner/outer loops:
```python
for i in it.iterate(include_params={"C",}):
	print(i);
	for j in it.iterate(i,):
		print(j);
```
This code iterates over *C* in the outer loop and over the rest of parameters in the inner loop.

Multiple parameter specifications may be included:
```python
itspec = [
	{
		'A':[1, 2, 3],
		'B':[10, 11, 12],
		'C':[20, 21]
	},
	{
		'A':[5, 6,],
		'B':[10, 11],
		'C':[22, 23]
	}
	];


it = ksiterate.Iteration(itspec);

for i in it.iterate():
	print(i);
```
In this case, the iteration would account for sum of two products of combinations from first dictionary and from second dictionary.
