
def get_mots():
    mots_f = []
    mots_m = []
    mots_fm = []

    filename = "./data/nom/fs.txt"
    with open(filename, encoding='utf-8') as lines:
        for mot in lines: 
            mots_f.append(mot.replace("\n", ""))
    filename = "./data/nom/ms.txt"
    with open(filename, encoding='utf-8') as lines:
        for mot in lines: 
            mots_m.append(mot.replace("\n", ""))

    mots_fm = sorted(set(mots_f) | set(mots_m))

    return mots_f, mots_m, mots_fm