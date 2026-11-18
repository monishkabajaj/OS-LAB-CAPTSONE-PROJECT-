import unittest
from modules.cpu_scheduling import fcfs, sjf_non_preemptive, round_robin
from modules.memory_management import allocate
from modules.deadlock import bankers_safety
from modules.disk_scheduling import disk_schedule

class TestOSSim(unittest.TestCase):
    def setUp(self):
        self.processes = [
            {"pid":"P1","arrival":0,"burst":5},
            {"pid":"P2","arrival":1,"burst":3},
        ]

    def test_fcfs_waiting(self):
        metrics, _ = fcfs(self.processes)
        self.assertEqual({x["pid"]:x["waiting"] for x in metrics}, {"P1":0,"P2":4})

    def test_sjf_returns_all_processes(self):
        metrics, _ = sjf_non_preemptive(self.processes)
        self.assertEqual(len(metrics), 2)

    def test_round_robin_completion(self):
        metrics, _ = round_robin(self.processes, 2)
        self.assertTrue(all(x["completion"] > 0 for x in metrics))

    def test_invalid_burst_rejected(self):
        with self.assertRaises(ValueError):
            fcfs([{"pid":"P1","arrival":0,"burst":0}])

    def test_memory_first_fit(self):
        rows, free = allocate([100, 300], [80, 150], "First Fit")
        self.assertEqual(rows[0][2], "B1")
        self.assertEqual(rows[1][2], "B2")

    def test_memory_unallocated(self):
        rows, _ = allocate([50], [80], "First Fit")
        self.assertEqual(rows[0][2], "Not allocated")

    def test_bankers_safe_state(self):
        safe, seq, _ = bankers_safety([3,3,2],
            [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]],
            [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]])
        self.assertTrue(safe)
        self.assertEqual(len(seq), 5)

    def test_disk_sstf(self):
        order, movement = disk_schedule([10,20,90], 15, "SSTF", 100)
        self.assertEqual(order[0], 10)
        self.assertEqual(movement, 85)

    def test_disk_boundary_rejected(self):
        with self.assertRaises(ValueError):
            disk_schedule([200], 50, "FCFS", 200)

if __name__ == "__main__":
    unittest.main(verbosity=2)
