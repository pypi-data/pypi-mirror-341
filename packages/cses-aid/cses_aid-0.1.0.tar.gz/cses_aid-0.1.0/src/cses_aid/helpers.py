from typing import List, Tuple, Dict
import sys
from collections import defaultdict, deque
import math


def fast_input() -> List[str]:
    """
    Read all input lines from stdin at once.

    Returns
    -------
    List[str]
        List of strings containing all input lines.

    Notes
    -----
    This function is particularly useful for competitive programming environments
    where reading all input at once is more efficient.
    """
    return sys.stdin.read().splitlines()


def binary_search(arr: List[int], target: int) -> int:
    """
    Perform binary search on a sorted array.

    Parameters
    ----------
    arr : List[int]
        Sorted array to search in.
    target : int
        Value to search for.

    Returns
    -------
    int
        Index of the target if found, -1 otherwise.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def prefix_sums(arr: List[int]) -> List[int]:
    """
    Compute prefix sums of an array.

    Parameters
    ----------
    arr : List[int]
        Input array of integers.

    Returns
    -------
    List[int]
        Prefix sum array where result[i] = sum(arr[0] to arr[i-1]).
        The first element is 0.
    """
    result = [0]
    for num in arr:
        result.append(result[-1] + num)
    return result


def sieve(limit: int) -> List[int]:
    """
    Generate list of prime numbers using Sieve of Eratosthenes.

    Parameters
    ----------
    limit : int
        Upper bound for prime number generation.

    Returns
    -------
    List[int]
        List of prime numbers up to the given limit.

    Notes
    -----
    The Sieve of Eratosthenes is an ancient algorithm for finding all prime numbers
    up to any given limit. It does so by iteratively marking the multiples of each
    prime number starting from 2.
    """
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]


def gcd(a: int, b: int) -> int:
    """
    Compute greatest common divisor using Euclid's algorithm.

    Parameters
    ----------
    a : int
        First number.
    b : int
        Second number.

    Returns
    -------
    int
        Greatest common divisor of a and b.
    """
    while b:
        a, b = b, a % b
    return a


def bfs(adj: Dict[int, List[int]], start: int) -> List[int]:
    """
    Perform Breadth-First Search on a graph.

    Parameters
    ----------
    adj : Dict[int, List[int]]
        Adjacency list representation of the graph.
    start : int
        Starting node for BFS.

    Returns
    -------
    List[int]
        Order of visited nodes during BFS traversal.
    """
    visited = set()
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(adj[node])
    return order


def dfs(adj: Dict[int, List[int]], start: int) -> List[int]:
    """
    Perform Depth-First Search on a graph.

    Parameters
    ----------
    adj : Dict[int, List[int]]
        Adjacency list representation of the graph.
    start : int
        Starting node for DFS.

    Returns
    -------
    List[int]
        Order of visited nodes during DFS traversal.

    Notes
    -----
    The implementation uses an iterative approach with a stack to avoid
    recursion depth limits on large graphs.
    """
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            stack.extend(reversed(adj[node]))  # Reverse to preserve original order
    return order


def count_bits(n: int) -> int:
    """
    Count the number of set bits in an integer's binary representation.

    Parameters
    ----------
    n : int
        Integer to count bits for.

    Returns
    -------
    int
        Number of set bits (1s) in the binary representation.
    """
    return bin(n).count("1")


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome.

    Parameters
    ----------
    s : str
        String to check.

    Returns
    -------
    bool
        True if the string is a palindrome, False otherwise.
    """
    return s == s[::-1]


def mod_exp(base: int, exp: int, mod: int) -> int:
    """
    Compute modular exponentiation efficiently.

    Parameters
    ----------
    base : int
        Base number.
    exp : int
        Exponent.
    mod : int
        Modulus.

    Returns
    -------
    int
        Result of (base ** exp) % mod.

    Notes
    -----
    This implementation uses the fast modular exponentiation algorithm,
    which is more efficient than computing the power first and then
    taking the modulus.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result
