def longest_common_subsequence(a, b):
    m = len(a)
    n = len(b)
    # Create a table with (m+1) rows and (n+1) columns.
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# Test cases using pytest

from correct_python_programsfromcorrect_python_programs import pytest


def test_longest_common_subsequence():
    assert longest_common_subsequence("ABCBDAB", "BDCAB") == 4
    assert longest_common_subsequence("Mturko", "Gurkha") == 3
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abcdgh", "aedfhr") == 3
    assert longest_common_subsequence("ABCXYZ", "ABDWZW") == 3


if __name__ == "__main__":
    pytest.main()
