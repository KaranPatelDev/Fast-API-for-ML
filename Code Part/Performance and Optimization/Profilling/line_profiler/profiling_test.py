from app import process_data
# from line_profiler import profile

@profile
def run():
    process_data(10000)


if __name__ == '__main__':
    run()


'''
To run the profiler, use the command:
kernprof -l -v profiling_test.py
where:
    -l: Tells kernprof to use line-by-line profiling.
    -v: Displays the results after execution.
This will execute the run function and provide detailed line-by-line profiling information for the process_data function.
'''