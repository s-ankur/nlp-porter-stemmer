#!/usr/bin/env python3
__author__ = "Ankur Sonawane (16085073)"
"""
1. Read the Porter Stemmer paper:
https://tartarus.org/martin/PorterStemmer/def.txt
and then implement the algorithm as given in the paper (not the revised and improved versions which came
r). Preferably implement it in Python. This is to be done for English.
late


This is a complete functional rewrite of the object oriented code specified at
https://tartarus.org/martin/PorterStemmer/python.txt
All of the functions in the module are tested automatically by using doctests embedded within the docstrings
"""
import re


def degree(word):
    """
    m() measures the number of consonant sequences between k0 and j.
    if c is a consonant sequence and v a vowel sequence, and <..>
    indicates arbitrary presence,

       <c><v>       gives 0
       <c>vc<v>     gives 1
       <c>vcvc<v>   gives 2
       <c>vcvcvc<v> gives 3
       ....

    >>> str(all(degree(word)==0 for word in ('tr',  'ee',  'tree',  'Y',  'by')))
    'True'

    >>> str(all(degree(word)==1 for word in ('trouble',  'oats',  'trees',  'ivy')))
    'True'

    >>> str(all(degree(word)==2 for word in ('troubles',  'private',  'oaten',  'orrery')))
    'True'
    """
    n = 0
    word = re.sub("^[^aeiouy]*", "", word)
    word = re.sub("[aeiouy]*$", "", word)
    while word:
        word = re.sub("^[aeiouy]*", "", word)
        bef = word
        word = re.sub("^[^aeiouy]*", "", word)
        if word != bef:
            n += 1
    return n


def vowelinstem(word):
    """vowelinstem() is TRUE <=> k0,...j contains a vowel

    >>> vowelinstem('man')
    True

    >>> vowelinstem('sk')
    False
    
    """
    return re.search("[aeiouy]", word) is not None


def doublec(word):
    """doublec(j) is TRUE <=> j,(j-1) contain a double consonant.

    >>> doublec('hitt')
    True

    >>> doublec('hit')
    False
    
    """
    if len(word) == 1:
        return False
    if word[-1] != word[-2]:
        return False
    return re.search("[aeiouy]", word[:-2]) is not None


def cvc(word):
    """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
    and also if the second c is not w,x or y. this is used when trying to
    restore an e at the end of a short  e.g.

       cav(e), lov(e), hop(e), crim(e), but
       snow, box, tray.

    >>> cvc('cat')
    True

    >>> cvc('to')
    False

    >>> cvc('ask')
    False
    
    """
    if len(word) != 3: return False
    if word[0] in 'aeiouy': return False
    if word[1] not in 'aeiouy': return False
    if word[2] in 'aeiouywx': return False
    return True


def consonant_y(word):
    """
    Converts the consonatal y to Y. Consonantal y is the y that is not after a consonant

    >>> consonant_y("may")
    'maY'

    >>> consonant_y("yam")
    'Yam'
    
    """
    ans = ""
    for i, j in enumerate(word):
        if j == 'y' and word[i - 1:i] in "aeiou":
            ans += "Y"
        else:
            ans += j
    return ans


def step1ab(word):
    """step1ab() gets rid of plurals and -ed or -ing. e.g.
        >>> step1ab("caresses")
        'caress'
        >>> step1ab("ponies")
        'poni'
        >>> step1ab("ties")
        'ti'
        >>> step1ab("caress")
        'caress'
        >>> step1ab("cats")
        'cat'
        
        >>> step1ab("feed")
        'feed'
        >>> step1ab("agreed")
        'agree'
        >>> step1ab("disabled")
        'disable'

        >>> step1ab("matting")
        'mat'
        >>> step1ab("mating")
        'mate'
        >>> step1ab("meeting")
        'meet'
        >>> step1ab("milling")
        'mill'
        >>> step1ab("messing")
        'mess'
        """
    if word[-1] == 's':
        if word.endswith("sses"):
            word = word[:-2]
        elif word.endswith("ies"):
            word = word[:-2]
        elif not word.endswith("ss"):
            word = word[:-1]
    if word.endswith("eed") and degree(word[:-3]) > 0:
        word = word[:-1]
    elif (word.endswith("ed") or word.endswith("ing")) and vowelinstem(word.rstrip('ed').rstrip('ing')):
        word = word.rstrip("ing").rstrip("ed")
        if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
            word = word + 'e'
        elif doublec(word) and word[-1] not in ('l', 's', 'z'):
            word = word[:-1]
        elif degree(word) == 1 and cvc(word):
            word = word[:-1] + 'e'
    return word


