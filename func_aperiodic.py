import enum
from re import S
from tkinter import NONE
import numpy as np
import itertools
from datetime import datetime
from matplotlib import pyplot as plt 
import matplotlib.colors as mcolors
import matplotlib.patches as mpatch

# linked list
class Node:
   def __init__(self, task_id=None, cpu_util=None):
      self.task_id = task_id
      self.cpu_util = cpu_util
      self.next = None


class LinkedList:
   def __init__(self):
      self.head = None


# read details about each task
def read_task(task_path):

    # aperiodic jobs 
    if task_path == "OnlinejobsOf100AP.txt":

        task_detail = []

        # read file 
        with open(task_path) as f:
            tasks = f.readlines()
        # declare local variable
        new_n = 0
        lock_append = False
        # turn str digit into int lists
        for t in tasks:
            for inf in t:
                if inf.isdigit() == True:
                    new_n *= 10
                    new_n += int(inf)  
                    lock_append = False
                else:
                    if inf is not None and (lock_append == False):
                        # append complete imformation in task_detail
                        task_detail.append(new_n)
                        lock_append = True
                        new_n = 0
        task_detail.append(new_n)
        # split the list to ideal format
        aprd_task = np.array_split(task_detail, len(tasks))
        
        return aprd_task
    # sporatic jobs 
    elif task_path == "OnlinejobsOf100SP.txt":

        tasks_detail = []

        # read file 
        with open(task_path) as f:
            tasks = f.readlines()
        # declare local variable
        new_n = 0
        lock_append = False
        # turn str digit into int lists
        for t in tasks:
            for inf in t:
                if inf.isdigit() == True:
                    new_n *= 10
                    new_n += int(inf)  
                    lock_append = False
                else:
                    if inf is not None and (lock_append == False):
                        # append complete imformation in tasks_detail
                        tasks_detail.append(new_n)
                        lock_append = True
                        new_n = 0
        tasks_detail.append(new_n)
        # split the list to ideal format
        spor_task = np.array_split(tasks_detail, len(tasks))
        
        return spor_task

    # periodic jobs
    elif task_path == "OnlinejobsOfHRT.txt":

        num_cal = []
        tasks = []
        jobs = []
        read_line = 0
        # read file 
        with open(task_path) as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines):
            # the number of line now 
            read_line += 1
            # init variable
            task_num = 0
            # declare local variable
            new_n = 0
            lock_append = False

            # turn str digit into int lists
            for t in line:
                for inf in t:
                    # choose the line including jobs
                    if (read_line % 4 == 1 or read_line % 4 == 2):
                        if inf.isdigit() == True:
                            new_n *= 10
                            new_n += int(inf) 
                            lock_append = False
                        else:
                            if inf is not None and (lock_append == False):
                                # append complete imformation in task_detail
                                num_cal.append(new_n)
                                lock_append = True
                                new_n = 0

            if (read_line % 4) == 1:
                tasks.append(num_cal)
                num_cal = []
            elif (read_line % 4) == 2:
                jobs.append(num_cal)
                num_cal = []
                
        return tasks, jobs

    else:
        print("File Name Error !")
        return 0

