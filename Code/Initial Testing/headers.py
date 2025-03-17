import binascii

# Function: Analyze and Compare File Headers
def compare_file_headers(image_paths):
    headers = {}
    
    # Read headers of all images
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            headers[image_path] = f.read(64)  # Read the first 64 bytes

    # Display the headers in hex and ASCII
    print("File Header Comparison:\n")
    for image_path, header in headers.items():
        print(f"Image: {image_path}")
        print("Header (Hex):", binascii.hexlify(header))
        print("Header (ASCII):", header)
        print("-" * 60)

    # Compare headers byte by byte
    print("\nHeader Differences (Byte Comparison):")
    for i in range(64):
        byte_values = [headers[image_path][i] for image_path in image_paths]
        if len(set(byte_values)) > 1:  # If the byte differs between images
            byte_hex = [binascii.hexlify(bytes([b])) for b in byte_values]
            print(f"Byte {i+1:02d}: {' | '.join([x.decode() for x in byte_hex])}")

# Main Execution
if __name__ == "__main__":
    # Replace with paths to your images
    image_paths = ["Geminii.jpg", "Geminiii.jpg", "Geminiv.jpg", "DallE.jpg", "DallH.jpg"]
    
    print("Step 1: File Header Analysis and Comparison")
    compare_file_headers(image_paths)
