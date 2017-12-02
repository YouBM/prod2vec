import json
import requests
from pprint import pprint
import nltk
from collections import Counter

def prepareData():
    data = json.load(open('products-sample.json'))
    output = []
    global_parameters = {}
    global_categs = []
    global_brands = []
    for item in data[0:2]:
        for var in item['variant_data']:
            params = var['params']
            for param in params:
                id = param['id']
                global_parameters[id] = []
    for item in data[0:2]:
        date = item['date']
        user = item['user_id']
        variant_id = item['variant_id']
        title = item['title_full']['C']
        category = item['product_type']['title']['C']
        product_id = item['product_id']
        description = item['brief_plain']['C'].replace('\n','')
        brand = item['brand']['title']['C']
        brand_id = item['brand']['brand_id']
        priceSum = 0
        varCount = 0
        parameters = {}
        for var in item['variant_data']:
            params = var['params']
            for param in params:
                id = param['id']
                parameters[id] = []
                value = [value for key, value in param['values'].items()][0] if isinstance([value for key, value in param['values'].items()][0], str) else [value for key, value in param['values'].items()][0][0]
                # parameter = id + ' ' + str(value)
                if id == 'SIZE_EUR':
                    print(date,user,id,value)
                if value not in parameters[id]:
                    parameters[id].append(value)
                if value not in global_parameters[id]:
                    global_parameters[id].append(value)


            priceSum += int(var['price']['CZ1000']['price'])
            varCount += 1
        price = priceSum / varCount
        global_brands.append(brand_id)
        global_categs.append(category)
        # for key, value in parameters.items():
        #     value = list(set(value))
        #     parameters[key] = value
        product = {
            "date": date,
            "user_id": user,
            "price": price,
            "category": category,
            "brand": brand_id,
            "params": parameters
        }
        output.append(product)
    # for key, value in global_parameters.items():
    #     value = list(set(value))
    #     global_parameters[key] = value
    global_brands = list(set(global_brands))
    global_categs = list(set(global_categs))
    final = []
    for prod in output:
        all = []
        categories = []
        brands = []
        params = []
        for cat in global_categs:
            categories.append({cat: 1 if cat == prod['category'] else 0})
        for bra in global_brands:
            brands.append({bra: 1 if bra == prod['brand'] else 0})
        for key, values in global_parameters.items():
            if key in prod['params'].keys():
                for value in values:
                    if value in prod['params'][key]:
                        right = [0] * (len(values) + 1)
                        index = values.index(value)
                        right[index] = 1
                        param = {key: right}
                        params.append(param)
            else:
                right = [0] * len(values)
                right.append(1)
                param = {key: right}
                params.append(param)
        all.append(prod['user_id'])
        all.append(prod['date'])
        all.append(prod['price'])
        all.extend(categories)
        all.extend(brands)
        all.extend(params)
        final.append(all)
        # print(len(all))
    pprint(final)
    # with open('data.txt', 'w') as outfile:
    #     json.dump(output, outfile)

def generate():
    print([0] * 8)

def translateSentence(sent):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'target':'de','key':'AIzaSyA_PsFfdEG7CHuxMz_NFwr4cCojdkm5E9Q','q':sent}
    url = 'https://translation.googleapis.com/language/translate/v2'
    r = requests.post(url,headers=headers,data=payload)
    jsonR = json.loads(r.text)
    return jsonR['data']['translations'][0]['translatedText']


def createTokens():
    tokens = []
    for desc in descs:
        words = nltk.word_tokenize(desc)
        words = [w.lower() for w in words]
        for index, word in enumerate(words):
            if word == '.' or word == ',':
                continue
            token = next((x for x in tokens if x['text'] == word), None)
            if token == None:
                token = {
                    "text": word,
                    "count": 1
                }
                tokens.append(token)
            else:
                token['count'] += 1
                tokens = [c for c in tokens if c['text'] != word]
                tokens.append(token)

    tokens = [c for c in tokens if c['count'] >= 5]
    tokens = sorted(tokens, key=lambda k: k['count'])
    pprint(tokens)


def createCombinations():
    combinations = []
    for desc in descs:
        words = nltk.word_tokenize(desc)
        for index, word in enumerate(words):
            if word == '.' or word == ',' or index == 0:
                continue
            if words[index-1] == '.' or words[index-1] == ',':
                continue
            text = words[index-1] + ' ' + words[index]
            comb = next((x for x in combinations if x['text'] == text), None)
            if comb == None:
                comb = {
                    "text": text,
                    "count": 1
                }
                combinations.append(comb)
            else:
                comb['count'] += 1
                combinations = [c for c in combinations if c['text'] != text]
                combinations.append(comb)

    combinations = [c for c in combinations if c['count'] >= 3]

    for index, com in enumerate(combinations):
        if index == 0:
            continue
        wordsPrev = nltk.word_tokenize(combinations[index-1]['text'])
        wordsPost = nltk.word_tokenize(com['text'])
        if wordsPrev[-1] == wordsPost[0]:
            com["text"] = combinations[index-1]['text'] + ' ' + wordsPost[-1]

    combinations = sorted(combinations, key=lambda k: k['count'])
    combinations = [c for index, c in enumerate(combinations) if index < len(combinations) - 1 and c['text'] not in combinations[index+1]['text']]
    pprint(combinations)



# def testData():
#     data = json.load(open('products-sample.json'))
#     item = data[4]
#     parameters = []
#     pprint(item.items())
#     for var in item['variant_data'][0:2]:
#         pprint(var)
#         # params = var['params']
#         # for param in params:
#         #     id = param['id']
#         #     value = [value for key, value in param['values'].items()][0] if isinstance([value for key, value in param['values'].items()][0], str) else [value for key, value in param['values'].items()][0][0]
#         #     parameter = id + ' ' + str(value)
#         #     parameters.append(parameter)
#     # pprint(Counter(parameters))




if __name__ == '__main__':
    # generate()
    # testData()
    prepareData()
    # print(com['text'])














