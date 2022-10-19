import cirq
import qsimcirq
import numpy as np
import sympy as sp
import pandas
import random
import time

class random_initialize(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def _unitary_(self):
        theta1=random.uniform(0,2*np.pi)
        theta2=random.uniform(0,2*np.pi)
        theta3=random.uniform(0,2*np.pi)
        a=np.cos(theta1)
        b=np.sin(theta1)*np.cos(theta2)
        c=np.sin(theta1)*np.sin(theta2)*np.cos(theta3)
        d=np.sin(theta1)*np.sin(theta2)*np.sin(theta3)
        return np.array([[a+b*1j, c-d*1j], [c+d*1j, -a+b*1j]])

    def __str__(self):
        return 'random'

z12 = cirq.NamedQubit("z12")
z14 = cirq.NamedQubit("z14")
z32 = cirq.NamedQubit("z32")
z34 = cirq.NamedQubit("z34")
z52 = cirq.NamedQubit("z52")
z54 = cirq.NamedQubit("z54")

x21 = cirq.NamedQubit("x21")
x23 = cirq.NamedQubit("x23")
x25 = cirq.NamedQubit("x25")
x41 = cirq.NamedQubit("x41")
x43 = cirq.NamedQubit("x43")
x45 = cirq.NamedQubit("x45")

q11 = cirq.NamedQubit("q11")
q13 = cirq.NamedQubit("q13")
q15 = cirq.NamedQubit("q15")

q22 = cirq.NamedQubit("q22")
q24 = cirq.NamedQubit("q24")

q31 = cirq.NamedQubit("q31")
q33 = cirq.NamedQubit("q33")
q35 = cirq.NamedQubit("q35")

q42 = cirq.NamedQubit("q42")
q44 = cirq.NamedQubit("q44")

q51 = cirq.NamedQubit("q51")
q53 = cirq.NamedQubit("q53")
q55 = cirq.NamedQubit("q55")
ran=random_initialize()

circuit=cirq.Circuit([
        
        cirq.H(cirq.NamedQubit('x21')),cirq.H(cirq.NamedQubit('x23')),cirq.H(cirq.NamedQubit('x25')),
        cirq.H(cirq.NamedQubit('x41')),cirq.H(cirq.NamedQubit('x43')),cirq.H(cirq.NamedQubit('x45')),
        
        cirq.CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q11')),
        cirq.CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q31')),
        cirq.CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q22')),
        
        cirq.CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q13')),
        cirq.CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q33')),
        cirq.CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q22')),
        cirq.CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q24')),
        
        cirq.CNOT(cirq.NamedQubit('x25'), cirq.NamedQubit('q15')),
        cirq.CNOT(cirq.NamedQubit('x25'), cirq.NamedQubit('q35')),
        cirq.CNOT(cirq.NamedQubit('x25'), cirq.NamedQubit('q24')),
        
        cirq.CNOT(cirq.NamedQubit('x41'), cirq.NamedQubit('q31')),
        cirq.CNOT(cirq.NamedQubit('x41'), cirq.NamedQubit('q51')),
        cirq.CNOT(cirq.NamedQubit('x41'), cirq.NamedQubit('q42')),
        
        cirq.CNOT(cirq.NamedQubit('x43'), cirq.NamedQubit('q33')),
        cirq.CNOT(cirq.NamedQubit('x43'), cirq.NamedQubit('q53')),
        cirq.CNOT(cirq.NamedQubit('x43'), cirq.NamedQubit('q42')),
        cirq.CNOT(cirq.NamedQubit('x43'), cirq.NamedQubit('q44')),
        
        cirq.CNOT(cirq.NamedQubit('x45'), cirq.NamedQubit('q35')),
        cirq.CNOT(cirq.NamedQubit('x45'), cirq.NamedQubit('q55')),
        cirq.CNOT(cirq.NamedQubit('x45'), cirq.NamedQubit('q44')),
        
        
        cirq.CNOT(cirq.NamedQubit('q11'), cirq.NamedQubit('z12')),
        cirq.CNOT(cirq.NamedQubit('q13'), cirq.NamedQubit('z12')),
        cirq.CNOT(cirq.NamedQubit('q22'), cirq.NamedQubit('z12')),
        
        cirq.CNOT(cirq.NamedQubit('q13'), cirq.NamedQubit('z14')),
        cirq.CNOT(cirq.NamedQubit('q15'), cirq.NamedQubit('z14')),
        cirq.CNOT(cirq.NamedQubit('q24'), cirq.NamedQubit('z14')),
        
        cirq.CNOT(cirq.NamedQubit('q31'), cirq.NamedQubit('z32')),
        cirq.CNOT(cirq.NamedQubit('q33'), cirq.NamedQubit('z32')),
        cirq.CNOT(cirq.NamedQubit('q22'), cirq.NamedQubit('z32')),
        cirq.CNOT(cirq.NamedQubit('q42'), cirq.NamedQubit('z32')),
        
        cirq.CNOT(cirq.NamedQubit('q33'), cirq.NamedQubit('z34')),
        cirq.CNOT(cirq.NamedQubit('q35'), cirq.NamedQubit('z34')),
        cirq.CNOT(cirq.NamedQubit('q24'), cirq.NamedQubit('z34')),
        cirq.CNOT(cirq.NamedQubit('q44'), cirq.NamedQubit('z34')),
        
        cirq.CNOT(cirq.NamedQubit('q51'), cirq.NamedQubit('z52')),
        cirq.CNOT(cirq.NamedQubit('q53'), cirq.NamedQubit('z52')),
        cirq.CNOT(cirq.NamedQubit('q42'), cirq.NamedQubit('z52')),
        
        cirq.CNOT(cirq.NamedQubit('q53'), cirq.NamedQubit('z54')),
        cirq.CNOT(cirq.NamedQubit('q55'), cirq.NamedQubit('z54')),
        cirq.CNOT(cirq.NamedQubit('q44'), cirq.NamedQubit('z54')),
        

        cirq.H(cirq.NamedQubit('x21')),cirq.H(cirq.NamedQubit('x23')),cirq.H(cirq.NamedQubit('x25')),
        cirq.H(cirq.NamedQubit('x41')),cirq.H(cirq.NamedQubit('x43')),cirq.H(cirq.NamedQubit('x45')),

        cirq.measure(cirq.NamedQubit('x21')),cirq.measure(cirq.NamedQubit('x23')),
        cirq.measure(cirq.NamedQubit('x25')),cirq.measure(cirq.NamedQubit('x41')),
        cirq.measure(cirq.NamedQubit('x43')),cirq.measure(cirq.NamedQubit('x45')),
        cirq.measure(cirq.NamedQubit('z12')),cirq.measure(cirq.NamedQubit('z14')),
        cirq.measure(cirq.NamedQubit('z32')),cirq.measure(cirq.NamedQubit('z34')),
        cirq.measure(cirq.NamedQubit('z52')),cirq.measure(cirq.NamedQubit('z54')),

    #cirq.Moment(
    #    cirq.depolarize(0.2)(cirq.NamedQubit('x')),
    #),
    
])
qsim_start = time.time()
#print(circuit)
simulator = qsimcirq.QSimSimulator()

result = simulator.simulate(circuit)
print("\nDirac notation:")
print(result.dirac_notation())
    
qsim_elapsed = time.time() - qsim_start
print(f'qsim runtime: {qsim_elapsed} seconds.')    