def  schedule(tasks_list, jobs_list, aprd_job_list,spor_job_list):
    remain=[]
    deadline=[]
    release_time=[]
    aprd_queue=[]
    finish_tasks=[]
    count=0
    temp=10001
    point=101
    check_one=0
    check_two=0
    aprd_remain=0
    assume=2
    processors=assume
    for i in range(len(tasks_list)):
        release_time.append(tasks_list[i][1])
        remain.append(tasks_list[i][4])
        deadline.append(tasks_list[i][1]+tasks_list[i][2]) #deadline=release_time+period
    while(count<10001):
        for i in range(len(aprd_job_list)):
            if count==aprd_job_list[i][1]:
                if aprd_queue.count(aprd_job_list[i][0])==0:
                    aprd_queue.append(aprd_job_list[i][0])
                    aprd_remain=aprd_remain+aprd_job_list[i][2]
        for i in range(len(tasks_list)):
            if count>=release_time[i] and deadline[i]<temp and remain[i]>0 and count+remain[i]/processors<=deadline[i]:
                temp=deadline[i]
                point=i
        if point!=101: # have found 
             remain[point]= remain[point]-1
             check_one=check_one+1
             if remain[point]==0:
                if finish_tasks.count(tasks_list[point][0])==0:
                    finish_tasks.append(tasks_list[point][0])
                check_two=check_two+tasks_list[point][4]
                remain[point]=tasks_list[point][4] 
                release_time[point]=release_time[point]+tasks_list[point][2]
                deadline[point]=release_time[point]+tasks_list[point][2]
        else: # not found , schedule aperiodic_job
            if  aprd_remain>0:
                aprd_remain=aprd_remain-1
        point=101
        temp=10001
        if processors==1:
            count=count+1
            processors=assume
        else:
            processors-=1
    if check_two!=check_one or len(finish_tasks)!=len(tasks_list) or len(aprd_queue) != len(aprd_job_list) or  aprd_remain !=0:
        assume=assume+1
        print("程式執行中")
    else:
        print("number of minimum required processors is: 2")  
   
    while check_two!=check_one or len(finish_tasks)!=len(tasks_list) or len(aprd_queue) != len(aprd_job_list) or  aprd_remain !=0:
        temp=10001 
        point=101
        check_one=0
        check_two=0
        processors=assume
        count=0
        aprd_remain=0
        for i in range(len(tasks_list)):
           del release_time[0]
           del deadline[0]
           del remain[0]
        for i in range(len(finish_tasks)):
             del finish_tasks[0]
        for i in range(len(aprd_queue)):
             del aprd_queue[0]
        for i in range(len(tasks_list)):
           release_time.append(tasks_list[i][1])
           remain.append(tasks_list[i][4])
           deadline.append(tasks_list[i][1]+tasks_list[i][2]) #deadline=release_time+period
        while(count<10001):
            for i in range(len(aprd_job_list)):
                if count==aprd_job_list[i][1]:
                    if aprd_queue.count(aprd_job_list[i][0])==0:
                        aprd_queue.append(aprd_job_list[i][0])
                        aprd_remain=aprd_remain+aprd_job_list[i][2]
            for i in range(len(tasks_list)):
                if count>=release_time[i] and deadline[i]<temp and remain[i]>0 and count+remain[i]/processors<=deadline[i]:
                    temp=deadline[i]
                    point=i
            if point!=101: # have found 
                 remain[point]= remain[point]-1
                 check_one=check_one+1
                 if remain[point]==0:
                     if finish_tasks.count(tasks_list[point][0])==0:
                         finish_tasks.append(tasks_list[point][0])
                     check_two=check_two+tasks_list[point][4]
                     remain[point]=tasks_list[point][4] 
                     release_time[point]=release_time[point]+tasks_list[point][2]
                     deadline[point]=release_time[point]+tasks_list[point][2]
            else: # not found , schedule aperiodic_job
                if  aprd_remain>0:
                    aprd_remain=aprd_remain-1
            point=101
            temp=10001
            if processors==1:
                count=count+1
                processors=assume
            else:
                processors-=1
        assume=assume+1
        print(processors,end=" ") 
        print("(這可能不是答案，程式執行中)")
    print("number of minimum required processors is:",end=" ")
    print(processors+1)
    print("計算中，請稍候") 
    temp=10001 
    point=101
    minimum=10001
    flag=101
    check_one=0
    check_two=0
    processors=assume ##
    count=0
    response_time=0
    spor_remain_list=[]
    spor_deadline_list=[]
    spor_queue=[]
    spor_remain=0
    loss=[]
    execute=[]
   
    for i in range(len(tasks_list)):
         del release_time[0]
         del deadline[0]
         del remain[0]
    for i in range(len(finish_tasks)):
        del finish_tasks[0]
    for i in range(len(spor_job_list)):
        spor_remain_list.append(spor_job_list[i][2])
        spor_deadline_list.append(spor_job_list[i][3])
    for i in range(len(tasks_list)):
        release_time.append(tasks_list[i][1])
        remain.append(tasks_list[i][4])
        deadline.append(tasks_list[i][1]+tasks_list[i][2]) #deadline=release_time+period
    while(count<10001):
         for i in range(len(spor_job_list)):
                if count==spor_job_list[i][1]:
                    if spor_queue.count(spor_job_list[i][0])==0:
                        spor_queue.append(spor_job_list[i][0])
                        spor_remain=spor_remain+spor_job_list[i][2]
         for i in range(len(tasks_list)):
                if count>=release_time[i] and deadline[i]<temp and remain[i]>0 and count+remain[i]/processors<=deadline[i]:
                    temp=deadline[i]
                    point=i
         if point!=101: # have found 
                 remain[point]= remain[point]-1
                 check_one=check_one+1
                 if remain[point]==0:
                     if finish_tasks.count(tasks_list[point][0])==0:
                         finish_tasks.append(tasks_list[point][0])
                     check_two=check_two+tasks_list[point][4]
                     remain[point]=tasks_list[point][4] 
                     release_time[point]=release_time[point]+tasks_list[point][2]
                     deadline[point]=release_time[point]+tasks_list[point][2]
         else: # not found , schedule sporadic_job
                if  spor_remain>0:
                    for i in range(len(spor_remain_list)):  
                        if spor_queue.count(spor_job_list[i][0])==1 and spor_remain_list[i]>0 and spor_deadline_list[i]< minimum and spor_deadline_list[i]>=count+spor_remain_list[i]/processors:
                            minimum=spor_remain_list[i]
                            flag=i
                    if flag!=101:
                        spor_remain_list[flag]-=1
                        spor_remain=spor_remain-1
                    minimum=10001
                    flag=101
                            
         point=101
         temp=10001
         if processors==1:
             count=count+1
             processors=assume##
         else:
            processors-=1
   # if check_two==check_one and len(finish_tasks)==len(tasks_list) and len(aprd_queue) == len(aprd_job_list) and  aprd_remain ==0:
        #print("yes")
    
    #print("CPU utilization of each processor") 
    #for i in range(assume-1):
       # print("processor ",i+1," utilization is: ",utilization[i]/100,"%")
    #print("average response time of aperiodic jobs is: ",response_time/100) #SRTF
    for i in range (len(spor_queue)):
        if spor_remain_list[spor_queue[i]-1]==0:
            execute.append(spor_queue[i])
        else:
            loss.append(spor_queue[i])
    temp=10001 
    point=101
    minimum=10001
    flag=101
    minimum_a=10001
    flag_a=101 
    check_one=0
    check_two=0
    processors=assume##
    count=0
    aprd_remain=0
    spor_remain=0
    response_time=0
    aprd_remain_list=[]
    mark=[]
    utilization=[]
    spor_remain=0
    for i in range(processors):
        utilization.append(0)
    for i in range(len(tasks_list)):
         del release_time[0]
         del deadline[0]
         del remain[0]
    for i in range(len(jobs_list)):
        mark.append(0)
    for i in range(len(finish_tasks)):
        del finish_tasks[0]
    for i in range(len(spor_queue)):
        del spor_queue[0]
        del spor_remain_list[0]
        del spor_deadline_list[0]
    for i in range(len(aprd_queue)):
        del aprd_queue[0]
    for i in range(len(aprd_job_list)):
        aprd_remain_list.append(aprd_job_list[i][2])
    for i in range(len(spor_job_list)):
        spor_remain_list.append(spor_job_list[i][2])
        spor_deadline_list.append(spor_job_list[i][3])
    for i in range(len(tasks_list)):
        release_time.append(tasks_list[i][1])
        remain.append(tasks_list[i][4])
        deadline.append(tasks_list[i][1]+tasks_list[i][2]) #deadline=release_time+period
    while(count<10001):
         for i in range(len(aprd_job_list)):
                if count==aprd_job_list[i][1]:
                    if aprd_queue.count(aprd_job_list[i][0])==0:
                        aprd_queue.append(aprd_job_list[i][0])
                        aprd_remain=aprd_remain+aprd_job_list[i][2]
         for i in range(len(spor_job_list)):
                if count==spor_job_list[i][1]:
                    if spor_queue.count(spor_job_list[i][0])==0:
                        spor_queue.append(spor_job_list[i][0])
                        spor_remain=spor_remain+spor_job_list[i][2]
         for i in range(len(tasks_list)):
                if count>=release_time[i] and deadline[i]<temp and remain[i]>0 and count+remain[i]/processors<=deadline[i]:
                    temp=deadline[i]
                    point=i
         if point!=101: # have found 
                 remain[point]= remain[point]-1
                 if jobs_list[point][mark[point]]>0:
                     jobs_list[point][mark[point]]-=1
                     utilization[processors-1]+=1
                 check_one=check_one+1
                 if remain[point]==0:
                     mark[point]+=1
                     if finish_tasks.count(tasks_list[point][0])==0:
                         finish_tasks.append(tasks_list[point][0])
                     check_two=check_two+tasks_list[point][4]
                     remain[point]=tasks_list[point][4] 
                     release_time[point]=release_time[point]+tasks_list[point][2]
                     deadline[point]=release_time[point]+tasks_list[point][2]
         else: # not found , schedule sporadic_job and aperiodic_job
                if  spor_remain>0:
                    for i in range(len(spor_remain_list)):  
                        if spor_queue.count(spor_job_list[i][0])==1 and spor_remain_list[i]>0 and spor_deadline_list[i]< minimum and spor_deadline_list[i]>=count+spor_remain_list[i]/processors:
                            minimum=spor_remain_list[i]
                            flag=i
                    if flag!=101:
                        if loss.count(spor_job_list[i][0])==0 :#ok
                            spor_remain_list[flag]-=1
                            spor_remain=spor_remain-1
                            utilization[processors-1]+=1
                        else : # not found , schedule aperiodic_job
                            if  aprd_remain>0:
                                aprd_remain=aprd_remain-1
                                utilization[processors-1]+=1
                                for i in range(len(aprd_remain_list)):  # SRTF
                                    if aprd_queue.count(aprd_job_list[i][0])==1 and aprd_remain_list[i]>0 and aprd_remain_list[i]< minimum_a:
                                        minimum_a=aprd_remain_list[i]
                                        flag_a=i
                                aprd_remain_list[flag_a]-=1
                                if aprd_remain_list[flag_a]==0:
                                    response_time = response_time + count- aprd_job_list[flag_a][1]
                    else : # not found , schedule aperiodic_job
                         if  aprd_remain>0:
                                aprd_remain=aprd_remain-1
                                utilization[processors-1]+=1
                                for i in range(len(aprd_remain_list)):  # SRTF
                                    if aprd_queue.count(aprd_job_list[i][0])==1 and aprd_remain_list[i]>0 and aprd_remain_list[i]< minimum_a:
                                        minimum_a=aprd_remain_list[i]
                                        flag_a=i
                                aprd_remain_list[flag_a]-=1
                                if aprd_remain_list[flag_a]==0:
                                    response_time = response_time + count- aprd_job_list[flag_a][1]
                else : # not found , schedule aperiodic_job
                       
                        if  aprd_remain>0:
                            aprd_remain=aprd_remain-1
                            utilization[processors-1]+=1
                            for i in range(len(aprd_remain_list)):  # SRTF
                                 if aprd_queue.count(aprd_job_list[i][0])==1 and aprd_remain_list[i]>0 and aprd_remain_list[i]< minimum_a:
                                     minimum_a=aprd_remain_list[i]
                                     flag_a=i
                            aprd_remain_list[flag_a]-=1
                            if aprd_remain_list[flag_a]==0:
                                 response_time= response_time + count- aprd_job_list[flag_a][1]

                minimum=10001
                flag=101
                minimum_a=10001
                flag_a=101 
                            
         point=101
         temp=10001
         if processors==1:
             count=count+1
             processors=assume##
         else:
            processors-=1
    #if check_two==check_one and len(finish_tasks)==len(tasks_list) and len(aprd_queue) == len(aprd_job_list) and  aprd_remain ==0:
       # print("yes")
    
    print("CPU utilization of each processor") 
    for i in range(assume):##
       print("processor ",i+1," utilization is: ",utilization[i]/100,"%")
    print("average response time (waiting time) of aperiodic jobs is: ",response_time/100) #SRTF
    print("Loss of sporadic jobs is : ",len(loss), " %");
    print("ID list of the executable sporadic jobs are: ",len(execute)," tasks: ");
    execute.sort();
    for i in range(len(execute)):
        print("STask",execute[i],end="   ");
    return
    
    