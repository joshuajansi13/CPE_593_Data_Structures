def swap(l, a, b):
    l[a], l[b] = l[b], l[a]
    return l


def quicksort(numList):
    iteration = 1
    recursiveQuicksort(numList, 0, len(numList) - 1, iteration)


def recursiveQuicksort(numList, left, right, iter):
    if left >= right:
        return numList
    else:
        pivot_index = lomuto_partition(numList, left, right)
        print(f"Quicksort round {iter}: {numList}")
        print(f"Pivot index = {pivot_index}")
        print(f"Pivot value = {numList[pivot_index]} \n")

        iter += 1
        recursiveQuicksort(numList, left, pivot_index - 1, iter)
        recursiveQuicksort(numList, pivot_index + 1, right, iter)


def lomuto_partition(numList, leftPtr, rightPtr):
    pivot = numList[rightPtr]

    while True:
        while (leftPtr < rightPtr) and (numList[leftPtr] < pivot):
            leftPtr += 1
        while (rightPtr > leftPtr) and (numList[rightPtr] > pivot):
            rightPtr -= 1
        if leftPtr >= rightPtr:
            break
        else:
            swap(numList, leftPtr, rightPtr)

    return leftPtr


# Main code for testing quicksort
userInput = input('Please enter a list of integers separated by spaces:\n')
numList = [int(x) for x in userInput.split()]

print(f"User input: {numList} \n")

quicksort(numList)
print(f"List after quicksort: {numList}")
