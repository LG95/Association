def associate(records, attributes, minsupport, minconfidence):
	"""
	Generate association rules for the given data respecting minsupport and
	minconfidence.

	Return the frequent itemsets and the association rules.

	Input:
		records - dataset for which association rules are to be found;
		attributes - record attribute description used to find possible items;
		minsupport - minimum support for an itemset;
		minconfidence - minimum confidence for a rule. 
	"""

	# set of items possibly present in records
	items = map(lambda p: p[0], attributes)
	minsupport *= len(items) # multiply minsupport by the number of items
	# find the frequent itemsets
	frequent = generate_frequent(items, minsupport, records)
	# find the rules for the frequent itemsets
	rules = generate_rules(frequent, minconfidence, records)

	return frequent, rules

def generate_frequent(items, minsupport, records):
	"""
	Generate frequent itemsets using the Apriori algorithm.

	Return the frequent itemsets.

	Input:
		items - set of items present in the dataset;
		minsupport - lowest value of support an itemset should have;
		records - dataset used to find frequent itemsets.
	"""

	# itemset of the current (k-th) iteration
	current = list( map(lambda i: [i], items) )
	itemsets = []	# set of frequent itemsets paired with their support
	k = 1 # size of each itemset in current

	while current != []:
		print('\nk = ' + str(k) + ':'),
		print(str( len(current) ) + ' candidate itemsets before pruning and'),

		# discard pairs whose support is below minsupport
		current = filter(lambda its: support(its, records) >= minsupport, current)

		print(str( len(current) ) + ' candidate itemsets after pruning.')
		print('Candidates (after pruning)')
		for itemset in current:
			print(itemset)
		k += 1 # update k
		
		itemsets.extend(current)	# add the current to itemsets
		# generate itemsets with k + 1 elements from current
		current = apriori_generate(current)

	return itemsets

def support(itemset, records):
	"""
	Calculates the itemset's support based on records.

	Return the support.

	Input:
		itemset - set of items whose support will be calculated;
		record - set of records containing items from itemset. 
	"""

	support = 0	# itemset's support

	for record in records:
		items = iter(itemset)	# iterator on itemset
		present = True	# record has every item in itemset

		try:
			while present:	# record has every item already checked
				# check whether record has the next item
				present = record[ items.next() ]

		except StopIteration:	# all items checked
			support += 1	# update support

	return support


def apriori_generate(itemsets):
	"""
	Generate a set of itemsets, each with one more element than the itemsets in
	the given set. Uses the Fk-1 x Fk-1 approach.

	Return the new set.

	Input:
		itemsets - set of itemsets used to generate the new set.
	"""

	new = []	# set of itemsets with one more item each

	for i, a in enumerate(itemsets):	# each itemset and its index
		for b in itemsets[i + 1:]:	# each itemset not run against a
			# a and b differ only in their last elements
			if a[:-1] == b[:-1] and a[-1] != b[-1]:
				# add the itemset with the same prefix as a (and b) and with 
				# a's and b's last elements to new
				new.append(a[:-1] + [a[-1], b[-1]])

	return new

def generate_rules(itemsets, minconfidence, records):
	"""
	Generate rules using the Apriori algorithm.

	Return the set of generated rules.

	Input:
		itemsets - frequent itemsets from which the rules will be generated;
		minconfidence - lowest value of confidence a rule should have;
		records - set of records used when calculating support.
	"""

	rules = [] # the generated rules

	# each itemset with at least two items
	for itemset in filter(lambda its: len(its) >= 2, itemsets):
		# set of initial consequents used to generate rules
		consequents = [ [i] for i in itemset ]
		# generated rules for itemset
		generated = apriori_genrules(itemset, consequents, minconfidence, records)
		# add the rules generated for itemset to rules
		rules.extend(generated)

	return rules

def apriori_genrules(itemset, consequents, minconfidence, records):
	"""
	Generate rules for the given itemset and consequents.

	Return the rules generated.

	Input:
		itemset - itemset used to generate rules;
		consequents - non-empty set of right-hand side candidates for the
	generated rules;
		minconfidence - lowest value of confidence a rule should have;
		records - set of records used when calculating support.
	"""

	rules = []	# set of generated rules
	k = len(itemset) # number of elements in each itemset

	# the next rules will not have empty antecedent or consequent
	while consequents != [] and k > (len(consequents[0]) + 1):
		# set of consequents used to generate the next iteration's consequents
		next_consequents = consequents[:]

		for consequent in reversed(consequents):	# each consequent
			# find the antecedent (itemset - consequent)
			antecedent = list( filter(lambda i: i not in consequent, itemset) )

			# calculate the rule's confidence
			confidence = float( support(itemset, records) )
			confidence /= support(antecedent, records)

			# the generated rule has enough confidence
			if confidence >= minconfidence:
				# add the rule, antecedent consequent pair, to rules
				rules.append( (antecedent, consequent) )

			else:	
				# remove this consequent from next_consequents
				next_consequents.remove(consequent)

			# add one item to each element in next_consequents
			consequents = apriori_generate(next_consequents)
		
	return rules