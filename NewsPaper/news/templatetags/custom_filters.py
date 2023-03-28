from django import template
import re
from .bad_words import bad_words
bad_words += [word.capitalize() for word in bad_words]

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
    """
    value: значение, к которому нужно применить фильтр
    """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} Р'


@register.filter()
def censor(sentence: str):
    sentence_ = re.sub("[\"\',.!:;]", '', sentence)
    words = sentence_.split(' ')
    bad_exist = set(words).intersection(bad_words)
    for bad_word in bad_exist:
        replace = bad_word[0] + '*' * (len(bad_word) - 1)
        sentence = re.sub(bad_word, replace, sentence)
    return sentence


# if __name__ == '__main__':
#     import re
#
#     bad_words = ['chlen', 'huy', 'blyad', 'pizda']
#     sent = 'my huy is big and her pizda is wet'
#     words = ['my', 'huy', 'is', 'big', 'and', 'her', 'pizda', 'is', 'wet']
#
#     print(set(words).intersection(bad_words))
#     bad_exist = set(words).intersection(bad_words)
#     for word in bad_exist:
#         print(sent)
#         sent = re.sub(word, word[0] + '*', sent)
#         print(sent)
#
#     # print(re.sub('huy', 'h*', sent))
