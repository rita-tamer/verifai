import subprocess

AI_TAGS = [
    "Credit", "JUMD Type", "JUMD Label", "Actions Action", 
    "Actions Software Agent", "Claim Generator", "Signature", 
    "Assertions Url", "C2PA", "Thumbnails", "Manifests"
]

def analyze_metadata(file_path):
    result = subprocess.run(['exiftool', file_path], capture_output=True, text=True)
    output = result.stdout.lower()
    matches = [tag for tag in AI_TAGS if tag.lower() in output]
    return matches
