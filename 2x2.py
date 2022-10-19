import cirq
import qsimcirq
import numpy as np
import sympy as sp
import pandas
import random

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
    
class check(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 4

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
x = cirq.NamedQubit("x")
a = cirq.NamedQubit("a")
b = cirq.NamedQubit("b")
z = cirq.NamedQubit("z")
ran=random_initialize()

circuit=cirq.Circuit([
    cirq.Moment(
        ran(cirq.NamedQubit('a')),ran(cirq.NamedQubit('b')),
    ),
    cirq.Moment(
        cirq.H(cirq.NamedQubit('x')),
    ),
    cirq.Moment(
        cirq.CNOT(cirq.NamedQubit('x'), cirq.NamedQubit('a')),
    ),
    cirq.Moment(
        cirq.CNOT(cirq.NamedQubit('x'), cirq.NamedQubit('b')),
    ),
    cirq.Moment(
        cirq.CNOT(cirq.NamedQubit('a'), cirq.NamedQubit('z')),
    ),
    cirq.Moment(
        cirq.CNOT(cirq.NamedQubit('b'), cirq.NamedQubit('z')),
    ),
    cirq.Moment(
        cirq.H(cirq.NamedQubit('x')),
    ),
    cirq.Moment(
        cirq.measure(cirq.NamedQubit('x'),key='x1'),cirq.measure(cirq.NamedQubit('z'),key='z1'),
    ),

    cirq.Moment(
        cirq.X(x).with_classical_controls('x1'),
        cirq.X(z).with_classical_controls('z1'),
    ),
])

simulator=cirq.Simulator()
result = simulator.simulate(circuit)

print(circuit)
print("\nDirac notation:")
print(result)

with open('result.txt','w+',encoding = 'utf-8') as f:
    print(circuit,file=f)
    print("\nDirac notation:",file=f)
    print(result,file=f)
