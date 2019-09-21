using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace FileReader
{
    class Program
    {
        static void Main(string[] args)
        {
            var inputFilePath = args[0];
            var lineCountFilePath = Path.Combine(GetAssemblyDirectory(), "../../../lineCountFile.txt");
            var uniqueCountFilePath = Path.Combine(GetAssemblyDirectory(), "../../../uniqueCountFile.txt");

            WordCount.Count(inputFilePath, lineCountFilePath, uniqueCountFilePath);
            //WordCount.CountAsync(inputFilePath, lineCountFilePath, uniqueCountFilePath).Wait();
            //CreateFile();
        }

        public static void CreateFile()
        {
            string filePath = Path.Combine(GetAssemblyDirectory(), "data.txt");

            string[] words = { "a", "cat", "mouse", "house", "pig", "three", "ten", "fire", "wolf", "cheese" };

            //long oneGigaBytes = 1024 * 1024 * 1024;
            long oneGigaBytes = 1024;
            long totalBytes = 10 * oneGigaBytes;

            int maxWordsPerLine = 10;
            var writtenBytes = 0L;

            var rand = new Random();

            var writer = new StreamWriter(filePath);

            while (writtenBytes < totalBytes)
            {
                var builder = new StringBuilder();
                var wordsPerLine = rand.Next(maxWordsPerLine) + 1;

                for (int i = 1; i <= wordsPerLine; i++)
                {
                    var word = words[rand.Next(words.Length)];
                    builder.Append(word);
                    if (i != maxWordsPerLine)
                    {
                        builder.Append(" ");
                    }
                }
                var line = builder.ToString();

                writer.WriteLine(line);
                writtenBytes += line.Length;
            }

            writer.Dispose();
        }

        public static string GetAssemblyDirectory()
        {
            string codeBase = Assembly.GetExecutingAssembly().CodeBase;
            UriBuilder uri = new UriBuilder(codeBase);
            string path = Uri.UnescapeDataString(uri.Path);
            return Path.GetDirectoryName(path);
        }
    }

    public static class WordCount
    {
        /// <summary>
        /// Question: Provide your own analysis of pros and cons of the data structure you use, time complexity, etc.
        /// I have used Dictionary. The lookup complexity will be O(1) amortize. As we just need to out the final unique count dictionary seems the best choice
        /// </summary>
        public static void Count(string inputFile, string lineCountFile, string uniqueCountFile)
        {
            var watch = new Stopwatch();
            watch.Start();
            var dict = new Dictionary<string, long>(StringComparer.OrdinalIgnoreCase);

            using (var reader = new StreamReader(new FileStream(inputFile, FileMode.Open)))
            using (var lineCountWriter = new StreamWriter(new FileStream(lineCountFile, FileMode.Create)))
            {
                // read line
                string line;
                var lineNumber = 0;
                while ((line = reader.ReadLine()) != null)
                {
                    lineNumber++;
                    var words = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                    lineCountWriter.WriteLine($"{lineNumber} {words.Length}");

                    foreach (var word in words)
                    {
                        if (dict.ContainsKey(word))
                        {
                            dict[word]++;
                        }
                        else
                        {
                            dict.Add(word, 1);
                        }
                    }
                }
            }

            using (var uniqueCountWriter = new StreamWriter(new FileStream(uniqueCountFile, FileMode.Create)))
            {
                foreach (var pair in dict)
                {
                    uniqueCountWriter.WriteLine($"{pair.Key} {pair.Value}");
                }
            }

            watch.Stop();
            Console.WriteLine($"Total execution time in(ms): {watch.ElapsedMilliseconds}");
        }


        /// <summary>
        /// Question: Your program should scale with more CPUs, i.e., your program should run faster as more CPUs are available.
        /// As we need to stream the file before calculating the unique word count, parallelize the wordcount logic will not improve file read time
        /// Also, the word count calculation is happening in memory, this will be a fast operation and will not imprve the overall running time as the context switching
        /// overhad will be more the actually dictionary lookup
        /// </summary>
        public static async Task CountAsync(string inputFile, string lineCountFile, string uniqueCountFile)
        {
            var watch = new Stopwatch();
            watch.Start();
            var dict = new ConcurrentDictionary<string, long>(StringComparer.OrdinalIgnoreCase);

            using (var reader = new StreamReader(new FileStream(inputFile, FileMode.Open)))
            using (var lineCountWriter = new StreamWriter(new FileStream(lineCountFile, FileMode.Create)))
            {
                // read line
                string line;
                var lineNumber = 0;
                while ((line = await reader.ReadLineAsync()) != null)
                {
                    lineNumber++;
                    var words = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                    await lineCountWriter.WriteLineAsync($"{lineNumber} {words.Length}");

                    foreach (var word in words)
                    {
                        dict.AddOrUpdate(word, 1, (key, value) => value + 1);
                    }
                }
            }

            using (var uniqueCountWriter = new StreamWriter(new FileStream(uniqueCountFile, FileMode.Create)))
            {
                foreach (var pair in dict)
                {
                    await uniqueCountWriter.WriteLineAsync($"{pair.Key} {pair.Value}");
                }
            }

            watch.Stop();
            Console.WriteLine($"Total execution time in(ms): {watch.ElapsedMilliseconds}");
        }
    }
}
