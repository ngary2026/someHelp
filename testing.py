# Neranti Gary 
# ID:003061486
import re 

class Boggle:
  def __init__(self, grid, dictionary):
    self.grid = [[x.lower() for x in row] for row in grid]
    # Put the words into a hash; same with prefix
    self.dictionary = set(word.lower() for word in dictionary)  # Set for fast lookups
    self.dictionary = self.build_word_prefix_set(dictionary)  # Precompute valid prefixes
    self.solution = set()  # Store unique words found
    self.visited = [[False] * len(grid[0]) for _ in range(len(grid))]  # Track visited cells
    self.directions = [
        (-1,-1),  #up left
        (-1,0),   #up
        (-1,1),   #up right
        (0,1),    #right
        (1,1),    #down right
        (1,0),    #down
        (1,-1),   #down left
        (0,-1),   #left
    ]
    if self.is_valid_grid() and self.is_valid_dict():
      self.find_words()

  def is_valid_grid(self):
    if not self.grid or not all(len(row) == len(self.grid) for row in self.grid):
      return False

    valid_letters = re.compile(r"^(?:[a-p]|qu|r|t|st|[v-z])$")
    for row in self.grid:
      for cell in row:
        if not valid_letters.match(cell.lower()): 
            return False 
    return True

  def is_valid_dict(self):
    for word in self.dictionary:
      if not word.isalpha():
        return False
      
    if not self.dictionary:
      return False
    else:
      return True

  def build_word_prefix_set(self, dictionary):
    prefixes = {}
    for word in dictionary:
      prefixes[word] = 1
      for i in range(1, len(word)):
        p = word[:i]
        if p not in self.dictionary:
          prefixes[p] = 0  
    return prefixes

  def in_bounds(self, x, y):
      return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

  def search(self, x, y, current_word):
    if self.in_bounds(x, y) and not self.visited[x][y]:
      current_word += self.grid[x][y]
        
      # Prune the search if the word is not a valid prefix
      if current_word in self.dictionary:

          # Mark the current cell as visited
          self.visited[x][y] = True

          if(self.dictionary.get(current_word) == 1):
            # Only add the word if it's at least 3 characters long and a valid dictionary word
            if len(current_word) >= 3:
                self.solution.add(current_word)
        
          # Explore all 8 possible directions
          for dx, dy in self.directions:
              new_x, new_y = x + dx, y + dy
              self.search(new_x, new_y, current_word)

      # Unmark the cell after exploration (backtracking)
      self.visited[x][y] = False

  def find_words(self):
    for i in range(len(self.grid)):
      for j in range(len(self.grid[0])):
        self.visited = [[False] * len(self.grid[0]) for _ in range(len(self.grid))]
        self.search(i, j, "")

  def getSolution(self):
      return sorted(self.solution)
        
def main():
  grid = [["T", "W", "Y", "R"], 
          ["E", "N", "P", "H"],
          ["G", "Z", "Qu", "R"],
          ["O", "N", "T", "A"]]
  dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry", "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", "arty", "rhr", "not", "quar"]

  mygame = Boggle(grid, dictionary)
  print(mygame.getSolution())

if __name__ == "__main__":
  main()













  # Neranti Gary 
# ID:003061486
import re 

class Boggle:
  def __init__(self, grid, dictionary):
    self.grid = [[x.lower() for x in row] for row in grid]
    # Put the words into a hash; same with prefix
    self.dictionary = set(word.lower() for word in dictionary)  # Set for fast lookups
    self.prefixes = self.build_word_prefix_set(dictionary)  # Precompute valid prefixes
    self.solution = set()  # Store unique words found
    self.visited = [[False] * len(grid[0]) for _ in range(len(grid))]  # Track visited cells
    self.directions = [
        (-1,-1),  #up left
        (-1,0),   #up
        (-1,1),   #up right
        (0,1),    #right
        (1,1),    #down right
        (1,0),    #down
        (1,-1),   #down left
        (0,-1),   #left
    ]
    if self.is_valid_grid() and self.is_valid_dict():
      self.find_words()

  def is_valid_grid(self):
    if not self.grid or not all(len(row) == len(self.grid) for row in self.grid):
      return False

    valid_letters = re.compile(r"^(?:[a-p]|qu|r|t|st|[v-z])$")
    for row in self.grid:
      for cell in row:
        if not re.match(valid_letters, cell.lower()): 
            return False 
    return True

  def is_valid_dict(self):
    for word in self.dictionary:
      if not word.isalpha():
        return False
      
    if not self.dictionary:
      return False
    else:
      return True

  def build_word_prefix_set(self, dictionary):
    prefixes = set()
    for word in dictionary:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])
    return prefixes

  def in_bounds(self, x, y):
      return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

  def search(self, x, y, current_word):
    if self.in_bounds(x, y) or not self.visited[x][y]:
        return
    
    current_word += self.grid[x][y]
        
    # Prune the search if the word is not a valid prefix
    if current_word not in self.dictionary:
        return

    if len(current_word) >= 3 and current_word in self.dictionary:
        self.solution.add(current_word)

    # Mark the current cell as visited
    self.visited[x][y] = True
        
    # Explore all 8 possible directions
    for dx, dy in self.directions:
        new_x, new_y = x + dx, y + dy
        self.search(new_x, new_y, current_word)

      # Unmark the cell after exploration (backtracking)
    self.visited[x][y] = False

  def find_words(self):
    self.solution.clear()
    for i in range(len(self.grid)):
      for j in range(len(self.grid[0])):
        self.visited = [[False] * len(self.grid[0]) for _ in range(len(self.grid))]
        self.search(i, j, "")
    return list(self.solution)

  def getSolution(self):
    return sorted(self.find_words())
        
def main():
  grid = [["T", "W", "Y", "R"], 
          ["E", "N", "P", "H"],
          ["G", "Z", "Qu", "R"],
          ["O", "N", "T", "A"]]
  dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry", "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went", "wet", "arty", "rhr", "not", "quar"]

  mygame = Boggle(grid, dictionary)
  print(mygame.getSolution())

if __name__ == "__main__":
  main()