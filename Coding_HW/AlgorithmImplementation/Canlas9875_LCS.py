import numpy as np


class LCS:
    def __init__(self, A, B) -> None:
        self.A_str = A
        self.B_str = B
        self.LCS_matrix = np.zeros((len(self.A_str)+1, len(self.B_str)+1), dtype=np.int32)

    def fillLCSMatrix(self):
        for i in range(1, np.shape(self.LCS_matrix)[0]):
            for j in range(1, np.shape(self.LCS_matrix)[1]):
                if self.A_str[i-1] != self.B_str[j-1]:
                    self.LCS_matrix[i, j] = 0
                else:
                    self.LCS_matrix[i, j] = self.LCS_matrix[i-1, j-1] + 1

        print(f"LCS matrix:\n{self.LCS_matrix}")

    def getLongestCommonSubstring(self):
        # Output: a list of strings that are the longest common continuous substrings of A and B. Please note that if there are multiple such common substrings, you need to print all of them.
        max = 0
        LCS_ind = []
        for i in range(1, np.shape(self.LCS_matrix)[0]):
            for j in range(1, np.shape(self.LCS_matrix)[1]):
                if self.LCS_matrix[i, j] > max and self.LCS_matrix[i, j] != 0:
                    max = self.LCS_matrix[i, j]
                    LCS_ind.clear()
                    LCS_ind.append((i,j))
                elif self.LCS_matrix[i, j] == max and self.LCS_matrix[i, j] != 0:
                    LCS_ind.append((i,j))

        if len(LCS_ind) == 0:
            print("There are no common continuous substrings between the two inputs.")
            return
        else:
            LCS_list = []
            for indices in LCS_ind:
                str_idx = indices[0] - 1
                substring = self.A_str[str_idx]
                for i in range(0, max-1):
                    str_idx -= 1
                    substring = self.A_str[str_idx] + substring
                LCS_list.append(substring)

            print(f"Longest common continuous substrings: {LCS_list}")
            print(f"Max length: {max}")
        return


# Test LCS class and its methods
inputStr_A = input("Please enter your first string: ")
inputStr_B = input("Please enter your second string: ")

lcs_instance = LCS(inputStr_A, inputStr_B)

# Test fillLCSMatrix
lcs_instance.fillLCSMatrix()

# Test getLongestCommonSubstring
lcs_instance.getLongestCommonSubstring()