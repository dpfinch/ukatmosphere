#### Set of tools to help format wordings and images

def PrettyWordList(wordlist):
    if wordlist == 2:
        prettylist = ' & '.join(wordlist)
    else:
        prettylist = ', '.join(wordlist[:-1]) + ' & '+wordlist[-1]
    return [prettylist]
