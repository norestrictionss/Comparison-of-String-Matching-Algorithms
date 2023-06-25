# Comtributors
# Hakki Kokur, Baris Giray Akman, Yasin Kucuk, Musa Ozkan


import time
import psutil

# Horspool Algorithm


def create_bad_symbol_table(pattern):
    # using dict because to gain more speed. mem be sacrificed because of that, we can use 29 length of array.
    bad_symbol_table = dict()
    # calculating length of the pattern outside the loop
    length = len(pattern)
    for ch in set(pattern):
        rigt_most_occurrence = pattern.rfind(ch, 0, -1)
        value = length - rigt_most_occurrence - 1
        bad_symbol_table[ch] = value if value != 0 else length
    bad_symbol_table["others"] = length
    return bad_symbol_table


# Horspool Algorithm
def Horspool(s, pattern, all_indexes):
    comparison_count = 0
    number_of_match = 0

    # Bad match table is created.
    badMatchTable = create_bad_symbol_table(pattern)

    # Index i is set to the last index of the pattern.
    i = len(pattern) - 1

    # While loop is used for iteration along the text.
    while i < len(s):
        k = 0
        
        if s[i-k] != pattern[len(pattern)-k-1]:
            comparison_count+=1
            
        else:

            while k<len(pattern) and s[i-k] == pattern[len(pattern)-k-1]:
                comparison_count+=1
                k+=1

        # If while loop is not broken, it means pattern matches with substring.
        if k == len(pattern):
            all_indexes.append([i - len(pattern) + 1, i + 1])
            number_of_match += 1

           
        
        # Index i is updated according to the bad match table.
        

        i+=badMatchTable.get(s[i], len(pattern))
 
    # Results are displayed via print function.
    print("Number of comparison: ", comparison_count)
    print("Number of matches: ", number_of_match)

    return (number_of_match, all_indexes, comparison_count, badMatchTable)


# Brute force string matching algorithm
def brute_force(s: "string", pattern: "string"):
    all_indexes = list()
    comparison_count = 0
    number_of_match = 0
    # Iteration along the input
    for i in range(len(s) - len(pattern) + 1):
        j = 0
        # Pattern and substring comparison is done through while loop
        while j < len(pattern):
            comparison_count += 1
            # If there is a mismatch, loop will end.
            if s[i + j] != pattern[j]:
                break
            # If while loop is not broken, it means pattern matches with substring.
            j += 1  # 10101010101
        # If loop ends up without break, j must be equal to the length of the pattern.
        # If substring matches the pattern, beginning and ending indexes are stored in the list.
        if (j == len(pattern) and all_indexes == []) or (
            j == len(pattern) and i > all_indexes[-1][1]
        ):
            all_indexes.append([i, i + j - 1])
            number_of_match += 1

        elif (
            j == len(pattern)
            and all_indexes != []
            and i <= all_indexes[-1][1]
            and i >= all_indexes[-1][0]
        ):
            all_indexes[-1][1] = i + j - 1
            number_of_match += 1
    return (number_of_match, all_indexes, comparison_count)


# Boyer more string matching algorithm
def boyer_more(pattern, string):
    def create_bad_symbol_table(pattern):
        # using dict because to gain more speed. mem be sacrificed because of that, we can use 29 length of array.
        bad_symbol_table = dict()
        # calculating length of the pattern outside the loop
        length = len(pattern)
        for ch in set(pattern):
            rigt_most_occurrence = pattern.rfind(ch, 0, -1)
            value = length - rigt_most_occurrence - 1
            bad_symbol_table[ch] = value if value != 0 else length
        bad_symbol_table["others"] = length
        return bad_symbol_table

    def create_good_suffix_table(pattern):
        good_suffix = list()
        length = len(pattern)
        good_suffix.append(length)
        for k in range(1, length+1):
            
            # AT_THAT
            comp_part = pattern[-k:]
            n = -k
            shift_amount = None
            while True:
                n -= 1
                index = length + n
                abs_n = abs(n)
                if abs_n < length and pattern[index : index + k] == comp_part:
                    if pattern[n - 1] != pattern[-k - 1]:
                        shift_amount = abs(n + k)
                        break
                elif abs_n == length and pattern[index : index + k] == comp_part:
                    shift_amount = abs(n + k)
                    break
                elif abs_n > length:
                    num = k + length - abs_n
                    if pattern[:num] == comp_part[-num:]:
                        shift_amount = abs(n + k)
                        break
                    if abs_n == length + len(comp_part):
                        shift_amount = length
                        break
            good_suffix.append(shift_amount)
        return good_suffix

    bad_symbol_table = create_bad_symbol_table(pattern)
    good_suffix_table = create_good_suffix_table(pattern)
    

    len_pat = len(pattern)
    len_str = len(string)
    k = None
    i = len_pat - 1
    found_count = 0
    comparison_count = 0
    found_index = []
    while i < len_str:
        comparison_count += 1
        if pattern[-1] != string[i]:
            i = i + bad_symbol_table.get(
                string[i], bad_symbol_table["others"]
            )  # good_suffix_table[0]
        elif len_pat == 1:
            found_count += 1
            found_index.append(i)
            i = i + bad_symbol_table["others"]
        else:
            k = 1
            i -= 1
            while True:
                comparison_count += 1
                if pattern[-k - 1] == string[i]:
                    if len_pat == (k + 1):
                        found_count += 1
                        found_index.append(i)
                        i = i + bad_symbol_table["others"]
                        break
                    k = k + 1
                    i = i - 1
                else:
                    bad_ch = string[i]
                    shift_amount = max(
                        good_suffix_table[k],
                        bad_symbol_table.get(bad_ch)
                        if bad_symbol_table.get(bad_ch, -1) - k + 1 > 0
                        else bad_symbol_table["others"],
                    )
                    i = i + shift_amount + k
                    break
    return (
        found_count,
        found_index,
        comparison_count,
        bad_symbol_table,
        good_suffix_table,
    )


