import pdb
critics = {
	'Lisa Rose': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'Superman Returns': 3.5,
		'You, Me and Dupree': 2.5,
		'The Night Listener': 3.0
	},
	'Gene Seymour': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 1.5,
		'Superman Returns': 5.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 3.5
	},
	'Michael Philips': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.0,
		'Superman Returns': 3.5,
		'The Night Listener': 4.0
	},
	'Claudia Puig': {
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'The Night Listener': 4.5,
		'Superman Returns': 4.0,
		'You, Me and Dupree': 2.0
	},
	'Mick LaSalle': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'Just My Luck': 2.0,
		'Superman Returns': 3.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 2.0
	},
	'Jack Matthews': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'The Night Listener': 3.0,
		'Superman Returns': 5.0,
		'You, Me and Dupree': 3.5
	},
	'Toby': {
		'Snakes on a Plane': 4.5,
		'You, Me and Dupree': 1.0,
		'Superman Returns': 4.0
	}
}

from math import sqrt

# Returns a distance-based (Euclidean distance) similarity score for person1 and person2
# Note that this similarity score does not account for consistent grande inflation
# If one person tends to give higher grades than the other, even though both people
# might have similar tastes, their distance will be higher. Still, depending on the
# application, this might be what is expected
def sim_distance(prefs,person1,person2):
	# Get the list of shared_items
	si = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1

	# if they have no ratins in common, return 0
	if len(si)==0: return 0

	# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])

	return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs,p1,p2):
	# Get the list of mutually rated shared_items
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item]=1

	# Find the number of elements
	n=len(si)

	# if they have no ratings in common, return 0
	if n==0: return 0

	# Add up all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	# Sum up the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

	# Sum up the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0

	r=num/den

	return r

def sim_tanimoto(prefs,p1,p2):
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item]=1
	n=len(si)
	if n==0: return 0

	dotProduct=sum([prefs[p1][item]*prefs[p2][item] for item in si])
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

	t=dotProduct/(sum1Sq+sum2Sq-dotProduct)
        return t
# For more similarity metrics, http://en.wikipedia.org/wiki/Metric_%28mathematics%29#Examples

def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

	scores.sort()
	scores.reverse()
	return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		# don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)

		# ignore scores of 0 or lower
		if sim<=0: continue
		for item in prefs[other]:

			# only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				# Similarity * Score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				# Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim

			# Create the normalized list
			rankings=[(total/simSums[item],item) for item,total in totals.items()]

			# Return the sorted list
			rankings.sort()
			rankings.reverse()
	return rankings

def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]
	return result

def calculateSimilarItems(prefs,n=10):
	result={}

	itemPrefs=transformPrefs(prefs)
	c=0

	for item in itemPrefs:
		c+=1
		if c%100==0:
			print "%d / %d" %(c,len(itemPrefs))

		scores=topMatches(itemPrefs,item,n=10,similarity=sim_distance)
		result[item]=scores
	return result

def getRecommendedItems(prefs,itemMatch,user):
	userRatings=prefs[user]
	scores={}
	totalSim={}

	for(item,rating) in userRatings.items():
		for(similarity,item2) in itemMatch[item]:
			if item2 in userRatings:continue

			scores.setdefault(item2,0)
			scores[item2]+=similarity*rating

			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity

	rankings=[(score/totalSim[item],item) for item,score in scores.items()]

	rankings.sort()
	rankings.reverse()
	return rankings

def loadMovieLens(path="./movielens"):
	movies={}
	for line in open(path+"/u.item"):
		(id,title)=line.split("|")[0:2]
		movies[id]=title

	prefs={}
	for line in open(path+"/u.data"):
		(user,movieid,rating,ts)=line.split("\t")
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)
	return prefs



