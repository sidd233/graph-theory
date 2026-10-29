import sys, subprocess
from kp import torus, eulerian_orientations, build, kernel_perfect
from lift import lift
def run(N,arcs):
    s=f"{N} {len(arcs)}\n"+"\n".join(f"{u} {v}" for u,v in arcs)
    return subprocess.run(["./kpc"],input=s,capture_output=True,text=True).stdout.strip()
N3,E3=torus(3,3)
ors=eulerian_orientations(N3,E3)
kp33=[a for a in ors if kernel_perfect(N3,*build(N3,a))[0]]
print("sanity C3xC3 kp orientation ->",run(9,kp33[0]))
print("sanity C3xC3 non-kp orientation ->",run(9,[a for a in ors if a not in kp33][0]))
N5,E5=torus(3,5); print("sanity C3xC5 orientation ->",run(15,eulerian_orientations(N5,E5,limit=1)[0]))
for i,b in enumerate(kp33[:int(sys.argv[1])]):
    print(f"C3xC9 lift #{i} ->",run(27,lift(b,3,3,9)),flush=True)
