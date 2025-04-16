import pyqpanda as pq

__all__ = ['expval', 'QuantumMeasure', 'ProbsMeasure', 'DensityMatrixFromQstate', 'VN_Entropy', 'Mutal_Info', 'Hermitian_expval', 'VarMeasure', 'Purity', 'MeasurePauliSum']

Hermitian_expval = hermitian_expval
Hermitian = hermitian
DensityMatrixFromQstate = densitymatrixfromqstate
VN_Entropy = vn_entropy
Mutal_Info = mutal_info

def expval(machine: pq.QuantumMachine, prog: pq.QProg, pauli_str_dict: dict, qlists: pq.QVec):
    """expval(machine,prog,pauli_str_dict,qlists)
    Expectation value of the supplied Hamiltonian observables

    if the observables are :math:`0.7Z\\otimes X\\otimes I+0.2I\\otimes Z\\otimes I`,
    then ``Hamiltonian`` ``dict`` would be ``{{'Z0, X1':0.7} ,{'Z1':0.2}}`` .

    expval api only supports on QPanda CPUQVM now.Please checks
      https://pyqpanda-toturial.readthedocs.io/zh/latest/index.html for alternative api.

    :param machine: machine created by qpanda
    :param prog: quantum program created by qpanda
    :param pauli_str_dict: Hamiltonian observables
    :param qlists: qubit allocated by pyQpanda.qAlloc_many()
    :return: expectation

    Example::

        input = [0.56, 0.1]
        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        m_prog = pq.QProg()
        m_qlist = m_machine.qAlloc_many(3)
        cir = pq.QCircuit()
        cir.insert(pq.RZ(m_qlist[0],input[0]))
        cir.insert(pq.CNOT(m_qlist[0],m_qlist[1]))
        cir.insert(pq.RY(m_qlist[1],input[1]))
        cir.insert(pq.CNOT(m_qlist[0],m_qlist[2]))
        m_prog.insert(cir)
        pauli_dict  = {'Z0 X1':10,'Y2':-0.543}
        exp2 = expval(m_machine,m_prog,pauli_dict,m_qlist)
        print(exp2)
        pq.destroy_quantum_machine(m_machine)
    """
ExpVal = expval
QuantumMeasure = quantum_measure
ProbsMeasure = probs_measure
VarMeasure = var_measure
MeasurePauliSum = measure_paulisum
Purity = purity
