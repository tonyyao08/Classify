# check if two words are similar enough to return as equal
# will accept words that have characters all in the same place, but
# one or two mismatched characters based off original word length
def match_text(s1, s2):
    if s1 == s2:
        return True
    else:
        # convert words to char array to check for one off errors
        char_array1 = [char for char in s1]
        char_array2 = [char for char in s2]
        # get smallest and biggest length
        l1 = len(char_array1)
        l2 = len(char_array2)
        min_length = l1 if l1 < l2 else l2
        max_length = l1 if l1 > l2 else l2
        # initalize number of mismatched chars to difference between lengths 
        mismatch_count = max_length - min_length
        # accept one or more errors for words with > 2 characters
        if min_length < 3:
            return False
        return close_enough(char_array1, char_array2, min_length, mismatch_count)

# check if 2 words are close enough to be counted as the same
def close_enough(c1, c2, min_length, mismatch_count):
    # count occurences of mismatched characters
    for i in range(min_length):
        if c1[i] != c2[i]:
            mismatch_count+=1
    # accept 1 mismatch for words with length < 5
    if min_length < 5:
        return True if mismatch_count <= 1 else False
    else: # accept 2 mismatches for words with length >= 5
        return True if mismatch_count <= 2 else False

print(match_text("hellioi", "helloik"))



    
