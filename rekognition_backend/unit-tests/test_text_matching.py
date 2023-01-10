from fuzzywuzzy import fuzz


# look through all label-keyword pairs in database
# if we find a keyword that perfectly matches detected text, return label
# otherwise, keep track of current highest accuracy and label
# return this current highest label in the end if its accuracy > 60%
# otherwise, return unknown

def match_text(user_entered, detected):
    current_best = "None"
    highest_accuracy = 0
    for label in user_entered:
        keywords = user_entered.get(label)
        for detected_text in detected:
            for keyword in keywords:
                str1 = keyword.lower()
                str2 = detected_text.lower()

                # matches whole string accuracy
                f1 = fuzz.ratio(str1, str2)
                if f1 == 100:
                    return(label)
                if highest_accuracy < f1:
                    highest_accuracy = f1
                    current_best = label
                # print(str1 + " was compared to " + str2)
                # print(f1)
                # print()

                # rearranges string into tokens, then sorts and compares whole string
                f3 = fuzz.token_sort_ratio(str1, str2)
                if f3 == 100:
                    return(label)
                if highest_accuracy < f3:
                    highest_accuracy = f3
                    current_best = label
                # print(str1 + " was compared to " + str2)
                # print(f3)
                # print()
                if highest_accuracy > 60:
                    return current_best
                else:
                    return "Unknown"

user_entered = {
    "Wisconsin": ["Wisconsin"],
    "Virginia": ["Virginia"],
}

detected = [
    "WISCONSIN",
    "FORWARD",
    "E PLURIBUS 2004 UNUM",
    "WISCONSIN",
    "FORWARD",
    "E",
    "PLURIBUS",
    "2004",
    "UNUM",
]

matched_text = match_text(user_entered, detected)

assert(matched_text == "Wisconsin") # check if correct state was matched
print("EVERYTHING PASSED")