import pytest
from ..helpers import (
    fast_input,
    binary_search,
    prefix_sums,
    sieve,
    gcd,
    bfs,
    dfs,
    count_bits,
    is_palindrome,
    mod_exp
)

def test_binary_search():
    # Test with sorted array
    arr = [1, 3, 5, 7, 9]
    assert binary_search(arr, 5) == 2
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 9) == 4
    assert binary_search(arr, 4) == -1  # Not found
    assert binary_search(arr, 10) == -1  # Not found
    
    # Test with empty array
    assert binary_search([], 5) == -1
    
    # Test with single element
    assert binary_search([5], 5) == 0
    assert binary_search([5], 3) == -1

def test_prefix_sums():
    # Test with positive numbers
    assert prefix_sums([1, 2, 3, 4, 5]) == [0, 1, 3, 6, 10, 15]
    
    # Test with negative numbers
    assert prefix_sums([-1, -2, -3]) == [0, -1, -3, -6]
    
    # Test with empty array
    assert prefix_sums([]) == [0]
    
    # Test with single element
    assert prefix_sums([5]) == [0, 5]

def test_sieve():
    # Test with small limit
    assert sieve(10) == [2, 3, 5, 7]
    
    # Test with larger limit
    primes = sieve(20)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19]
    
    # Test with limit less than 2
    assert sieve(1) == []
    assert sieve(0) == []

def test_gcd():
    # Test with positive numbers
    assert gcd(48, 18) == 6
    assert gcd(17, 5) == 1  # Coprime numbers
    
    # Test with zero
    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5
    
    # Test with negative numbers
    assert gcd(-48, 18) == 6
    assert gcd(48, -18) == 6
    assert gcd(-48, -18) == 6

def test_bfs():
    # Test with simple graph
    graph = {
        1: [2, 3],
        2: [4],
        3: [4],
        4: []
    }
    assert bfs(graph, 1) == [1, 2, 3, 4]
    
    # Test with disconnected graph
    graph = {
        1: [2],
        2: [],
        3: [4],
        4: []
    }
    assert bfs(graph, 1) == [1, 2]
    
    # Test with empty graph
    assert bfs({}, 1) == []

def test_dfs():
    # Test with simple graph
    graph = {
        1: [2, 3],
        2: [4],
        3: [4],
        4: []
    }
    assert dfs(graph, 1) == [1, 2, 4, 3]
    
    # Test with disconnected graph
    graph = {
        1: [2],
        2: [],
        3: [4],
        4: []
    }
    assert dfs(graph, 1) == [1, 2]
    
    # Test with empty graph
    assert dfs({}, 1) == []

def test_count_bits():
    # Test with various numbers
    assert count_bits(0) == 0
    assert count_bits(1) == 1
    assert count_bits(2) == 1
    assert count_bits(3) == 2
    assert count_bits(255) == 8
    assert count_bits(256) == 1
    
    # Test with negative numbers
    assert count_bits(-1) == 1  # In Python, -1 is represented as ...11111111

def test_is_palindrome():
    # Test with palindromes
    assert is_palindrome("") == True
    assert is_palindrome("a") == True
    assert is_palindrome("racecar") == True
    assert is_palindrome("madam") == True
    
    # Test with non-palindromes
    assert is_palindrome("hello") == False
    assert is_palindrome("python") == False
    
    # Test with mixed case
    assert is_palindrome("Racecar") == False  # Case sensitive

def test_mod_exp():
    # Test with small numbers
    assert mod_exp(2, 3, 5) == 3  # 2^3 mod 5 = 8 mod 5 = 3
    assert mod_exp(3, 4, 7) == 4  # 3^4 mod 7 = 81 mod 7 = 4
    
    # Test with large numbers
    assert mod_exp(2, 10, 1000) == 24  # 2^10 mod 1000 = 1024 mod 1000 = 24
    
    # Test with zero
    assert mod_exp(0, 5, 7) == 0
    assert mod_exp(2, 0, 7) == 1  # Any number to the power of 0 is 1
    
    # Test with modulus 1
    assert mod_exp(2, 3, 1) == 0  # Any number mod 1 is 0

# Note: fast_input() is not tested here as it requires stdin input
# and is typically used in competitive programming environments 