def step1c(word):
    """step1c() turns terminal y to i when there is another vowel in the stem.
    >>> step1c("happy")
    'happi'

    >>> step1c("sky")
    'sky'

    """
    if word.endswith("y") and vowelinstem(word[:-1]):
        word = word[:-1] + 'i'
    return word


def step2(word):
    """step2() maps double suffices to single ones.
    so -ization ( = -ize plus -ation) maps to -ize etc. note that the
    string before the suffix must give m() > 0.

    >>> step2("relational")
    'relate'
    >>> step2("conditional")
    'condition'
    >>> step2("rational")
    'rational'
    >>> step2("valenci")
    'valence'
    >>> step2("hesitanci")
    'hesitance'
    >>> step2("digitizer")
    'digitize'
    >>> step2("conformabli")
    'conformable'
    >>> step2("radicalli")
    'radical'
    >>> step2("differentli")
    'different'
    >>> step2("vileli")
    'vile'


    """
    if word[-2] == 'a':
        if word.endswith("ational") and degree(word[:-7]):
            word = word[:-5] + 'e'
        elif word.endswith("tional") and degree(word[:-6]):
            word = word[:-2]
    elif word[-2] == 'c':
        if word.endswith("enci") and degree(word[:-4]):
            word = word[:-1] + 'e'
        if word.endswith("anci") and degree(word[:-4]):
            word = word[:-1] + 'e'
    elif word[-2] == 'e':
        if word.endswith("izer") and degree(word[:-4]):
            word = word[:-1]
    elif word[-2] == 'l':

        if word.endswith("abli") and degree(word[:-4]):
            word = word[:-1] + 'e'
        elif word.endswith("alli") and degree(word[:-4]):
            word = word[:-2]
        elif word.endswith("entli") and degree(word[:-5]):
            word = word[:-2]
        elif word.endswith("eli") and degree(word[:-3]):
            word = word[:-2]
        elif word.endswith("ousli") and degree(word[:-5]):
            word = word[:-2]
    elif word[-2] == 'o':
        if word.endswith("ization") and degree(word[:-7]):
            word = word[:-5] + 'e'
        elif word.endswith("ation") and degree(word[:-5]):
            word = word[:-3] + 'e'
        elif word.endswith("ator") and degree(word[:-4]):
            word = word[:-2] + 'e'
    elif word[-2] == 's':
        if word.endswith("alism") and degree(word[:-5]):
            word = word[:-2]
        elif (word.endswith("iveness") and degree(word[:-7])) or (word.endswith("fulness") and degree(word[:-7])) or (
                word.endswith("ousness") and degree(word[:-7])):
            word = word[:-4]
    elif word[-2] == 't':
        if word.endswith("aliti") and degree(word.rstrip('ousli')):
            word = word[:-3]
        elif (word.endswith("iviti") and degree(word.rstrip('iviti'))) or (
                word.endswith("biliti") and degree(word.rstrip('biliti'))):
            word = word[:-3] + 'e'
    return word


def step3(word):
    """step3() dels with -ic-, -full, -ness etc. similar strategy to step2.

        >>> step3('triplicate')
        'triplic'
        >>> step3('formative')
        'form'
        >>> step3('formalize')
        'formal'
        >>> step3('electriciti')
        'electric'
        >>> step3('electrical')
        'electric'
        >>> step3('hopeful')
        'hope'
        >>> step3('goodness')
        'good'
    """
    if word[-1] == 'e':
        if word.endswith("icate") and degree(word[:-5]):
            word = word[:-3]
        elif word.endswith("ative") and degree(word[:-5]):
            word = word[:-5]
        elif word.endswith("alize") and degree(word[:-5]):
            word = word[:-3]
    elif word[-1] == 'i':
        if word.endswith("iciti") and degree(word[:-5]):
            word = word[:-3]
    elif word[-1] == 'l':
        if word.endswith("ical") and degree(word[:-4]):
            word = word[:-2]
        elif word.endswith("ful") and degree(word[:-3]):
            word = word[:-3]
    elif word[-1] == 's':
        if word.endswith("ness") and degree(word[:-4]):
            word = word[:-4]
    return word


