from django import template


register = template.Library()

@register.filter()
def censor(value:str):
   swear_words = ('банан', 'морков', 'карто', 'броккол', 'ананас',
                  'Банан', 'Морков', 'Карто', 'Броккол', 'Ананас',)
   for word in swear_words:
      if word in value:
          value = value.replace(word, '****')

   return value