# That function generates output and inserts the mark sign if necessary
def generate_output(input_file, all_indexes, output_file):
    j = 0
    k = 0
    # If there is no pattern matching in the input, function doesn't have to work anymore.
    if len(all_indexes) == 0:
        return
    # Iteration along the input
    for i in range(len(input_file)):
        # If beginning index is equal to i, label mark must be inserted into the output file.
        if j < len(all_indexes) and i == all_indexes[j][k] and k == 0:
            k += 1
            output_file.write("<mark>")
            output_file.write(input_file[i])
        # If ending index is equal to i, label mark including forward slash must be inserted into the output file.
        elif j < len(all_indexes) and i == all_indexes[j][k]:
            j += 1
            k = 0
            output_file.write(input_file[i])
            output_file.write("</mark>")
        else:
            output_file.write(input_file[i])


# TEST ENVIROMENT

## read input files and add all string to strings one by one

# To insert more string statically, you can use append() method for the list patterns
pattern = "AT_THAT"
patterns = []
patterns.append(pattern)


# To insert more string statically, you can use append() method for the list strings
string = open("input.html", "r")
strings = []

strings.append(string.read())


"""
strings = strings.read()
[
    "<HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML><HTML><BODY>WHICH_FINALLY_HALTS. _ _ AT_THAT POINT</BODY></HTML>"
]

"""

## search each patterin in strings or what??

for pattern in patterns:
    for string in strings:
        print("#" * 100)
        print("pattern: ", pattern)

        print("Results for Boyer Moore Algorithm")
        # (found_count, found_index, comperasion_count, bad_symbol_table, good_suffix_table)
        start_time = time.time()
        result = boyer_more(pattern, string)
        ## output dosyasi yazdirilmali
        end_time = time.time()
        print("Total Match Count: ", result[0])
        print("Total Comperarison Count: ", result[2])
        print(f"Runtime: {end_time-start_time:.5}")
        # bu kisimda bad ve good tablelarin formati uygun olmayabilir

        print("Bad Symbol Table: ")
        for key, value in result[3].items():
            if key == "others":
                print(f"\tFor anothers, Shift Amount: {value}")
            else:
                print(f"\tCharacter: {key}, Shift Amount: {value}")
        print("Good Suffix Table: ")
        for index in range(len(result[4])):
            if index != 0:
                print(f"\tKey: {index}, Shift Amount: {result[4][index]}")
        print(f"\tKey: {len(result[4])}, Shift Amount: {result[4][0]}")
        print("*" * 100)

        print("Results for Brute Force Algorithm")
        start_time = time.time()
        # (found_count, found_index, comparison_count)
        result = brute_force(string, pattern)
        output_file = open("output.html", "w")

        # Generating an output for the HTML file
        generate_output(string, result[1], output_file)
        ## output dosyasi yazdirilmali
        end_time = time.time()
        print("Total Match Count: ", result[0])
        print("Total Comparison Count: ", result[2])
        print(f"Runtime: {end_time-start_time:.5}")

        # Horspool Algorithm
        all_indexes = []
        print("*" * 100)
        print("Results for Horspool Algorithm")
        start_time = time.time()
        result = Horspool(string, pattern, all_indexes)
        end_time = time.time()
        print("Total Match Count: ", result[0])
        print("Total Comperarison Count: ", result[2])
        print(f"Runtime: {end_time-start_time:.5}")
        print("Bad Symbol Table: ")
        for key, value in result[3].items():
            if key == "others":
                print(f"\tFor anothers, Shift Amount: {value}")
            else:
                print(f"\tCharacter: {key}, Shift Amount: {value}")