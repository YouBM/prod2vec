import json
import nltk
import requests
from pprint import pprint
import operator

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
                if id not in ['SIZE_EUR', 'COLOR']:
                    if value not in parameters[id]:
                        parameters[id].append(value)
                    if value not in global_parameters[id]:
                        global_parameters[id].append(value)
            priceSum += int(var['price']['CZ1000']['price'])
            varCount += 1
        price = priceSum / varCount
        global_brands.append(brand_id)
        global_categs.append(category)
        product = {
            "date": date,
            "user_id": user,
            "price": price,
            "category": category,
            "brand": brand_id,
            "params": parameters
        }
        output.append(product)
    global_brands = list(set(global_brands))
    global_categs = list(set(global_categs))
    final = []
    for prod in output:
        all = []
        params = []
        for cat in global_categs:
            if cat == prod['category']:
                right = [0] * (len(global_categs) + 1)
                index = global_categs.index(cat)
                right[index] = 1
                category = {"CATEGORY": right}
                all.append(category)
        for bra in global_brands:
            if bra == prod['brand']:
                right = [0] * (len(global_brands) + 1)
                index = global_brands.index(bra)
                right[index] = 1
                brand = {"BRAND": right}
                all.append(brand)
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
        all.append({"USER": prod['user_id']})
        all.append({"DATE": prod['date']})
        all.append({"PRICE": prod['price']})
        all.extend(params)
        final.append(all)
    pprint(final)


def mostFoundProducts():
    data = json.load(open('products-sample.json'))
    views = []
    for item in data[0:900]:
        user = item['user_id']
        date = item['date']
        product_id = item['product_id']
        view = {
            "user": user,
            "date": date,
            "product": product_id
        }
        views.append(view)
    views.sort(key=lambda x: (x["user"], x["date"]), reverse=True)
    pprint(views)



def translate_sentence(sent):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'target':'de','key':'AIzaSyA_PsFfdEG7CHuxMz_NFwr4cCojdkm5E9Q','q':sent}
    url = 'https://translation.googleapis.com/language/translate/v2'
    r = requests.post(url,headers=headers,data=payload)
    json_r = json.loads(r.text)
    return json_r['data']['translations'][0]['translatedText']


def create_tokens():
    tokens = []
    descs  = []
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


def create_combinations():
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


if __name__ == '__main__':
    # generate()
    # testData()
    # prepareData()
    mostFoundProducts()
    # print(com['text'])
