#!/usr/bin/python3
#
# Summary
# This tool generates a list of John the Ripper permutation rules for mixed l33t translations.
#
# Details
# I had the need for a mixed l33t rule, as oppsed to "replace all X letters with Y letter" l33t, and I wasn't finding
# solutions from public searches, so I built my own mixed l33t rule. Given there are many variations
# of l33t translations (s = 5 or $, T = 7, etc), I made the tool configurable, so you can simply enter in which
# characters you want translated and to what. A basic, default L33t Translation Table is already in place, but
# you can add other transltions to your heart's desire.
#
# How to Use
# 1. Configure the L33t Translation Table to your liking
# 2. Run the script to generate your mixed l33t ruleset `python3 generate_mixed_l33t.py`
# 3. Copy paste the output ruleset into your john.conf file
#
# Example output:
# [List.Rules:mixed_l33t]
# /a op[a4]
# %2a op[a4] /a op[a4]
# %3a op[a4] %2a op[a4] /a op[a4]
# /s op[s$]
# %2s op[s$] /s op[s$]
# %3s op[s$] %2s op[s$] /s op[s$]
# /e op[e3]
# %2e op[e3] /e op[e3]
# %3e op[e3] %2e op[e3] /e op[e3]
#

import random
import re
import copy

# L33t Translation Table
# Which chars to you want to translate into l33t?
CHARS = {
    "a": "4",
    "s": "$",
    "e": "3",
    # ...Optional: add more translations...
}

# Rule name
RULENAME = "[List.Rules:mixed_l33t]"

# Default Rules Templates
# These basic rules cover most cases for mixed l33t permutations.
# /char means select first occurrent of char (then permutate based on following rule)
# op[char_list] means generate multiple permutations by replacing input char with each char in char_list
# %,num,char means only generate permuration from this rule line if char exists at least num times
RULES_TEMPLATES = {
    "single": "/{old} op[{old}{new}]",
    "double": "%2{old} op[{old}{new}] /{old} op[{old}{new}]",
    "triple": "%3{old} op[{old}{new}] %2{old} op[{old}{new}] /{old} op[{old}{new}]",
}

# Loop over each char we want to l33t, and generate the l33t rules for it
for initial_char in CHARS.keys():
    # Convert user-friendly L33t Tranlation Table into scripting format
    CHARS[initial_char] = {"replacement": CHARS[initial_char]}
    # Generate mixed l33t rules
    for key in RULES_TEMPLATES.keys():
        CHARS[initial_char][key] = RULES_TEMPLATES[key].format(
            old=initial_char, new=CHARS[initial_char]["replacement"]
        )

# Print ruleset for insertion into john.conf
print(RULENAME)

# Simple rules output - one rule at a time
for initial_char in CHARS.keys():
    for key in RULES_TEMPLATES.keys():
        print(CHARS[initial_char][key])

# Complex mix of all rules - attempts to cover every potential combination or mixture of letters
all_options = set()
for initial_char in CHARS.keys():
    for key in RULES_TEMPLATES.keys():
        all_options.add(CHARS[initial_char][key])

print(all_options)
print("...")
print("...")
print("...")


def extract_l33t_chars(str):
    results = []
    if str:
        findings = re.findall("/.", str)
        for f in findings:
            results.append(f.replace("/", ""))
    return results


def is_not_duplicate_char(original_value, potential_appendage, addition):
    # Only if addition isn't of same initial char
    # potential appendage is what we may append this this
    # addition is the running additions we have so far, ready to be appended to original value
    option_being_changed_included_chars = extract_l33t_chars(original_value)
    new_option_l33t_char = extract_l33t_chars(potential_appendage)[0]
    chars_in_addition = extract_l33t_chars(addition)
    if all(
        [
            # new_option_l33t_char not in option_being_changed_included_chars,
            # chars_in_addition not in option_being_changed_included_chars,
            # chars_in_addition not in new_option_l33t_char,
            new_option_l33t_char
            not in chars_in_addition,
        ]
    ):
        return True
    return False


TOTAL_GENERATION_LOOPS = 1000
base_options = copy.deepcopy(all_options)
for i in range(0, TOTAL_GENERATION_LOOPS):
    original_value = random.sample(base_options, 1)[0]
    addition = original_value

    for k in CHARS.keys():
        # Insert randomness to additions
        if random.choice([True, False]):
            potential_appendage = random.sample(base_options, 1)[0]
            if is_not_duplicate_char(original_value, potential_appendage, addition):
                addition += " {}".format(potential_appendage)

    all_options.add(addition)


# PRINTER

for option in all_options:
    print(option)

# for option in all_options:
#     a = extract_l33t_chars(option)
#     print(a)
#     # print(option)
