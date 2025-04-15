import math
import random
import sys
import timeout_decorator
sys.path.append('/media/angelo/WorkData/git/VITAMIN-APP/VITAMIN/')
from vitamin_model_checker.model_checker_interface.explicit import ATL
from vitamin_model_checker.utils.generators import CGS_generator
import time

TIMEOUT = 2700  # seconds

# Wrap the functions that require a timeout with the decorator
@timeout_decorator.timeout(TIMEOUT)
def generate_model(agents, states):
    return CGS_generator.generate_random_CGS(agents, states, states, random.randint(1, states), 'tmp')

@timeout_decorator.timeout(TIMEOUT)
def model_checking(phi):
    return ATL.model_checking(phi, 'tmp')

def run_experiments(num_agents_min, num_agents_max, num_states_min, num_states_max, repetitions):
    with open('results.csv', 'w') as file:
        file.write('# States; # Agents; ATL time [sec]\n')    
    for state in range(num_states_min, num_states_max+1, 5):
        for agents in range(num_agents_min, num_agents_max+1):
            coalition = ','.join([str(i) for i in range(1, agents+1)])
            # target = f'a1{random.randint(1, int(math.sqrt(state)))}_{random.randint(1, int(math.sqrt(state)))}'
            target = 'a11_1'
            phi = f'(<{coalition}>F {target})'
            avg_time = 0
            with open('results.csv', 'a') as file:
                file.write(str(state) + ';' + str(agents) + ';')
            for _ in range(0, repetitions):
                try:
                    # Measure start time
                    start = time.time()
                    # Generate the model
                    generate_model(agents, int(math.sqrt(state)))
                    # Run model checking
                    res = model_checking(phi)
                    # Measure end time
                    end = time.time()
                    avg_time += end - start
                except timeout_decorator.TimeoutError:
                    print("Function took too long and was terminated.")
                    avg_time += TIMEOUT  # Consider the timeout duration as the time taken for this run
            avg_time = avg_time / repetitions
            with open('results.csv', 'a') as file:
                file.write(str(avg_time) + '\n')

if __name__ == "__main__":
    num_agents_min = max(int(sys.argv[1]), 1)
    num_agents_max = max(int(sys.argv[2]), 1)
    num_states_min = max(int(sys.argv[3]), 1)
    num_states_max = max(int(sys.argv[4]), 1)
    repetitions = max(int(sys.argv[5]), 1)
    run_experiments(num_agents_min, num_agents_max, num_states_min, num_states_max, repetitions)
