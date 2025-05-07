def next_permutation(arr):
    # Step 1: Find the first index from the right where arr[i] < arr[i+1]
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return None  # The array is in descending order; no next permutation
    
    # Step 2: Find the smallest element greater than arr[i] to its right
    j = len(arr) - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Step 3: Swap elements at positions i and j
    arr[i], arr[j] = arr[j], arr[i]
    
    # Step 4: Reverse the sub-array from (i+1) to end
    left = i + 1
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    
    return arr