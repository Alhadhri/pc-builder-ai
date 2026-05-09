import pandas as pd
import heapq
from collections import deque

def load_data():
    files = {
        'CPU': 'CPUs.csv',
        'MB': 'MBs.csv',
        'RAM': 'RAMs.csv',
        'Storage': 'Storage.csv',
        'GPU': 'GPUs.csv',
        'PSU': 'PSUs.csv'
    }
    datasets = {}
    for key, file in files.items():
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        datasets[key] = df
    return datasets

def is_compatible(current_build, next_comp, category, budget):
    current_total = sum(item['price_usd'] for item in current_build.values())
    if current_total + next_comp['price_usd'] > budget:
        return False
    if category == 'MB':
        cpu = current_build.get('CPU')
        if cpu and str(next_comp['socket']).strip() != str(cpu['socket']).strip(): return False
    elif category == 'RAM':
        mb = current_build.get('MB')
        if mb:
            mb_type = mb.get('ram_type') or mb.get('type')
            ram_type = next_comp.get('ram_type') or next_comp.get('type')
            if str(ram_type).strip().upper() != str(mb_type).strip().upper(): return False
    return True

def matches_purpose(comp, category, purpose):
    if purpose == "Gaming":
        if category == "GPU" and comp['vram_gb'] < 8: return False
    return True

# تأكد من هذا الاسم تحديداً
def run_search(algo, budget, purpose, datasets):
    order = ['CPU', 'MB', 'RAM', 'Storage', 'GPU', 'PSU']
    visited = 0
    if algo == 'UCS':
        counter = 0
        pq = [(0, counter, {})]
        while pq:
            cost, _, build = heapq.heappop(pq)
            visited += 1
            if len(build) == 6: return build, cost, visited
            category = order[len(build)]
            for _, comp in datasets[category].iterrows():
                if is_compatible(build, comp, category, budget) and matches_purpose(comp, category, purpose):
                    new_build = build.copy()
                    new_build[category] = comp.to_dict()
                    counter += 1
                    heapq.heappush(pq, (cost + comp['price_usd'], counter, new_build))
    else:
        queue = deque([(0, {})])
        while queue:
            cost, build = queue.popleft() if algo == 'BFS' else queue.pop()
            visited += 1
            if len(build) == 6: return build, cost, visited
            category = order[len(build)]
            for _, comp in datasets[category].iterrows():
                if is_compatible(build, comp, category, budget) and matches_purpose(comp, category, purpose):
                    new_build = build.copy()
                    new_build[category] = comp.to_dict()
                    queue.append((cost + comp['price_usd'], new_build))
    return None, 0, visited