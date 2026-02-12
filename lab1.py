import random

def generate_random_string(n):
    result = ''
    characters = 'ab'
    
    for _ in range(n):
        random_index = random.randint(0, len(characters) - 1)
        result += characters[random_index]
    
    return result

def find_all_substring_positions(string, substring):
    positions = []
    index = string.find(substring)
    
    while index != -1:
        positions.append(index)
        index = string.find(substring, index + 1)
    
    return positions

# Исходные правила
rules = [
    {"from": "aaa", "to": "aaab"},
    {"from": "aabb", "to": "abab"},
    {"from": "aa", "to": "aba"},
    {"from": "aaab", "to": "ab"},
    {"from": "bbb", "to": "baaaa"},
]

def random_reduce(string, count):
    arr = []
    
    for rule in rules:
        poses = find_all_substring_positions(string, rule["from"])
        if len(poses) == 0:
            continue
        
        for pos in poses:
            arr.append({
                "pos": pos,
                "rule": rule
            })
    
    if len(arr) == 0 or count == 6:
        return [string, True]
    
    random_index = random.randint(0, len(arr) - 1)
    el = arr[random_index]
    
    return [string[:el["pos"]] + el["rule"]["to"] + string[el["pos"] + len(el["rule"]["from"]):], False]

def random_normalize(string1):
    count_rules = 0
    while True:
        string, res = random_reduce(string1, count_rules)
        count_rules += 1
        if res:
            return string
        string1 = string

# Минимальные правила
rules1 = [
    {"from": "aba", "to": "aa"},
    {"from": "aaa", "to": "ab"},
    {"from": "abb", "to": "ab"},
    {"from": "bbb", "to": "baa"},
    {"from": "aab", "to": "aa"},
    {"from": "bab", "to": "ab"},
    {"from": "baa", "to": "aa"},
]

def fuzz(str1, str2):
    norm_str1 = None
    way = []
    err = False

    def normalize(temp_str, with_way=False):
        nonlocal norm_str1, err
        if with_way and temp_str == norm_str1:
            return
        
        found = False
        for i in range(len(rules1)):
            rule = rules1[i]
            pos = temp_str.find(rule["from"])
            if pos != -1:
                new_str = temp_str[:pos] + rule["to"] + temp_str[pos + len(rule["from"]):]
                if with_way:
                    way.append(i)
                normalize(new_str, with_way)
                found = True
                break
        
        if not found and with_way and temp_str != norm_str1:
            err = True
            return
        
        if not found and not with_way:
            norm_str1 = temp_str

    normalize(str1)
    normalize(str2, True)
    
    if err:
        return False
    if len(way) == 0:
        return True
    
    way.reverse()
    res = False
    mem = set()
    
    def dfs(temp_str, index_way):
        nonlocal res
        if index_way == len(way):
            return
        if temp_str == str2 or res:
            res = True
            return
        if temp_str in mem:
            return
        
        mem.add(temp_str)
        rule_index = way[index_way]
        rule = rules1[rule_index]
        poses = find_all_substring_positions(temp_str, rule["to"])
        
        for pos in poses:
            dfs(temp_str[:pos] + rule["from"] + temp_str[pos + len(rule["to"]):], index_way + 1)
    
    dfs(str2, 0)
    return res

def first_compare(str1, str2):
    if 'a' in str1:
        return 'a' in str2
    return True

def second_compare(str1, str2):
    count_a1 = str1.count('a')
    count_a2 = str2.count('a')
    return count_a1 % 2 == count_a2 % 2

def random_reduce1(string, count):
    arr = []
    
    for rule in rules1:
        poses = find_all_substring_positions(string, rule["from"])
        if len(poses) == 0:
            continue
        
        for pos in poses:
            arr.append({
                "pos": pos,
                "rule": rule
            })
    
    if len(arr) == 0 or count == 5:
        return [string, True]
    
    random_index = random.randint(0, len(arr) - 1)
    el = arr[random_index]
    
    return [string[:el["pos"]] + el["rule"]["to"] + string[el["pos"] + len(el["rule"]["from"]):], False]

def random_normalize1(string1):
    count_rules = 0
    while True:
        string, res = random_reduce1(string1, count_rules)
        count_rules += 1
        if res:
            return string
        string1 = string

def meta(str1):
    string = random_normalize1(str1)
    return first_compare(str1, string) and second_compare(str1, string)

def testing():
    for i in range(1000):
        test_string = generate_random_string(50)
        reduced_string = random_normalize(test_string)
        
        if i % 100 == 0:
            print(i)
        
        if not ((fuzz(test_string, reduced_string) or 
                (fuzz(reduced_string, test_string))) and 
                meta(test_string)):
            
            if len(test_string) > len(reduced_string) or \
               (len(test_string) == len(reduced_string) and test_string > reduced_string):
                print(test_string, reduced_string)
            else:
                print(reduced_string, test_string)

if __name__ == "__main__":
    testing()