# This source code was written by :
#    Name: Momanyi Biffon Manyura   ID: 202114080103    Degree: PhD
#    University: 电子科技大学 School: Computer Science and Engineering
#    Course: Operating Systems Structure and applications
#    Lecturer: Prof. Chao Song
#    Date: 2022/04/19


import psutil as ps
import sys, datetime
from prettytable import PrettyTable


# This function returns process operations
def process_operations():
    print("\n**************Manage processes**************\n")
    operations = ['1.Suspend', '2.Resume', '3.Terminate']
    for i in operations:
        print(i)
    process_operations.operation = int(input("Choose an operation:\n"))


# This function returns all processes currently running in the computer system
def processes():
    print("----Processes----")
    processes_table = PrettyTable(['PID', 'PNAME', 'STATUS'])
     
    for process in ps.pids():
 
        # While fetching the processes, some of the subprocesses may exit
        # Hence we need to put this code in try-except block
        try:
            p = ps.Process(process)
            processes_table.add_row([
                str(process),
                p.name(),
                p.status(),
                ])
             
        except Exception as e:
            pass
    print(processes_table)
    print("Total processes:",len(ps.pids())) # Displaying total number of processes

def get_process_id():
    pro_id = int(input("Enter process ID to view details:\n"))
    return pro_id


# This function prints details of a single process in a table
def single_process(p_id):
    
    # Initialization of a table using PrettyTables
    process_table = PrettyTable(['PID', 'PPID', 'PNAME', 'STATUS',
                                 'CPU', 'NUM THREADS', 'CREATED TIME',
                                 'CHILDREN'])
    
    # Using PrettyTables to display single process information
    ps_details = ps.Process(pid=p_id)
    process_table.add_row([
        p_id,
        ps_details.ppid(),
        ps_details.name(),
        ps_details.status(),
        str(ps_details.cpu_percent())+"%",
        ps_details.num_threads(),
        datetime.datetime.fromtimestamp(ps_details.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
        ps_details.children(),
    ])
         

    print(process_table)
        

# This function suspends processes if all conditions are met
def suspend_process(p_id):
    p_dtl = ps.Process(p_id)
    if p_dtl.status() != 'stopped':
        confirm_s = int(input("Do you want to suspend process {} \n1. Yes \t 2.No\n".format(p_id)))
        if confirm_s == 1:
            p_dtl.suspend()
            print("Process {} suspended!".format(p_id))
            resume_suspended_process = int(input("Resume process {}\n1. Yes\n2. No\n".format(p_id)))
            if resume_suspended_process == 1:
                resume_process(p_id)
            else:
                sys.exit("Program ended")
        else:
            print("Process {} not suspended".format(p_id))
            get_process_id()
    else:
        confirm_resume = int(input("Process {} is already {}, do you want to resume it? \n1. Yes\n2. No\n".format(p_id, p_dtl.status())))
        if confirm_resume == 1:
            resume_process(p_id)
        else:
            processes()
            get_process_id()


# This functions is used to resume processes if all conditions are met
def resume_process(p_id):
    p_dtl = ps.Process(pid=p_id)
    status = p_dtl.status()
    if status == 'stopped':
        confirm_r = int(input("Resume process {}? \n1. Yes \n2. No.\n".format(p_id)))
        if confirm_r == 1:
            p_dtl.resume()
            new_status = ps.Process(p_id).status()
            print("Process {} is now {}".format(p_id, new_status))
            suspend_running_process = int(input("Suspend process {}\n1. Yes\n2. No\n".format(p_id)))
            if suspend_running_process == 1:
                suspend_process(p_id)
            else:
                sys.exit("Program ended")
                
        else:
            print("Resume cancelled!, process {} is still {}".format(p_id, p_dtl.status()))
    else:
        print("Process {} is already {} \n".format(p_id, p_dtl.status()))
        suspend_this_process = int(input("Do you want to suspend process {}?\n1. Yes\n2. No\n".format(p_id)))
        if suspend_this_process == 1:
            suspend_process(p_id)
        else:
            sys.exit("Program ended!")


# This function terminates a particular process if all conditions are met
def terminate_process(p_id):
    p_dtl = ps.Process(p_id)
    confirm_t = int(input("Do you want to terminate process {}\n1. Yes\n2. No\n".format(p_id)))
    if confirm_t == 1:
        p_dtl.terminate()
        print("Process {} has been terminated!".format(p_id))
    else:
        print("Process terminate cancelled!")


# main function
if __name__ == "__main__":
    print("Running processes")
    processes()
    pro_id = get_process_id() # getting an ID to fetch single process details
    try:
        try:
            # This function displays single process details
            single_process(pro_id)
        
            # This function contains process management operations
            process_operations()
        
            # Calling functions to perform the three operations
            if process_operations.operation == 1:
                suspend_process(pro_id) # Suspend process function call
            elif process_operations.operation == 2:
                resume_process(pro_id) # Resume process function call
            elif process_operations.operation == 3:
                terminate_process(pro_id) # Terminate process function call
            else:
                print("Invalid operation!")
            
        except ps.NoSuchProcess:
            print("No process was found with id {}".format(pro_id))
            
    except ps.AccessDenied:
        print("You don't have permission to change process {}".format(pro_id))
        

