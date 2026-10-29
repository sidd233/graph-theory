import subprocess
from lift import lift
from lift2 import kp33
def run(N,arcs):
    s=f"{N} {len(arcs)}\n"+"\n".join(f"{u} {v}" for u,v in arcs)
    return subprocess.run(["./kpc"],input=s,capture_output=True,text=True).stdout.strip()
for i,b in enumerate(kp33()):
    print(f"C3xC9 lift #{i}:",run(27,lift(b,3,3,9)),flush=True)
