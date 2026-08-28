import re
with open('__HOME_RANDALL_PLACEHOLDER__/cyclic-cypher-compressor/archive_legacy_builds.py', 'r') as f:
    content = f.read()

# I will update the archive_legacy_builds.py script to reflect the new protocol as well just in case they run it again.
new_content = content.replace("with tarfile.open(tarball, \"w\") as tar:", "with tarfile.open(tarball, \"w\") as tar:") 
