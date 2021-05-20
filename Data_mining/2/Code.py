import pandas as pd
import itertools

data = pd.read_csv('store_data.csv')
mininimum_support_perc = 20 
confidence_percentage = 70 
num_of_rows, num_of_columns = data.shape


list_of_transaction = []
item_set = {}
for i in range(num_of_rows):
    list_of_transaction.append([str(data.values[i, j]) for j in range(num_of_columns)])
allItems = sorted([item for is_sublist_method in list_of_transaction for item in is_sublist_method if item != 'nan'])


def is_sublist_method(support_count_one, filtered_f1_d):
    for i in support_count_one:
        if i not in filtered_f1_d:
            return False
    return True

def frequancyOfSingleItemSet(items, mininimum_support_perc):
    freqTable = {}
    for item in items:
        if item in freqTable:
            freqTable[item] = freqTable[item] + 1
            item_set[item] = item_set[item] + 1
        else:
            freqTable[item] = 1;
            item_set[item] = 1;


    filteredFreqTable = {}
    for key, value in freqTable.items():
        if (value >= mininimum_support_perc):
            filteredFreqTable[key] = value;

    return freqTable, filteredFreqTable
suppCountOFeach1, support_count_one = frequancyOfSingleItemSet(allItems, mininimum_support_perc)


def freq_of_output_set(support_count_one, list_of_transaction, mininimum_support_perc):
    support_count_one = sorted(list(support_count_one.keys()))
    support_count_one = list(itertools.combinations(support_count_one, 2))
    frequency_tabular = {}
    filtered_f1_d = {}
    for iter1 in support_count_one:
        count = 0
        for iter2 in list_of_transaction:
            if is_sublist_method(iter1, iter2):
                count += 1
        frequency_tabular[iter1] = count
        item_set[iter1] = count
    for key, value in frequency_tabular.items():
        if value >= mininimum_support_perc:
            filtered_f1_d[key] = value

    return frequency_tabular, filtered_f1_d
frequency_tabular, filtered_f1_d = freq_of_output_set(support_count_one, list_of_transaction, mininimum_support_perc)


def freq_triple_item_method(filtered_f1_d, list_of_transaction, mininimum_support_perc):
    filtered_f1_d = list(filtered_f1_d.keys())
    filtered_f1_d = sorted(list(set([item for t in filtered_f1_d for item in t])))
    filtered_f1_d = list(itertools.combinations(filtered_f1_d, 3))
    freq_table_1_sec = {}
    filterd_item_pop_stack = {}
    for iter1 in filtered_f1_d:
        count = 0
        for iter2 in list_of_transaction:
            if is_sublist_method(iter1, iter2):
                count += 1
        freq_table_1_sec[iter1] = count
        item_set[iter1] = count
    for key, value in freq_table_1_sec.items():
        if value >= mininimum_support_perc:
            filterd_item_pop_stack[key] = value

    return freq_table_1_sec, filterd_item_pop_stack


freq_table_1_sec, filterd_item_pop_stack = freq_triple_item_method(filtered_f1_d, list_of_transaction, mininimum_support_perc)
print (filterd_item_pop_stack)


def freq_of_4_item_method(filterd_item_pop_stack, list_of_transaction, mininimum_support_perc):
    filterd_item_pop_stack = list(filterd_item_pop_stack.keys())
    filterd_item_pop_stack = sorted(list(set([item for t in filterd_item_pop_stack for item in t])))
    filterd_item_pop_stack = list(itertools.combinations(filterd_item_pop_stack, 4))
    freqTableFour = {}
    filteredFreqTableFour = {}
    for iter1 in filterd_item_pop_stack:
        count = 0
        for iter2 in list_of_transaction:
            if is_sublist_method(iter1, iter2):
                count += 1
        freqTableFour[iter1] = count
        item_set[iter1] = count;
    for key, value in freqTableFour.items():
        if value >= mininimum_support_perc:
        
            filteredFreqTableFour[key] = value

    return freqTableFour, filteredFreqTableFour


freqTableFour, filteredFreqTableFour = freq_of_4_item_method(filterd_item_pop_stack, list_of_transaction, mininimum_support_perc)


sets_of_transaction_1 = []
for iter1 in list(filterd_item_pop_stack.keys()):
    subsets = list(itertools.combinations(iter1, 2))
    sets_of_transaction_1.append(subsets)


def finalSelection(allItemset, itemlist):
    return itemlist[allItemset]


list_filteredFreqTableThree = list(filterd_item_pop_stack.keys())


for i in range(0, len(list_filteredFreqTableThree)):
    for iter1 in sets_of_transaction_1[i]:
        A = iter1
        B = set(list_filteredFreqTableThree[i]) - set(iter1)
        confidence_percentage = (finalSelection(list_filteredFreqTableThree[i], item_set) / finalSelection(A, item_set)) * 100
        print("{}    ->       {}  confidence_percentage = {}% {}".format(A, B, confidence_percentage, "STRONG" if (confidence_percentage >= 70) else "WEAK"))

