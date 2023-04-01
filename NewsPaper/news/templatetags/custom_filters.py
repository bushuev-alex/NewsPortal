from django import template
import re
from .bad_words import bad_words
bad_words += [word.capitalize() for word in bad_words]

register = template.Library()


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
        replace_by = bad_word[0] + '*' * (len(bad_word) - 1)
        sentence = re.sub(bad_word, replace_by, sentence)
    return sentence


if __name__ == '__main__':
    import re
    sent = re.sub(f"my ({'|'.join(bad_words)})", "good_news", "This is bad_news.")
    print(sent)
