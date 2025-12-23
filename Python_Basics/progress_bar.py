from tqdm import tqdm
import time

def simulate_work(item):
    time.sleep(0.1)

for item in tqdm(range(90), desc='Processing items'):
    simulate_work(item)