from collections import Counter
import heapq

#Build a structure for Huffman node
class HuffmanNode:
    def __init__(self, char, freq):
        self.char  = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq


#read file and compute probabilities for letters respectively
def get_probabilities(file_path):
    #open text
    with open(file_path, 'r', encoding = 'utf-8') as file:
        text = file.read().lower()
    
    #extract letters and compute frequencies
    letter_counts = Counter(char for char in text if char.isalpha())
    total_counts = sum(letter_counts.values())
    
    probabilities = {letter: freq / total_counts for letter, freq in letter_counts.items()}
    return probabilities


# function for building the Huffman tree (Not reverse)
def build_tree(probabilities):
    # Create priority queue to obtain the node with smallest probability
    heap = [HuffmanNode(char, freq) for char, freq in probabilities.items()]
    heapq.heapify(heap)
    
    while (len(heap) > 1):
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    #return the root node
    return heap[0]

# function for assigning binary strings to letters
def compute_strings (node, prefix = '', code_map = {}):
    if node is not None:
        if node.char is not None:
            code_map[node.char] = prefix
        
        compute_strings (node.left, prefix + '0', code_map)
        compute_strings (node.right, prefix + '1', code_map)
    
    return code_map

# function for computing the average number of bits used per letter
def compute_average (probabilities, code_map):
    return sum(probabilities[char] * len(string) for char, string in code_map.items())


def main():
    file_path = "words_alpha.txt"
    probabilities = get_probabilities(file_path)
    
    #build the Huffman tree to get the root node and assign strings
    r_node = build_tree(probabilities)
    code_map = compute_strings(r_node)
    
    #compute average bits used per letter
    avg = compute_average(probabilities, code_map)
    
    print("\nHuffman Codes:")
    for char, string in code_map.items():
        print(f"{char}: {string}")
   
    print("")
    print(f"\nAverage number of bits used per letter: {avg:.6f}")
   

main()