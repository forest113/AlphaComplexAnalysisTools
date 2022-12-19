import subprocess

input_files = []
molecules = []
alpha_vals = []

num_molecules = int(input('Number of input files:'))
for i in range(0, num_molecules):
    f = input('Path to input file')
    input_files.append(f)
    molecules.append(f.split('/')[-1].split('.')[0])
    
num_alpha = int(input('Number of alpha values:')) 
for i in range(0, num_alpha):
    alpha_vals.append(int(input('Alpha value:')))
    
cpu_alg = input('path to cpu alg:')
gpu_alg = input('path to gpu alg:')


cpu_ops = []
for i in range(0, num_molecules):
    for j in range(0, num_alpha):
        cpu_ops.append(subprocess.run([cpu_alg, input_files[i], 'cpu_outputs/'+molecules[i]+'_alpha'+str(alpha_vals[j])+'.txt', '0', str(alpha_vals[j])], stdout=subprocess.PIPE))

for op in cpu_ops:
    print(op.stdout)
    
for i in range(0, num_molecules):
    for j in range(0, num_alpha):
        cpu_ops.append(subprocess.run([gpu_alg, input_files[i], 'cpu_outputs/'+molecules[i]+'_alpha'+str(alpha_vals[j])+'.txt', '0', str(alpha_vals[j]), '10000'], stdout=subprocess.PIPE))

for op in cpu_ops:
    print(op.stdout)
