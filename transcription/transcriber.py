import re

# словарь с исключениями, которые не подчиняются общим правилам транскрипции
EXCEPTIONS = {
    # конечные согласные читаются
    'sud': 'syd',
    'ouest': 'wɛst',
    'fils': 'fis',   
    'bonus': 'bonys',
    'bac': 'bak',
    'sept': 'sɛt',  
    
    # исключения с окончанием -er
    'hiver': 'ivɛʀ',
    'mer': 'mɛʀ',
    'cher': 'ʃɛʀ',
    'hier': 'jɛʀ',
    'ver': 'vɛʀ',
    'fer': 'fɛʀ',
    'cœur': 'kœʀ',
    'sœur': 'sœʀ',
    
    # числительные с -x
    'six': 'sis',
    'dix': 'dis',
    
    # другие частые исключения
    'monsieur': 'məsjø',
    'madame': 'madam',
    'mademoiselle': 'madmwazɛl'
}

def get_exception(word: str) -> str | None:
    word_lower = word.lower()
    return EXCEPTIONS.get(word_lower)

# функция проверки, является ли текст французским
def is_french_text(text: str) -> bool:
    french_pattern = r'^[a-zA-Zàâäéèêëïîôöùûüÿçæœ\'\- ]+$'
    
    if not re.match(french_pattern, text):
        return False
    
    french_letters = r'[a-zA-Zàâäéèêëïîôöùûüÿçæœ]'
    if not re.search(french_letters, text):
        return False
    
    consonant_cluster = r'[bcdfghjklmnpqrstvwxz]{5,}'
    if re.search(consonant_cluster, text.lower()):
        return False
    
    vowels = r'[aeiouyàâèéêëïîôùû]'
    if not re.search(vowels, text.lower()):
        return False
    
    return True
    
def transcribe(word: str) -> str:
    if not is_french_text(word):
        return "Извините, кажется, вы не прислали мне французских слов."
    
    exception_transcription = get_exception(word)
    if exception_transcription:
        return f"Транскрипция: {exception_transcription}"

    word2tr = word.lower().split() # текст переводится в нижний регистр и делится на слова
    consonants = 'bcdfghjklmnpqrstvwxz'
    
    result = 'Транскрипция: '

    for j in range(len(word2tr)):

        i = 0
        was_cut = False

        if word2tr[j][-1] in 'xdpts':
            # удаляются непроизносимые согласные на конце
            word2tr[j] = word2tr[j][:len(word2tr[j])-1]
            was_cut = True

        while i < len(word2tr[j]):

            if i < len(word2tr[j]) - 1 and word2tr[j][i] == word2tr[j][i+1] and word2tr[j][i] in consonants:
                # проверка, есть ли двойные согласные, они читаются как простые
                current_letter = word2tr[j][i]
                if current_letter in gr2ph:
                    rule = codes[gr2ph[current_letter]['nicht']]
                    if i == 0 and j != 0:
                        result += ' '
                    result += rule[0]
                    i += 2
                    continue
            
            current_letter = word2tr[j][i]

            if current_letter in gr2ph:
                # проверка на комбинацию букв
                combinations = sorted(gr2ph[current_letter].keys(), key=len, reverse=True)
                rule = None
                
                for k in combinations:
                    
                    if k == 'nicht':
                        # если комбинации нет, проверка на специальные правила
                        rule = special_rules(word2tr[j], i, was_cut)
                        continue
                    
                    if k == word2tr[j][i+1:i+1+len(k)]:
                        # проверка на специальные правила для комбинаций
                        rule = combination_rules(current_letter, k, word2tr[j], i)
                        if rule is None:
                            rule = codes[ gr2ph[current_letter][k] ]
                            break
                
                if rule is not None:
                    # если на предыдущих шагах было обнаружено подходящее правило, записываем в результат
                    if i == 0 and j != 0:
                        result += ' '
                    result += rule[0]
                    i += rule[1]
                
                else:
                    # если специальное правило или комбинация не были найдены, то транскрибируем как одна буква -- один звук
                    h = codes[gr2ph[current_letter]['nicht']]
                    if i == 0 and j != 0:
                        result += ' '
                    result += h[0]
                    i += 1

            else:
                # если ничего не подошло, оставляем символ таким, какой есть
                if i == 0 and j != 0:
                        result += ' '
                result += word2tr[j][i]
                i += 1
 
            

    print('Transcription:', result)
    return result

