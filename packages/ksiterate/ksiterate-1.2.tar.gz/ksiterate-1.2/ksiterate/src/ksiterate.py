#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################################################################### 
#   Copyright 2021 Konrad Sakowski
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
####################################################################################
import itertools
import pandas

class Iteration(object):
	internal_params = set(["index",]);
	def __init__(self, itspec, only = {}):
		"""
			A class implementing iteration over products of given parameters.

			Variable *itspec* is a list of dictionaries. Every dictionary shall have parameter names as a keys and lists of parameter values as the corresponding dictionary values. Then, this class allows to iterate over product of every combination of given parameter values.
			Alternatively, it is possible to pass a tuple of parameter names as dictionary key, and then a list of tuples/lists as a dictionary value. Then, in the iteration these values will be coupled, as indicated by the tuples/lists given as the dictionary value.

			Additionally, it is possible to pass *only* variable to limit parameters given as dictionary keys to values from lists given as corresponding dictionary values.
		"""
		self.iteras = [];
		self.df = pandas.DataFrame();
		index=0;
		for params in itspec:
			# przygotowanie zadań na podstawie parametrów
			keys=params.keys();
			itlist=[params[k] for k in keys];
			#print(itlist)
			#print(keys, list(itertools.product(*itlist)))
			rows0 = itertools.product(*itlist);

			columns = [];
			for key in keys:
				if(type(key) is not tuple):
					columns.append(key);
				else:
					for inner_key in key:
						columns.append(inner_key);

			rows=[];
			for row0 in rows0:
				row = [];
				for key, val in zip(keys, row0):
					if(type(key) is not tuple):
						row.append(val);
					else:
						for inner_val in val:
							row.append(inner_val);
				rows.append(row);

			#print(columns);
			#print(rows);
			self.df = pandas.concat([self.df, pandas.DataFrame(rows, columns=columns)], ignore_index=True);

		for key, vals in only.items():
			self.df = self.df[self.df[key].isin(vals)];

		self.df.drop_duplicates(inplace=True, ignore_index=True);
		self.df = self.df.where(self.df.notnull(), None); # zamiana NaN'ów na None

		assert self.internal_params & set(self.df.columns) == set(), "Internal parameter names cannot be used in parameter specification"; 

		# setup internal parameters below

		self.df['index'] = range(1, len(self.df) + 1)

		#print(self.df)


	def iterate(self, otera={}, ignore_params=[], include_params = None):
		"""
			This function iterates over unique combinations of parameter values.

			By setting either *ignore_params* or *include_params*, the certain parameters may be excluded from (or included in) the iteration. This may be used to iterate over parameters in certain sequence. In that case, to further iterate over parameters not included in iteration, this function may be used, with *otera* parameter set to dictionary returned by this function. Then, the remaining parameter values will be iterated, corresponding to former parameter values given by *otera*. This pattern may be nested.
		"""

		all_params = set(self.df.columns);
		ignore_params = set(ignore_params);
		iterated_params = set(otera.keys()) & all_params; # mogą być jeszcze jakieś inne elementy w otera, które nie są parametrami;

		if(include_params is not None):
			assert len(ignore_params)==0, "ignore_params and include_params cannot be used simultaneously";
			include_params = set(include_params);
		else:
			assert ignore_params & iterated_params == set(), "Cannot ignore already iterated parameters"; 
			include_params = all_params - iterated_params - ignore_params;

		assert iterated_params & include_params == set(), "Cannot include already iterated parameters"; 

		dg = self.df;
		#print("self.df\n", dg);

		for key in iterated_params:
			val = otera[key];

			#print(key);

			dg = dg[dg[key] == val];

		#print("dg\n", dg);
		iterated_and_included_params = iterated_params | include_params;
		if(iterated_and_included_params != all_params): # parametry wewnętrzne, jak index, dodajemy dopiero jak są uwzględnione wszystkie parametry iteracji, nie wcześniej
			iterated_and_included_params -= self.internal_params;

		dh = dg[list(iterated_and_included_params)].copy();
		dh.drop_duplicates(inplace=True, ignore_index=True);

		#print("dh\n", dh);

		iteras = dh.to_dict(orient='records');
		for itera in iteras:
			yield itera; 


	def len(self):
		"""
			This function returns the number of combinations.
		"""
		return len(self.df);
