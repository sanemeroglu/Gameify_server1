
import math



#function calculates distance start
def euclidean_distnce(game_data, person1, person2):
    common_item = {}
    #common buy in person1 and person2
    for item in game_data[person1]:
        if item in game_data[person2]:
            common_item[item] = True

    #if no item is common
    if len(common_item) == 0: return 0

    #calculate distance
    #√((x1-x2)^2 + (y1-y2)^2)
    distance = sum([math.pow(game_data[person1][itm] - game_data[person2][itm], 2) for itm in common_item.keys()])
    distance = math.sqrt(distance)
    #return result
    return 1/(distance + 1)

def transform_dataset(data):
    result = {}
    for item in data.keys():  # item is a person like 'Donald'
        for subitem in data[item].keys():  # subitem is actually an item like 'Tylor Swift'
            result.setdefault(subitem, {})
            result[subitem][item] = data[item][subitem]  # swap between person and item

        return result

def calculateSimilarItems(game_data, n=5):   #n is how many top similar items to store
    result = {}
    game_data_reverse = transform_dataset(game_data)   #transforms dataset to item centric
    for item in game_data_reverse.keys():
        #finding distance score of all other items with respect to current item
        similarities = [(euclidean_distnce(game_data_reverse, item, other), other) for other in game_data_reverse.keys() if item != other]
        similarities.sort()
        similarities.reverse()   #top scores first
        result[item] = similarities[0:n]   #taking only top 2 items and storing in result
    return result

def pearson_correlation(game_data, person1, person2):
    si = {}
    for item in game_data[person1]:
        if item in game_data[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    #calculating sum
    sum1 = sum([game_data[person1][it] for it in si])
    sum2 = sum([game_data[person2][it] for it in si])

    #calculating sum of squares
    sumSq1 = sum([pow(game_data[person1][it], 2) for it in si])
    sumSq2 = sum([pow(game_data[person2][it], 2) for it in si])

    #calculate sum of products
    sumPr = sum([game_data[person1][it] * game_data[person2][it] for it in si])

    #calculate person score
    num = sumPr - (sum1*sum2/n)
    den = math.sqrt((sumSq1-pow(sum1, 2)/n)*(sumSq2 - pow(sum2, 2)/n))
    if(den == 0):
        return 0
    r = num/den
    return r

def topMatches(game_data, person, n, similirity=pearson_correlation):
    scores = [(similirity(game_data, person, other), other) for other in game_data.keys() if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]
