#!/usr/bin/python3
#
# Summary
# This tool generates a list of John the Ripper permutation rules for mixed l33t translations.
#
# Details
# I had the need for a mixed l33t rule (3xample), as oppsed to the common replace-all l33t rule (3xampl3) that I often come across.
# Googling wasn't giving me good results, so I built my own mixed l33t rule. Since there are many variations
# of l33t translations (s = 5 or $, T = 7, etc), I made the tool configurable, so you can simply enter in which
# characters you want translated and to what. A basic, default L33t Translation Table is already in place, but
# you can add other transltions to your heart's desire.
#
# How to Use
# 1. Configure the L33t Translation Table to your liking
# 2. Run the script to generate your mixed l33t ruleset `python3 generate_mixed_l33t.py`
# 3. Copy paste the output ruleset into your john.conf file
# 4. Try it out: `john -w:words.txt -rule:mixed_l33t --stdout | sort | uniq`
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

import itertools

# L33t Translation Table
# Which chars to you want to translate into l33t?
CHARS = {
    "a": "4",
    "s": "$",
    "e": "3",
    # "t": "7",
    # "i": "1",
    # ...Optionally add more translations...
}

# Advanced Setup: How many different chars would you like replaced in the word?
# example: testadmin => [t3st4dm1n, test4dm1n, 7es74dm1n, ...] would be 3, because i only want 3 or less diff chars changed during any given permutation
# This is useful when you don't want to generate so many output permutations, but still want many diff chars permutated
TOTAL_DIFF_LETTERS = len(CHARS.items())

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

# Simple rules output - one rule at a time
all_options = []
for initial_char in CHARS.keys():
    for key in RULES_TEMPLATES.keys():
        rule = CHARS[initial_char][key]
        all_options.append(rule)
        # print(rule)


def strip_dup_char_rules(rules_input):
    """Ensure a line of rules doesn't have multiple rules for a single character."""
    chars_list = []
    results = []
    for rule in rules_input:
        # Get the char that will be altered
        char = rule[-3]
        if char not in chars_list:
            chars_list.append(char)
            results.append(rule)
    return results


# Generate every possible combination of rules, 1-rules-long
results = []
for i in range(0, TOTAL_DIFF_LETTERS):
    combos = list(itertools.combinations(all_options, i + 1))
    for combo in combos:
        rule_list = strip_dup_char_rules(combo)
        results.append(rule_list)

# Remove rules that do the same thing
# Example: /a op[a4] /s op[s$] and /s op[s$] /a op[a4]
# TODO: Not sure if this is having any affect
filtered_rules = []
for rule_list in results:
    for test_against in results:
        if len([i for i in test_against if i in rule_list]) == len(rule_list):
            # if test_against != rule_list:
            #     print("Here is a duplicate rule: {rule_list} and {test_against} ")
            #     exit()
            break
    filtered_rules.append(rule_list)

# Convert rules from python list to rules line
lines_results = []
for rule_list in filtered_rules:
    rule_line = " ".join(rule_list)
    lines_results.append(rule_line)

# Remove duplicate entries
uniq_res = set(lines_results)

# Print rulesets for insertion into john.conf
print(RULENAME)
for rule_line in uniq_res:
    print(rule_line)