def special_rules(word: str, pos: int, was_cut: bool) -> list[str, int] | None:
    # функция, проверяющая специальные правила для одной буквы
    current_pos = word[pos]
    vowels = 'aeiouyàâèéêëïîôùû'
    pronounced_consonants = 'bcdfghjklmnpqrstvwx'  # кроме z
    all_consonants = 'bcdfghjklmnpqrstvwxz'

    if current_pos == 'o':
        if (pos + 1 < len(word) and word[pos + 1] in pronounced_consonants):
            return ['ɔ', 1]
        else:
            return ['o', 1]

    elif current_pos  == 'i' and pos + 1 < len(word) and word[pos + 1] in vowels:
        return ['j', 1]

    elif current_pos == 's':
        prev_is_vowel = pos > 0 and word[pos - 1] in vowels
        next_is_vowel = pos + 1 < len(word) and word[pos + 1] in vowels
        if prev_is_vowel and next_is_vowel:
            return ['z', 1]

    elif current_pos == 'u' and pos + 1 < len(word) and word[pos + 1] in vowels:
        return ['ɥ', 1]
    
    elif current_pos == 'e':
        if pos == len(word) - 1 and was_cut == False:
            return ['', 1]
        elif (pos + 2 <= len(word) - 1 and word[pos + 1] in all_consonants and word[pos + 2] in all_consonants) or (pos + 1 == len(word) - 1 and word[pos + 1] in all_consonants) or (pos == len(word) - 1 and was_cut == True):
            return ['ɛ', 1]
        else:
            return ['ə', 1]
    
    

    return None

def combination_rules(current_letter: str, combination: str, word: str, current_pos: int) -> list[str, int] | None:
    # функция, проверяющая нестандартные правила комбинаций
    next_pos = current_pos + len(combination) + 1
    vowels = 'aeiouyàâèéêëïîôùû'
    pronounced_consonants = 'bcdfghjklmnpqrstvwx'

    if (current_letter == 'a' and combination in ['n', 'm', 'in', 'im'] or
        current_letter == 'e' and combination in ['n', 'm', 'in'] or
        current_letter == 'i' and combination in ['n', 'm'] or
        current_letter == 'o' and combination in ['n', 'm', 'u'] or
        current_letter == 'u' and combination in ['n', 'm'] or
        current_letter == 'y' and combination in ['n', 'm']):
        if next_pos < len(word) and word[next_pos] in vowels:
            if current_letter == 'a':
                if combination == 'in':
                    return ['ɛn', 3]
                elif combination == 'im':
                    return ['ɛm', 3]
                elif combination == 'n':
                    return ['an', 2]
                elif combination == 'm':
                    return ['am', 2]
            elif current_letter == 'e':
                if combination == 'n':
                    return ['ɛn', 2]
                elif combination == 'm':
                    return ['ɛm', 2]
                elif combination == 'in':
                    return ['ɛn', 3]
            elif current_letter == 'i':
                if combination == 'n':
                    return ['in', 2]
                elif combination == 'm':
                    return ['im', 2]
            elif current_letter == 'o':
                if combination == 'n':
                    return ['on', 2]
                elif combination == 'm':
                    return ['om', 2]
            elif current_letter == 'o':
                if combination == 'u':
                    return ['w', 2]
                elif combination == 'n':
                    return ['yn', 2]
                elif combination == 'm':
                    return ['ym', 2]
            elif current_letter == 'y':
                if combination == 'n':
                    return ['in', 2]
                elif combination == 'm':
                    return ['im', 2]
                
    elif current_letter == 't' and combination == 'i':
        if current_pos + 2 < len(word) and word[current_pos + 2] in vowels:
         return ['s', 1]
        else:
            return ['t', 1]
                
    elif current_letter == 'i':
        if combination == 'll' and current_pos > 0 and word[current_pos - 1] in vowels:
            return ['j', 3]
        elif combination == 'll':
            return ['ij', 3]
        
    elif current_letter == 'e' and combination == 'u':
        if current_pos + 2 < len(word) and word[current_pos + 1] in pronounced_consonants:
            return ['œ', 2]
        else:
            return ['ø', 2]


    return None

