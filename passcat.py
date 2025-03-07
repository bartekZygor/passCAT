import hashlib
import sys
import threading
from queue import Queue

def load_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        return None

def verify_ntlm(word, hash_value):
    return hashlib.new('md4', word.encode('utf-16le')).hexdigest().upper() == hash_value

def crack_hashes(hash_queue, wordlist, result_file):
    while not hash_queue.empty():
        hash_value = hash_queue.get()
        found = False
        for word in wordlist:
            if verify_ntlm(word, hash_value):
                print(f"Found password: '{word}' for hash: {hash_value}")
                result_file.write(f"Hash: {hash_value} → Password: {word}\n")
                found = True
                break
        if not found:
            print(f"No password found for hash: {hash_value}")
            result_file.write(f"Hash: {hash_value} → No password found\n")
        hash_queue.task_done()

def main():
    print("Password RECAP v2.0")
    print("Made by Mewtwo\n")
    print("Enjoy!\n")

    # Get file paths
    hash_file_path = input("Enter hash file path: ")
    wordlist_file_path = input("Enter wordlist file path: ")

    hashes = load_file(hash_file_path)
    wordlist = load_file(wordlist_file_path)

    if not hashes or not wordlist:
        print("Error: Could not read files. Script aborted.")
        sys.exit(1)

    hash_queue = Queue()
    for hash_value in hashes:
        hash_queue.put(hash_value)

    with open("result.txt", "w", encoding="utf-8") as result_file:
        print(f"\nChecking hashes from '{hash_file_path}' against wordlist '{wordlist_file_path}'...")

        # Create and start threads
        num_threads = 10
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=crack_hashes, args=(hash_queue, wordlist, result_file))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    print("\nResults saved in 'result.txt'")

if __name__ == "__main__":
    main()
