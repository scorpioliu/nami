#! /usr/bin/env python

# multiprocessTemplate.py
# Using multiprocess template

# Comes from http://jeetworks.org/node/81

# by scorpioliu
# 2012.02.11

import random
import multiprocessing, queue
import time

 
class Worker(multiprocessing.Process):
 
    def __init__(self, work_queue, result_queue):
 
        # base class initialization
        multiprocessing.Process.__init__(self)
 
        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False
 
    def run(self):
        while not self.kill_received:
 
            # get a task
            #job = self.work_queue.get_nowait()
            try:
                job = self.work_queue.get_nowait()
            except queue.Empty:
                break
 
            # the actual processing
            print("Starting " + str(job) + " ...")
            delay = random.randrange(1,3)
            time.sleep(delay)
 
            # store the result
            self.result_queue.put(delay)
 
if __name__ == "__main__":
 
    num_jobs = 20
    num_processes=8
 
    # run
    # load up work queue
    work_queue = multiprocessing.Queue()
    for job in range(num_jobs):
        work_queue.put(job)
 
    # create a queue to pass to workers to store the results
    result_queue = multiprocessing.Queue()
 
    # spawn workers
    for i in range(num_processes):
        worker = Worker(work_queue, result_queue)
        worker.start()
 
    # collect the results off the queue
    results = []
    for i in range(num_jobs):
        print(result_queue.get())