gr2ph = {
    # словарь с звуками и комбинациями, ссылается на словарь со списками, в котором содержится транскрипция и число, на которое необходимо сдвинуть счетчик
    'a': {
         "nicht": 1,
         'n': 2,
         'nn': 3,
         "mm": 4,
         "m": 2,
         'i': 5,
         "in": 6,
         "im": 6,
         'ill': 7,
         'y': 8,
         'u': 9,
         "ur": 10
    },
    
    'b': {
         'nicht': 11
    },
    
    'c' : {
        'nicht': 15,
        'e': 12,
        'i': 12,
        'y': 12,
        'h': 13
    },

    'd': {
        'nicht': 14
    },

    'e': {
        'nicht': 16,
        'i': 5,
        'il': 17,
        'in': 6,
        'z': 18,
        'uz': 19,
        'u': 20,
        'n': 2,
        'nn': 21,
        'm': 2,
        'mm': 59,
        'au': 22
    },

    'f': {
        'nicht': 23
    },

    'g': {
        'nicht': 24,
        'e': 25,
        'i': 25,
        'y': 25,
        'n': 26,
        'u': 27
    },

    'h': {
        'nicht': 28
    },

    'i': {
        'nicht': 29,
        'n': 30,
        'nn': 31,
        'm': 30,
        'mm': 32,
        'en': 33,
        'll': 61
    },

    'j': {
        'nicht': 34
    },

    'k': {
        'nicht': 15
    },

    'l': {
        'nicht': 35
    },

    'm': {
        'nicht': 36
    },

    'n': {
        'nicht': 37
    },

    'o': {
        'nicht': 38,
        'z': 39,
        'u': 40,
        'n': 41,
        'nn': 42,
        'm': 41,
        'mm': 43,
        'i': 44,
        'in': 45
    },

    'p': {
        'nicht': 46,
        't': 28,
        'h': 47
    },

    'q': {
        'nicht': 15,
        'u': 48
    },

    's': {
        'nicht': 12
    },

    'r': {
        'nicht': 49
    },

    't': {
        'nicht': 50,
        'i': 12,
        'h': 51
    },

    'u': {
        'nicht': 52,
        'n': 53,
        'nn': 54,
        'm': 53,
        'mm': 55
    },

    'v': {
        'nicht': 56
    },

    'w': {
        'nicht': 57
    },

    'y': {
        'nicht': 29,
        'n': 30,
        'nn': 31,
        'm': 30,
        'mm': 32
    },

    'x':
        {
        'nicht': 60
        },

    'z': {
        'nicht': 58
    },

    'ç': {
        'nicht': 12
    },

    'à': {
        'nicht': 1
    },

    'â': {
        'nicht': 1
    },

    'è': {
        'nicht': 16
    },

    'ê': {
        'nicht': 16
    },

    'é': {
        'nicht': 18
    },

    'ï': {
        'nicht': 29
    },

    'î': {
        'nicht': 29
    },

    'û': {
        'nicht': 52
    },

    'ô': {
        'nicht': 39
    }
}

codes = [
    ['!!ERROR!!', 1],
    ['a', 1],
    ['ɑ̃', 2],
    ['an', 3],
    ['am', 3],
    ['ɛ', 2],
    ['ɛ̃', 3],
    ['aj', 4],
    ['ɛj', 2],
    ['ɔ', 2],
    ['o', 2],
    ['b', 1],
    ['s', 1],
    ['ʃ', 2],
    ['d', 1],
    ['k', 1],
    ['ɛ', 1],
    ['ɛj', 3],
    ['e', 2],
    ['ø', 2],
    ['œ', 2],
    ['ɛn', 3],
    ['o', 3],
    ['f', 1],
    ['g', 1],
    ['ʒ', 1],
    ['ɲ', 2],
    ['g', 2],
    ['', 1],
    ['i', 1],
    ['ɛ̃', 2],
    ['in', 3],
    ['im', 3],
    ['jɛ̃', 3],
    ['ʒ', 1],
    ['l', 1],
    ['m', 1],
    ['n', 1],
    ['ɔ', 1],
    ['o', 1],
    ['u', 2],
    ['ɔ̃', 2],
    ['ɔn', 3],
    ['ɔm', 3],
    ['wa', 2],
    ['wɛ̃', 3],
    ['p', 1],
    ['f', 2],
    ['k', 2],
    ['ʁ', 1],
    ['t', 1],
    ['t', 2],
    ['y', 1],
    ['œ̃', 2],
    ['yn', 3],
    ['ym', 3],
    ['v', 1],
    ['w', 1],
    ['z', 1],
    ['ɛm', 3],
    ['ks', 1],
    ['ij', 3]
]
