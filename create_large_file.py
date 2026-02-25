
content_to_repeat = "This is a test of the Cyclic Cypher Compressor. We are testing the full round-trip process to ensure that the unfold engine can perfectly reconstruct the data transmuted by the ccc-engine.\n"
# Repeat 46600 times for a ~10MB file.
# 226 chars * 46600 = 10,531,600 bytes
repetitions = 46600 
with open("large_file.txt", "w") as f:
    for _ in range(repetitions):
        f.write(content_to_repeat)
print("Created large_file.txt with ~10MB of data.")
