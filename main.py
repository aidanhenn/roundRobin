# Aidan Hennessy
import random

# list to store averages
avgs = [0 for _ in range(4)]
def randArrival():
    interArrival = [0]
    for num in range(100):
        interArrival.append(random.randint(5, 10))
    avgs[0] = sum(interArrival)
    #print(f"The inter-arrival times are: {interArrival}")

    counter = 0  # Initialize counter to 0
    arrivalTimes = []
    num = 1
    while num < len(interArrival):
        arrivalTimes.append(counter)
        counter += interArrival[num]
        num += 1
    print(f"The arrival times are: {arrivalTimes}")
    return arrivalTimes
def randService():
    serviceTimes = []
    for num in range(100):
        serviceTimes.append(random.randint(4, 8))
    print(f"The service times are: {serviceTimes}")
    avgs[1] += sum(serviceTimes)

    return serviceTimes


def round_robin_scheduling(time_quantum, arrival_times, burst_times):
    # find the number of processes using the number of arrival times
    num_processes = len(arrival_times)

    # create a list of lists to store outputs
    processes = [[pid + 1, arrival_times[pid], burst_times[pid], burst_times[pid]] for pid in range(num_processes)]
    current_time = 0 # set current time
    idx = 0 # set index to iterate through processes
    progress = [0 for _ in range(num_processes)] # create a list to store progress, set all vals to 0
    startT = [0 for _ in range(num_processes)] # create a list to store start times, set all vals to 0
    readyQueue = []  # create a list to store start times, set all vals to 0

    while any(process[2] > 0 for process in processes): # While any process has remaining time
        if processes[idx][2] > 0 and processes[idx][1] <= current_time: # If the next processes has been reached
            execution_time = min(time_quantum, processes[idx][2]) # Execute time quantum or the remaining time if less
            progress[idx] = progress[idx] + execution_time # Track progress for debugging
            current_time += execution_time  # Add the execution time to the current time
            execute_process(processes, idx, execution_time, current_time, progress[idx], processes[idx][0], processes[idx][1], processes[idx][3], startT, time_quantum)
            if idx not in readyQueue: # if the current process is not already in the ready queue add it
                readyQueue.append(idx)
            if processes[readyQueue[0]][2] == 0: # if the next process to run in the ready queue is 0, remove it
                readyQueue.pop(0)
            if processes[(idx + 1) % num_processes][1] <= current_time:
                idx = (idx + 1) % num_processes

            current_time += context_switch
        elif len(readyQueue) != 0 and processes[readyQueue[0]][2] > 0: # If the next process is not ready to run check ready queue
            execution_time = min(time_quantum, processes[readyQueue[0]][2])
            progress[readyQueue[0]] = progress[readyQueue[0]] + execution_time
            current_time += execution_time
            execute_process(processes, readyQueue[0], execution_time, current_time, progress[readyQueue[0]], processes[readyQueue[0]][0], processes[readyQueue[0]][1], processes[readyQueue[0]][3], startT, time_quantum)
            if processes[readyQueue[0]][2] == 0: # if the next process to run has no remaining time, remove it
                readyQueue.pop(0)
            current_time += context_switch

            if processes[(idx + 1) % num_processes][1] <= current_time:
                idx = (idx + 1) % num_processes
        else: # if the next process is not ready and the ready queue is empty, wait 1 second
            current_time += 1  # If no processes in ready queue, time still advances
        if processes[(idx + 1) % num_processes][1] <= current_time:
            idx = (idx + 1) % num_processes

            current_time += context_switch


# function to execute process
print(f"PID \t Arrival Time \t Service Time \t Start Time \t Initial Wait \t End Time \t Turnaround Time")


def execute_process(processes, idx, execution_time, current_time, progress, pid, arrivalT, serviceT, startT, Quantum):
    #calculate remaining time by taking the max of 0 or the remaining time
    remaining_time = max(0, processes[idx][2] - execution_time)
    #print(f"Time: {current_time}... Executing process {processes[idx][0]} for {execution_time} units of time, {progress}/{processes[idx][3]}")
    processes[idx][2] = remaining_time
    # Calculate the wait time for the current progress
    # Accumulate the wait time for the process
    if remaining_time == serviceT - Quantum:
        startT[idx] = current_time - Quantum
        # If process completes output info
    if remaining_time == 0:
        turnAroundTime = current_time-startT[pid-1]
        avgs[2]+=turnAroundTime
        avgs[3]+=turnAroundTime - serviceT
        print(f"PID: {pid} arrival time: {arrivalT} service time: {serviceT} start time: {startT[pid-1]} initial wait: {startT[pid-1]-arrivalT} end time: {current_time} turn around: {turnAroundTime} total wait time: {turnAroundTime - serviceT}")

print (f"AVERAGES: {avgs}")
# Example usage
if __name__ == "__main__":
    time_quantum = 2
    context_switch = 0
    arrival_times = randArrival()
    burst_times = randService()
    round_robin_scheduling(time_quantum, arrival_times, burst_times)
    print(f"\navg interarrival: {avgs[0]/100} \navg service time: {avgs[1] / 100} \navg turnaround time: {avgs[2] / 100} \navg total wait time: {avgs[3] / 100}")