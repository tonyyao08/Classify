from fuzzywuzzy import fuzz
# test whether our comparison function will return same or lower accuracy for similar matching text

str1 = "virginia"

# same text test
f1 = fuzz.ratio("virginia", str1)
print("virginia matches to " + str1 + " with " + str(f1) + " percent accuracy")
f2 = fuzz.token_sort_ratio("virginia", str1)
print("virginia matches to " + str1 + " with " + str(f2) + " percent accuracy")
print()
# similar text test
f3 = fuzz.ratio("west virginia", str1)
print("west virginia matches to " + str1 + " with " + str(f3) + " percent accuracy")
f4 = fuzz.token_sort_ratio("west virginia", str1)
print("west virginia matches to " + str1 + " with " + str(f4) + " percent accuracy")

# check if matching same word returns higher accuracy than similar words
assert(f1 > f3 and f2 > f4) 
print("EVERYTHING PASSED")