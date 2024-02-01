# Made by Saverio Scumaci (saverio2514@gmail.com)
#
# Solves iMessage Game Word Hunt
# In the game, the player sees a 4x4 grid and attempts to make as many
# words as possible in the allotted time frame. The longer the word,
# the more points it is worth. 
#
# Uses DFS and a Trie instead of a dictionary to increase solving 
# 
# credits: 
# Nathan Ang https://medium.com/@nathan_149/never-lose-in-wordhunt-again-with-computer-science-bb09ad5015ee
# https://github.com/nathan-149
# Dictionary from: https://boardgames.stackexchange.com/questions/38366/latest-collins-scrabble-words-list-in-text-file
# Collins Scrabble Words (2019).txt

class TrieNode():                                          #Initialize node
    def __init__(self):
        self.children = {}
        self.is_complete_word = False
        

def make_trie():                                           #Puts all of dictionary.txt into a trie
    root = TrieNode()
    with open("dictionary.txt", "r") as dictionary_file:
        for word in dictionary_file:
            curr = root
            word = word.strip()
            for letter in word:
                if letter not in curr.children:
                    curr.children[letter] = TrieNode()
                curr = curr.children[letter]
            curr.is_complete_word = True
    return root

            
def make_board(read):                                       #Makes 4x4 game board and fills it in with "read" input
    board = [[0] * 4 for _ in range(4)]
    index = 0
    for i in range(len(board)):
        for j  in range(len(board[0])):
            board[i][j] = read[index]
            index += 1
    return board
    

def recurse(row, col, word, path, visited, node, board, ans):#Recursively search for words with backtracking
    print("entered")
    if row < 0 or col < 0 or row >= 4 or col >= 4:
        return 
    if visited[row][col]:
        return
    letter = board[row][col]
    if letter not in node.children:
        return 
    
    word += letter
    visited[row][col] = True

    if len(word) > 3 and node.children[letter].is_complete_word:
        # Add valid word and its path to the result list
        ans.append((word, path))

    directions = [(1, 0, ", D"), (0, 1, ", R"), (-1, 0, ", U"), (0, -1, ", L"),(1, -1, ", LD"), 
                  (-1, 1, ", RU"), (1, 1, ", RD"), (-1, -1, ", LU")]
    
    for x,y,z in directions:
        if 0 <= row + x < 4 and 0 <= col + y < 4 and not visited[row + x][col + y]:
            recurse(row + x, col + y, word, path + z, visited, node.children[letter], board, ans)

    visited[row][col] = False


def word_hunt_solver():                                     #Get player input and send it to helper methods, then return answer
    root = make_trie()
    print("Enter the Board")
    read = input().strip().upper()
    
    #check that input is the right size
    if len(read) != 16:
        while(len(read) != 16):
            print("Wrong size, enter 16 characters")
            read = input().strip().upper()

    board = make_board(read)
    visited = [[False] * len(board[0]) for _ in range(len(board))]
    ans = []

    for i in range(4):
        for j in range(4):
            recurse(i, j, "", f"({i}, {j})", visited, root, board, ans)

    #Sort the results in descending order based on word length
    ans.sort(key=lambda x: len(x[0]))

    for i, (word, path) in enumerate(ans):
        print(f"{len(ans) - i}: {word}\n   {path}\n\n")

    input("Press Enter to exit")


if __name__ == "__main__":
    word_hunt_solver()
