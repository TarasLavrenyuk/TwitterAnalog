import random
from datetime import date, datetime
import re
import uuid


def getLastName():
    names = []
    names.append('Henriques')
    names.append('Kurth')
    names.append('Glaspie')
    names.append('Kiker')
    names.append('Sandidge')
    names.append('Coto')
    names.append('Cost')
    names.append('Raven')
    names.append('Copeland')
    names.append('Mckinsey')
    names.append('Soller')
    names.append('Vasques')
    names.append('Ehlers')
    names.append('Cobbins')
    names.append('Lovingood')
    names.append('Mcneill')
    names.append('Hoy')
    names.append('Pintor')
    names.append('Dieterich')
    names.append('Bonacci')
    names.append('Lehmkuhl')
    names.append('Simons')
    names.append('Schaub')
    names.append('Marriott')
    names.append('Poynter')
    names.append('Mcnicholas')
    names.append('Fiscus')
    names.append('Lesane')
    return names[random.randint(0, len(names)-1)]

def getFirstName():
    names = []
    names.append('Edna')
    names.append('Deetta')
    names.append('Lauretta')
    names.append('Evangelina')
    names.append('Georgie')
    names.append('Ellyn')
    names.append('Nenita')
    names.append('Ellis')
    names.append('Hisako')
    names.append('Randy')
    names.append('Janell')
    names.append('Kit')
    names.append('Jesusita')
    names.append('Eleanore')
    names.append('Lorie')
    names.append('Kristen')
    names.append('Oliver')
    names.append('Tracey')
    names.append('Treena')
    names.append('Sharron')
    names.append('Melonie')
    names.append('Neil')
    names.append('Felicitas')
    names.append('Vernetta')
    names.append('Bertha')
    names.append('Jerrica')
    names.append('Bernie')
    names.append('Talia')
    names.append('Doria')
    names.append('Violet')
    names.append('Ceola')
    names.append('Eloisa')
    names.append('Lorrie')
    names.append('Chung')
    names.append('Evelin')
    names.append('Marjory')
    names.append('Alysha')
    names.append('Beatris')
    names.append('Ophelia')
    names.append('Tiffani')
    names.append('Monserrate')
    names.append('Stanley')
    names.append('Lekisha')
    names.append('Hosea')
    names.append('Chiquita')
    names.append('Karly')
    names.append('Jeanelle')
    names.append('Nena')
    names.append('Vonnie')
    return names[random.randint(0, len(names)-1)]

def getCompany():
    companies = ['Bing', 'Google', 'Yahoo', 'Microsoft', 'Apple', 'Yandex']
    return companies[random.randint(0, len(companies)-1)]

def getBirthDate():
    start_date = date.today().replace(day=1, month=1, year=1970).toordinal()
    end_date = date.today().replace(day=1, month=1, year=1990).toordinal()
    return date.fromordinal(random.randint(start_date, end_date))

def getTags(string):
    tags = []
    words = string.split()
    for word in words:
        if word[0] == '#':
            word = " ".join(re.findall("[_a-zA-Z0-9]+", word))
            tags.append(word)
    return tags

def get_word():
    words = ['time',
             'person',
             'year',
             'way',
             'day',
             'thing',
             'man',
             'world',
             'life',
             'hand',
             'part',
             'child',
             'eye',
             'woman',
             'place',
             'work',
             'week',
             'case',
             'point',
             'government',
             'company',
             'number',
             'group',
             'problem',
             'fact',
             'be',
             'have',
             'do',
             'say',
             'get',
             'make',
             'go',
             'know',
             'take',
             'see',
             'come',
             'think',
             'look',
             'want',
             'give',
             'use',
             'find',
             'tell',
             'ask',
             'work',
             'seem',
             'feel',
             'try',
             'leave',
             'call',
             'good',
             'new',
             'first',
             'last',
             'long',
             'great',
             'little',
             'own',
             'other',
             'old',
             'right',
             'big',
             'high',
             'different',
             'small',
             'large',
             'next',
             'early',
             'young',
             'important',
             'few',
             'public',
             'bad',
             'same',
             'able'
             'the',
             'and',
             'a',
             'that',
             'I',
             'it',
             'not',
             'he',
             'as',
             'you',
             'this',
             'but',
             'his',
             'they',
             'her',
             'she',
             'or',
             'an',
             'will',
             'my',
             'one',
             'all',
             'would',
             'there',
             'their',
             'to',
             'of',
             'in',
             'for',
             'on',
             'with',
             'at',
             'by',
             'from',
             'up',
             'about',
             'into',
             'over',
             'after',
             'beneath',
             'under',
             'above']
    return words[random.randint(0, len(words)-1)]

def get_tag():
    tags = ['#love',  '#TagsForLikes', '#TagsForLikesApp',  '#TFLers', '#tweegram', '#photooftheday', '#20likes',
            '#amazing', '#smile', '#follow4follow', '#like4like', '#look', '#instalike', '#igers', '#picoftheday',
            '#food', '#instadaily', '#instafollow', '#followme', '#girl', '#iphoneonly', '#instagood', '#bestoftheday',
            '#instacool', '#instago', '#all_shots', '#follow', '#webstagram', '#colorful', '#style', '#swag']
    return tags[random.randint(0, len(tags)-1)]

def get_content():
    content = ' '
    i = 1
    while i <= 10:
        content = content + get_word() + ' '
        i += 1
    i = 1
    while i <= 3:
        content = content + get_tag() + ' '
        i += 1
    return content

def get_twit():
    content = get_content()
    posted_date = datetime.strptime(str(datetime.now().strftime("%Y-%m-%d %H:%M")), '%Y-%m-%d %H:%M')
    tags = getTags(content)
    id = uuid.uuid1()
    twit = {'id': id,
                'header': 'header',
                'content': content,
                'posted_date': posted_date,
                'liked': [],
                'tags': tags,
                'hide': 0
                }
    return twit