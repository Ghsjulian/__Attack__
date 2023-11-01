import threading
import time

# Function to process numbers
def process_number(number):
    global exit_flag  # Add this line
    if len(number) < 6:
        return
    print(number)
    if number == '123456':
        print("Number Found In Text File")
        exit_flag = True  # Set the flag to signal other threads to exit

# Open the file and read numbers
with open('number.txt', 'r') as file:
    numbers = [line.strip() for line in file]

# Number of threads to run simultaneously
thread_limit = 2# Adjust as needed

# Flag to signal threads to exit
exit_flag = False

# Function to create and run threads
def run_threads():
    global exit_flag
    threads = []
    
    while numbers:
        if exit_flag:
            break
        current_numbers = numbers[:thread_limit]
        numbers[:] = numbers[thread_limit:]
        
        for number in current_numbers:
            thread = threading.Thread(target=process_number, args=(number,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

# Start the threads
thread_handler = threading.Thread(target=run_threads)
thread_handler.start()

# Sleep to allow threads to run (you can set a timeout if needed)
time.sleep(1)

# Set the exit flag to signal threads to exit
exit_flag = True

# Wait for the thread_handler to finish
thread_handler.join()
