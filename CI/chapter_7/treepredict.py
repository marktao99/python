import collections

my_data=[line.split("\t") for line in file("decision_tree_example.txt")]
class decisionnode:
	def _init__(self,col=-1,value=None,results=None,tb=None,fb=None):
		self.col=col
		self.value=value
		self.results=results
		self.tb=tb
		self.fb=fb
def divideset(rows,column,value):
	split_function=None
	if isinstance(value,int) or isinstance(value,float):
		split_function=lambda row: row[column]>=value
	else:	
		split_function=lambda row: row[column]==value
		
	set1=[row for row in rows if split_function(row)]
	set2=[row for row in rows if not split_function(row)]
	return (set1,set2)

def uniquecounts(rows):
	results={}
	for row  in rows:
		r=row[len(row)-1]
		if r not in results:
			results[r]=0
		results[r]+=1
	return results

def giniimpurity(rows):
	total=len(rows)
	counts=uniquecounts(rows)
	imp=0
	for k1 in counts:
		p1=float(counts[k1])/total
		for k2 in counts:
			if k1==k2:
				continue
			p2=float(counts[k2])/total
			imp+=p1*p2
	return imp

def entropy(rows):
	from math import log
	log2=lambda x:log(x)/log(2)
	results=uniquecounts(rows)
	
	ent=0.0
	for r in results.keys():
		p=float(results[r])/len(rows)
		ent=ent-p*log2(p)
	return ent

def variance(rows):
	if len(rows) == 0: 
		return 0
	data = [float(row[len(row) - 1]) for row in rows]
	mean = sum(data) / len(data)

	variance = sum([(d-mean)**2 for d in data]) / len(data)
	return variance

def buildtree(rows, scorefun=entropy):
	if len(rows) == 0: 
		return decisionnode()
	current_score = scorefun(rows)

	best_gain = 0.0
	best_criteria = None
	best_sets = None

	column_count = len(rows[0]) - 1
	for col in range(0, column_count):
		column_values = set([row[col] for row in rows])
	
		for value in column_values:
			set1, set2 = divideset(rows, col, value)
			p = float(len(set1)) / len(rows)
			gain = current_score - p*scorefun(set1) - (1-p)*scorefun(set2)
			if gain > best_gain and len(set1) > 0 and len(set2) > 0:
	        		best_gain = gain
		        	best_criteria = (col, value)
	        		best_sets = (set1, set2)

	if best_gain > 0:
		trueBranch = buildtree(best_sets[0])
		falseBranch = buildtree(best_sets[1])
		return decisionnode(col=best_criteria[0], value=best_criteria[1],tb=trueBranch, fb=falseBranch)
	else:
		return decisionnode(results=uniquecounts(rows))


def printtree(tree, indent=''):
	if tree.results != None:  # leaf node
		print tree.results
	else:
		print '%s:%s?' % (tree.col, tree.value)
		print indent + 'T->',
		printtree(tree.tb, indent + '  ')
		print indent + 'F->',
		printtree(tree.fb, indent + '  ')


def classify(observation, tree):
	if tree.results != None:  # leaf
		return tree.results
	else:
		v = observation[tree.col]
		branch = None
	if isinstance(v, int) or isinstance(v, float):
		if v >= tree.value: branch = tree.tb
		else: branch = tree.fb
	else:
		if v == tree.value: branch = tree.tb
		else: branch = tree.fb
	return classify(observation, branch)


	
