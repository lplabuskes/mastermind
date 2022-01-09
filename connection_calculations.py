import time

def comparison(code1, code2, code_length=4, color_count=6):
    count1 = [0] * color_count
    count2 = [0] * color_count
    black_count = 0
    for i in range(code_length):
        count1[code1[i]] += 1
        count2[code2[i]] += 1
        if code1[i] == code2[i]:
            black_count += 1
    white_count = sum([ min(count1[i], count2[i]) for i in range(color_count) ]) - black_count
    return (black_count, white_count)

def possible_codes(code_length=4, color_count=6):
    codes = [[]]
    for i in range(code_length):
        new_codes = []
        for code in codes:
            for j in range(color_count):
                new_codes.append(code+[j])
        codes = new_codes
    return codes

def compute_relationships(code_length=4, color_count=6):
    all_codes = possible_codes(code_length, color_count)
    all_relations = [[0]*i for i in range(len(all_codes))] # Any code compared with itself is the trivial all-black, comp(a,b) = comp(b,a)
    for idx, code in enumerate(all_codes):
        for j in range(idx):
            all_relations[idx][j] = comparison(code, all_codes[j], code_length, color_count)
    return all_relations

def minimax_structure(code_length=4, color_count=6):
    relationship_array = compute_relationships(code_length, color_count)
    code_relations = [{} for i in range(len(relationship_array))]

    for i, code_set in enumerate(relationship_array):
        code_relations[i][(color_count, 0)] = [i] # all black <==> code compared with self
        for j, result in enumerate(code_set):
            if result in code_relations[i]:
                code_relations[i][result].append(j)
            else:
                code_relations[i][result]=[j]

            if result in code_relations[j]:
                code_relations[j][result].append(i)
            else:
                code_relations[j][result]=[i]
    return code_relations

if __name__ == "__main__":
    start = time.time()
    structure = minimax_structure()
    end = time.time()
    print(end-start)