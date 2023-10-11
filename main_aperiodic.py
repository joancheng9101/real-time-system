from tracemalloc import stop
from func_aperiodic import *
import time

def main():
    tasks_list, jobs_list = read_task("OnlinejobsOfHRT.txt")
    aprd_job_list = read_task("OnlinejobsOf100AP.txt")
    spor_job_list = read_task("OnlinejobsOf100SP.txt")
    schedule(tasks_list, jobs_list,aprd_job_list,spor_job_list)
if __name__ == '__main__':
    main()