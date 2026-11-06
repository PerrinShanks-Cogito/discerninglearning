import subprocess, sys
r=subprocess.run([sys.executable,"scripts/landmark_numbers/update_performance.py"],capture_output=True,text=True)
print(r.stdout); print(r.stderr)
print("JSON"); print(open("_data/landmark_performance.json").read())
# run 1793976391
