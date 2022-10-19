import cirq
import qsimcirq
import numpy as np
import sympy as sp
import pandas
import random
import time

logic0=['000000000','011010000','101100000','110110000']
logic1=['000110000','011100000','101010000','110000000']
e=1e-5

class error_init(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        ps = [1.0 - self._p, self._p]
        ops = [cirq.unitary(cirq.I), cirq.unitary(cirq.X)]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"error_init({self._p})"
    
class error_I(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        ps = [1.0 - self._p, self._p/3, self._p/3, self._p/3]
        ops = [cirq.unitary(cirq.I), cirq.unitary(cirq.X), cirq.unitary(cirq.Y), cirq.unitary(cirq.Z)]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"error_I({self._p})"

class error_H(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        ps = [1.0 - self._p, self._p/3, self._p/3, self._p/3]
        ops = [cirq.unitary(cirq.H), np.dot(cirq.unitary(cirq.H),cirq.unitary(cirq.X)), np.dot(cirq.unitary(cirq.H),cirq.unitary(cirq.Y)), np.dot(cirq.unitary(cirq.H),cirq.unitary(cirq.Z))]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"error_H({self._p})"

class error_CNOT(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 2

    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        ps = [1.0 - self._p, self._p/15, self._p/15, self._p/15, 
              self._p/15, self._p/15, self._p/15, 
              self._p/15, self._p/15, self._p/15, 
              self._p/15, self._p/15, self._p/15, 
              self._p/15, self._p/15, self._p/15]
        ops = [cirq.unitary(cirq.CNOT), 
               np.kron(cirq.I,cirq.unitary(cirq.X)), 
               np.kron(cirq.I,cirq.unitary(cirq.Y)), 
               np.kron(cirq.I,cirq.unitary(cirq.Z)),
               
               np.kron(cirq.unitary(cirq.X),cirq.I), 
               np.kron(cirq.unitary(cirq.X),cirq.unitary(cirq.X)), 
               np.kron(cirq.unitary(cirq.X),cirq.unitary(cirq.Y)), 
               np.kron(cirq.unitary(cirq.X),cirq.unitary(cirq.Z)),
               
               np.kron(cirq.unitary(cirq.Y),cirq.I), 
               np.kron(cirq.unitary(cirq.Y),cirq.unitary(cirq.X)), 
               np.kron(cirq.unitary(cirq.Y),cirq.unitary(cirq.Y)), 
               np.kron(cirq.unitary(cirq.Y),cirq.unitary(cirq.Z)),
               
               np.kron(cirq.unitary(cirq.Z),cirq.I), 
               np.kron(cirq.unitary(cirq.Z),cirq.unitary(cirq.X)), 
               np.kron(cirq.unitary(cirq.Z),cirq.unitary(cirq.Y)), 
               np.kron(cirq.unitary(cirq.Z),cirq.unitary(cirq.Z))]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return f"error_CNOT({self._p})" 

class error_aftermeasure(cirq.Gate):
    def _num_qubits_(self) -> int:
        return 1

    def __init__(self, p: float) -> None:
        self._p = p

    def _mixture_(self):
        ps = [1.0 - self._p, self._p]
        ops = [cirq.unitary(cirq.I),cirq.unitary(cirq.X)]
        return tuple(zip(ps, ops))

    def _has_mixture_(self) -> bool:
        return True

    def _circuit_diagram_info_(self, args) -> str:
        return '@',f"error_aftermeasure({self._p})"     

class my_surface_code_3():
    def __init__(self,noise_p):
        self.error = cirq.asymmetric_depolarize(p_x=noise_p/3,p_y=noise_p/3,p_z=noise_p/3)
        self.moment_list=[]
        self.z12 = cirq.NamedQubit("z12")
        self.z32 = cirq.NamedQubit("z32")

        self.x21 = cirq.NamedQubit("x21")
        self.x23 = cirq.NamedQubit("x23")

        self.q11 = cirq.NamedQubit("q11")
        self.q13 = cirq.NamedQubit("q13")
        self.q22 = cirq.NamedQubit("q22")
        self.q31 = cirq.NamedQubit("q31")
        self.q33 = cirq.NamedQubit("q33")

        self.error_I=error_I(noise_p)
        self.error_H=error_H(noise_p)
        self.error_init=error_init(noise_p)
        self.error_CNOT=error_CNOT(noise_p)
        self.error_aftermeasure=error_aftermeasure(noise_p)
        
        self.circuit=cirq.Circuit()
        self.circuit.append(cirq.Moment(
            self.error_init.on_each([
                cirq.NamedQubit('q11'),
                cirq.NamedQubit('q13'),
                cirq.NamedQubit('q22'),
                cirq.NamedQubit('q31'),
                cirq.NamedQubit('q33'),
                cirq.NamedQubit('z12'),
                cirq.NamedQubit('x21'),
                cirq.NamedQubit('x23'),
                cirq.NamedQubit('z32')]))
        )
        self.check()
        self.moment_list.append([i for i, moment in enumerate(self.circuit)][-1])
        
    def check(self):
        self.circuit.append(cirq.Moment(
            self.error_I(cirq.NamedQubit('z12')),
            self.error_I(cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            self.error_H(cirq.NamedQubit('x21')),
            self.error_H(cirq.NamedQubit('x23')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q11'), cirq.NamedQubit('z12')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q13'), cirq.NamedQubit('z12')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q22'), cirq.NamedQubit('z12')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q11')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q22')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x21'), cirq.NamedQubit('q31')))  
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q13')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q22')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('x23'), cirq.NamedQubit('q33')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q22'), cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q31'), cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            self.error_CNOT(cirq.NamedQubit('q33'), cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            cirq.measure(cirq.NamedQubit('z12'),key='c12'),
            cirq.measure(cirq.NamedQubit('z32'),key='c32'),
            self.error_H(cirq.NamedQubit('x21')),
            self.error_H(cirq.NamedQubit('x23')))
        )
        self.circuit.append(cirq.Moment(
            self.error_aftermeasure(cirq.NamedQubit('z12')),
            self.error_aftermeasure(cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            cirq.measure(cirq.NamedQubit('z12'),key='c12'),
            cirq.measure(cirq.NamedQubit('z32'),key='c32'))
        )
        self.circuit.append(cirq.Moment(
            cirq.measure(cirq.NamedQubit('x21'),key='c21'),
            cirq.measure(cirq.NamedQubit('x23'),key='c23'),
            self.error_I(cirq.NamedQubit('z12')),
            self.error_I(cirq.NamedQubit('z32')))
        )
        self.circuit.append(cirq.Moment(
            self.error_aftermeasure(cirq.NamedQubit('x21')),
            self.error_aftermeasure(cirq.NamedQubit('x23')))
        )
        self.circuit.append(cirq.Moment(
            cirq.measure(cirq.NamedQubit('x21'),key='c21'),
            cirq.measure(cirq.NamedQubit('x23'),key='c23'))
        )
        
        self.circuit.append(cirq.Moment(
            cirq.X(cirq.NamedQubit('x21')).with_classical_controls('c21'),
            cirq.X(cirq.NamedQubit('x23')).with_classical_controls('c23'),
            cirq.X(cirq.NamedQubit('z12')).with_classical_controls('c12'),
            cirq.X(cirq.NamedQubit('z32')).with_classical_controls('c32'),
        ))
        self.circuit.append(cirq.Moment(    
            cirq.X(cirq.NamedQubit('q11')).with_classical_controls('c12'),
        ))
        self.circuit.append(cirq.Moment(
            cirq.Z(cirq.NamedQubit('q11')).with_classical_controls('c21'),
        ))
        self.circuit.append(cirq.Moment(
            cirq.Z(cirq.NamedQubit('q13')).with_classical_controls('c23'),
        ))
        self.circuit.append(cirq.Moment(
            cirq.X(cirq.NamedQubit('q31')).with_classical_controls('c32'),
        )) 
        
    def x(self):
        self.circuit.append(cirq.Moment(
            cirq.X(cirq.NamedQubit('q11')),cirq.X(cirq.NamedQubit('q13'))
        ))
        self.check()
        self.moment_list.append([i for i, moment in enumerate(self.circuit)][-1])
        
    def z(self):
        self.circuit.append(cirq.Moment(
            cirq.Z(cirq.NamedQubit('q11')),cirq.Z(cirq.NamedQubit('q31'))
        ))
        self.check()
        self.moment_list.append([i for i, moment in enumerate(self.circuit)][-1])
        
    def simulate(self,alltime=0):
        simulator = cirq.Simulator()
        result = simulator.simulate_moment_steps((self.circuit))
        for i,step in enumerate(result):
            if alltime==1:
                print(step.dirac_notation())
                print()
                print(step.state_vector()[step.state_vector().nonzero()[0][1]]/step.state_vector()[step.state_vector().nonzero()[0][0]],step.state_vector()[step.state_vector().nonzero()[0][0]]/step.state_vector()[step.state_vector().nonzero()[0][1]])
            else:
                if i in self.moment_list:
                    print(step.dirac_notation())
                    print()
    
    def simulate_mul(self,re=1,io=0):
        simulator = cirq.Simulator()
        accept=0
        discard=0
        error=0
        k=0
        while k<re:
            try:
                result = simulator.simulate(self.circuit)
                k=k+1
            except:
                continue
            temp=result.dirac_notation(8).split('⟩')
            judge_dict={}
            for i in temp:
                if len(i)>0:
                    result_temp=i.split('|')
                    num=result_temp[0]
                    if num[0]==' ':
                        num=num[3:]
                    num=complex(num)
                    bits=result_temp[1]
                    judge_dict[bits]=num
            fai=0
            flag=0
            one=0
            if not len(judge_dict)==4:
                discard=discard+1
                if io==1:
                    print(judge_dict)
                continue
            else:
                if '000000000' in judge_dict and '011010000' in judge_dict and'101100000' in judge_dict and '110110000' in judge_dict:
                    fai=judge_dict['011010000']/judge_dict['000000000']
                    if fai==judge_dict['101100000']/judge_dict['000000000'] and fai==judge_dict['110110000']/judge_dict['000000000']:
                        error=error+1
                        if io==1:
                            print('x error')
                        continue
                    else:
                        discard=discard+1
                        if io==1:
                            print(judge_dict)
                        continue
                elif '000110000' in judge_dict  and '011100000' in judge_dict and'101010000' in judge_dict and '110000000' in judge_dict:
                    fai=judge_dict['011100000']/judge_dict['000110000']
                    if fai==judge_dict['101010000']/judge_dict['000110000'] and fai==judge_dict['110000000']/judge_dict['000110000']:
                        accept=accept+1
                        continue
                    else:
                        discard=discard+1
                        if io==1:
                            print(judge_dict)
                        continue
                else:
                    discard=discard+1
                    if io==1:
                        print(judge_dict)
                    continue
        print(accept,discard,error)
        
    def print_curcuit(self):
        print(self.circuit)
    
        
if __name__=='__main__':
    noise_p=0.01
    re=10000
    times=0
    code=my_surface_code_3(noise_p)
    code.x()
    #code.measure()
    qsim_start = time.time()
    code.simulate_mul(re=re,io=0)
    qsim_elapsed = time.time() - qsim_start
    print(f'{noise_p}, {times} x gates for {re} times, qsim runtime: {qsim_elapsed} seconds.')  
    
      