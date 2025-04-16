#initiator

#Edit distance
def edit_distance(str1, str2):
    m, n = len(str1), len(str2)
    
    # Create a 2D matrix to store distances
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill the matrix
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty
            if i == 0:
                dp[i][j] = j  # insert all characters of str2

            # If second string is empty
            elif j == 0:
                dp[i][j] = i  # remove all characters of str1

            # If last characters are the same
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last characters are different
            else:
                dp[i][j] = 1 + min(
                    dp[i][j-1],    # Insert
                    dp[i-1][j],    # Remove
                    dp[i-1][j-1]   # Replace
                )

    return dp[m][n]

#testing
word1 = "cat"
word2 = "cot"
distance = edit_distance(word1, word2)
print(f"Edit distance between '{word1}' and '{word2}' is: {distance}")

