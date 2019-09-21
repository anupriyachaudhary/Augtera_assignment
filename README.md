## INSTRUCTIONS:

#### 1. FileReader
    $dotnet build
    $dotnet run file_path

    (requires .NET core SDK 2.1 to run: https://dotnet.microsoft.com/download/dotnet-core/2.1)

#### 2. Scrabble
    $python Scrabble.py value_file_path dictionary_path

#### 3. IPAddressClustering
    $python IPAddressClustering.py config_file_path


## ANALYSIS

#### 1. FileReader
Time Complexity = O(n)

- Question: Your program should scale with more CPUs, i.e., your program should run faster as more CPUs are available.
- As we need to stream the file before calculating the unique word count, parallelizing the wordcount logic will not improve file read time. Also, the word count calculation is happening in memory, this will be a fast operation and will not improve the overall run time as the context switching overhead will be more than the actual dictionary lookup. 

#### 2. Scrabble
- Using an hash map for storing the values and doing look up is O(n^2) complexity.
- But if we implement a suffix array then it will be O(n)+O(m*largestSizeOf(Pattern)) , where m = no. of patterns and n = size of string
- So, if O(m*largestSizeOf(Pattern)) << O(n^2), suffix array would have been a better option

#### 3. IPAddressClustering
- Used a trie like structure to store the IP addresses and corresponding traffic
- Complexity = O(n) (,where n is number of IP addresses), building the the tree requires O(n) time and searching for subnet is constant time since depth is fixed i.e. 32


