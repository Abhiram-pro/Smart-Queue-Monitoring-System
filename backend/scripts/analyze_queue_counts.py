import csv
import os
import sys

def analyze(csv_path):
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return 1

    times = []
    queues = []

    worker_counts = []
    
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        # header: frame, time_sec, queue_1, queue_2, ..., worker_count
        # Check if worker_count column exists
        has_workers = 'worker_count' in header
        if has_workers:
            q_count = len(header) - 3  # frame, time_sec, worker_count
        else:
            q_count = len(header) - 2  # frame, time_sec only
        
        for row in reader:
            if not row:
                continue
            frame = int(row[0])
            time_sec = float(row[1])
            counts = [int(x) for x in row[2:2+q_count]]
            times.append(time_sec)
            queues.append(counts)
            
            if has_workers:
                worker_counts.append(int(row[-1]))  # last column is worker_count

    if not times:
        print("No data in CSV")
        return 1

    total_time = times[-1] - times[0] if len(times) > 1 else times[-1]
    if total_time <= 0:
        total_time = max(times[-1], 1.0)

    # transpose queues to per-queue lists
    per_queue = list(map(list, zip(*queues)))

    results = []
    for i, q in enumerate(per_queue):
        # average number in queue (time-average approximated by frame average)
        L = sum(q) / len(q)

        # estimate departures by summing positive drops between frames
        departures = 0
        for prev, curr in zip(q[:-1], q[1:]):
            if curr < prev:
                departures += (prev - curr)

        throughput = departures / total_time if total_time > 0 else 0

        if throughput > 0:
            W = L / throughput
        else:
            W = float('inf')

        results.append({
            'queue': i+1,
            'avg_occupancy': L,
            'departures': departures,
            'throughput_per_sec': throughput,
            'estimated_avg_wait_sec': W
        })

    # print a short summary
    print(f"Analyzed: {csv_path}")
    print(f"Total time (s): {total_time:.2f}, frames: {len(queues)}")
    
    if worker_counts:
        avg_workers = sum(worker_counts) / len(worker_counts)
        print(f"\nWorker Statistics:")
        print(f"  Average workers detected: {avg_workers:.2f}")
        print(f"  Min workers: {min(worker_counts)}, Max workers: {max(worker_counts)}")
    
    print(f"\nCustomer Queue Statistics:")
    for r in results:
        w = r['estimated_avg_wait_sec']
        w_str = f"{w:.2f}s" if w != float('inf') else "inf"
        print(f"Queue {r['queue']}: avg occupancy={r['avg_occupancy']:.2f}, departures={r['departures']}, throughput={r['throughput_per_sec']:.3f}/s, est avg wait={w_str}")

    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_queue_counts.py /path/to/queue_counts.csv")
        sys.exit(1)
    csv_path = sys.argv[1]
    sys.exit(analyze(csv_path))
