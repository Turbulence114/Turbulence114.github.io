def latency_aware_resource_assembling(A, L):
    A.sort(reverse=True)
    
    # Initialize dictionary for storing paths
    MAP = {}

    # Initialize route list
    ROUTE = []

    def SUM_ALL(arr):
        return sum(arr)

    def INITILAIZE_DICT(MAP):
        MAP.clear()

    def SELECT_MIN_VALUE(MAP):
        # Select the path with minimum value from MAP
        if not MAP:
            return None
        return min(MAP, key=MAP.get)

    def COMPUTE_ALL(i, r, j):
        return sum([A[i]] + [A[idx] for idx in r] + [A[j]])

    def PATH(i, r, j):
        # Generate a path string based on indices
        return (i, tuple(r), j)

    def SPLIT(value, alpha_L):
        # Split the value into pieces if it exceeds alpha_L
        return value - alpha_L

    def STORE(A, i, j, r):
        if (A[i] + SUM_ALL(r) + A[j] < L and j == len(A)) or j >= len(A):
            path = SELECT_MIN_VALUE(MAP)
            if path:
                ROUTE.append(path)
                A = [A[k] for k in range(len(A)) if k not in path[1]]
            INITILAIZE_DICT(MAP)
            r.clear()
            return

        if A[i] + SUM_ALL(r) + A[j] > L:
            T = COMPUTE_ALL(i, r, j)
            MAP[PATH(i, r, j)] = T
            if A[i] + SUM_ALL(r) + A[j] >= alpha * L:
                piece = SPLIT(A[j], alpha * L)
                A.append(piece)
                A.sort(reverse=True)
            STORE(A, i, j + 1, r)
        else:
            r.append(j)
            STORE(A, i, j + 1, r)

    # Initialize variables
    r = []
    INITILAIZE_DICT(MAP)
    alpha = 0.3

    while SUM_ALL(A) >= L and A:
        i = 0
        STORE(A, i, i + 1, r)

    return ROUTE

