import core.video_cypher_engine as eng

e = eng.VideoCypherStage1()
data = b'\xa7r\x22\xc3\x1c\x1c\x29\xb3\xec\xdf'
enc = e.encode_chunk(data)
dec = e.decode_chunk(enc)

print("Engine Restored.")
print(f"Decoded Matches Original: {data == dec}")
