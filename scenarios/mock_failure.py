MOCK_OOM_LOGS = """
[kernel] [28491.1023] oom-killer: gfp_mask=0x1100cca(GFP_HIGHUSER_MOVABLE), order=0
[kernel] [28491.1024] Memory cgroup out of memory: Killed process 4102 (leak_simulator) total-vm:409600kB, anon-rss:204800kB
[systemd] [28491.1090] worker.service: Main process exited, code=killed, status=9/KILL
[systemd] [28491.1091] worker.service: Failed with result 'oom-kill'.
[systemd] [28491.1100] worker.service: Scheduled restart job, restart counter is at 12.
"""
