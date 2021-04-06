phones = ['p','b','t','d','k','g','?','tS','dZ','s','S','h','m','n','N','l','r','j','w','i','e','6','a','o','u','aj','6j','ej','oj','uj','aw','6w','iw','ow','f','v','z','Z','T','D','I','e','{','3','@','A','V','U']

def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list

with open('lexicon.txt','r') as f:
    for line in f:
        tmp = line.split(' ',1);
        ps = unique(tmp[1].split(' '));
        for p in ps:
            if(p not in phones)
                print("In word"+tmp[0]+": "+p+" is not a phone.")
        