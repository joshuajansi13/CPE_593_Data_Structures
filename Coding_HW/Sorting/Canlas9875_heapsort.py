import math


def swap(l, a, b):
    l[a], l[b] = l[b], l[a]
    return l


def maxHeapify(numList, idx):
    left_node = (2 * idx) + 1 # left child node
    right_node = (2 * idx) + 2 # right child node
    largest = idx

    if left_node < len(numList) and numList[left_node] > numList[idx]:
        largest = left_node
    if right_node < len(numList) and numList[right_node] > numList[largest]:
        largest = right_node
    if largest != idx:
        numList = swap(numList, idx, largest)
        maxHeapify(numList, largest)


def buildMaxHeap(numList):
    midIdx = math.floor(len(numList) / 2) - 1
    for idx in range(midIdx, -1, -1):
        maxHeapify(numList, idx)
    


def heapsort(numList):
    for idx in range(len(numList)):
        swap( numList, 0, len(numList) - (idx+1) ) # swap the root and last item of the heap
        tempList = numList[ 0:len(numList) - (idx+1) ]
        maxHeapify( tempList, 0 )
        numList[0:len(numList) - (idx+1)] = tempList
        print( f"Heapsort round {idx+1}: {numList}" )


# Main code for testing heapsort
userInput = input('Please enter a list of integers separated by spaces:\n')
numList = [int(x) for x in userInput.split()]
print(f"User input: {numList}")

# Call buildMaxHeap
buildMaxHeap(numList)
print(f"buildMaxHeap output: {numList}")

# Call heapsort (no need to call buildMaxHeap again)
heapsort(numList)