def step4(word):
    """step4() takes off -ant, -ence etc., in context <c>vcvc<v>.
    >>> step4("revival")
    'reviv'
    >>> step4("inference")
    'infer'
    >>> step4("allowance")
    'allow'
    >>> step4("airliner")
    'airlin'
    >>> step4("gyroscopic")
    'gyroscop'
    >>> step4("adjustable")
    'adjust'
    >>> step4("defensible")
    'defens'
    >>> step4("irritant")
    'irrit'
    >>> step4("replacement")
    'replac'
    >>> step4("adjustment")
    'adjust'
    >>> step4("dependent")
    'depend'
    >>> step4("adoption")
    'adopt'
    >>> step4("homologou")
    'homolog'
    >>> step4("communism")
    'commun'
    >>> step4("activate")
    'activ'
    >>> step4("angulariti")
    'angular'
    >>> step4("homologous")
    'homolog'
    >>> step4("effective")
    'effect'
    >>> step4("bowdlerize")
    'bowdler'
    """
    if word[-2] == 'a':
        if word.endswith("al") and degree(word[:-2]):
            return word[:-2]
    elif word[-2] == 'c':
        if word.endswith("ance") and degree(word[:-4]):
            return word[:-4]
        elif word.endswith("ence") and degree(word[:-4]):
            return word[:-4]
    elif word[-2] == 'e':
        if word.endswith("er") and degree(word[:-2]):
            return word[:-2]
    elif word[-2] == 'i':
        if word.endswith("ic") and degree(word[:-2]):
            return word[:-2]
    elif word[-2] == 'l':
        if word.endswith("able") and degree(word[:-4]):
            return word[:-4]
        elif word.endswith("ible") and degree(word[:-4]):
            return word[:-4]
    elif word[-2] == 'n':
        if word.endswith("ant") and degree(word[:-3]):
            return word[:-3]
        elif word.endswith("ement") and degree(word[:-5]):
            return word[:-5]
        elif word.endswith("ment") and degree(word[:-4]):
            return word[:-4]
        elif word.endswith("ent") and degree(word[:-3]):
            return word[:-3]
    elif word[-2] == 'o':
        if word.endswith("ion") and (word[-4] == 's' or word[-4] == 't') and degree(word[:-3]):
            return word[:-3]
        elif word.endswith("ou") and degree(word[:-2]):
            return word[:-2]
    elif word[-2] == 's':
        if word.endswith("ism") and degree(word[:-3]):
            return word[:-3]
    elif word[-2] == 't':
        if word.endswith("ate") and degree(word[:-3]):
            return word[:-3]
        elif word.endswith("iti") and degree(word[:-3]):
            return word[:-3]
    elif word[-2] == 'u':
        if word.endswith("ous") and degree(word[:-3]):
            return word[:-3]
    elif word[-2] == 'v':
        if word.endswith("ive") and degree(word[:-3]):
            return word[:-3]
    elif word[-2] == 'z':
        if word.endswith("ize") and degree(word[:-3]):
            return word[:-3]
    return word


def step5(word):
    """step5() removes a final -e if m() > 1, and changes -ll to -l if
    m() > 1.

    >>> step5('probate')
    'probat'
    >>> step5('rate')
    'rate'
    >>> step5('cease')
    'ceas'

    >>> step5('controll')
    'control'
    >>> step5('roll')
    'roll'

    """
    if word[-1] == 'e':
        a = degree(word[:-1])
        if a > 1 or (a == 1 and not cvc(word[:-1])):
            return word[:-1]
    if word[-1] == 'l' and doublec(word) and degree(word[:-1]) > 1:
        return word[:-1]
    return word


def stem(word):
    """
    Function for Porter stemmer
    Algorithm:
    First apply lowercase so that case no longer is an issue
    Treat all the consonantal y's as a separate letter Y
    Apply all the steps as detailed in https://tartarus.org/martin/PorterStemmer/def.txt to the words as functions
    Convert back the consonantal Y to y if any

    >>> stem('controlled')
    'control'
    """
    for function in str.lower, consonant_y, step1ab, step1c, step2, step3, step4, step5, str.lower:
        word = function(word)
    return word


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
