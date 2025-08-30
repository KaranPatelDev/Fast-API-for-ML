import time
from timeit import default_timer as timer

def run_task(name, seconds):
    print(f"{name} Starting task: {timer()}")
    time.sleep(seconds)
    print(f"{name} Completed task: {timer()}")


start = timer()
run_task("Task 1", 2)
run_task("Task 2", 3)
run_task("Task 3", 1)
print(f"All tasks completed in: {timer() - start:.2f} seconds")