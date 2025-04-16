def decimal_to_binary(decimal_num, num_bits): ...
def pq_add_k_fourier(qlist, k, wires): ...
def pyqpanda_qft_add_to_register(m, k, qlist, clist):
    """

    Adding a number to a register

    .. math:: \text{Sum(k)}\x0bert m \rangle = \x0bert m + k \rangle.

    The procedure to implement this unitary operation is the following:
    (1). Convert the state from the computational basis into the Fourier basis by applying the QFT to the :math:`\x0bert m \rangle` state via the :class:`~pennylane.QFT` operator.
    (2). Rotate the :math:`j`-th qubit by the angle :math:`\x0crac{2k\\pi}{2^{j}}` using the :math:`R_Z` gate, which leads to the new phases, :math:`\x0crac{2(m + k)\\pi}{2^{j}}`.
    (3). Apply the QFT inverse to return to the computational basis and obtain :math:`m+k`.
 
    :param m: classic integar to embedded in register.
    :param k: classic integar to added to the register.
    :param qlist: qubits list allocated by pyqpanda.
    :parma clist: classic bits  allocated by pyqpanda.

    :return:
        dict result of add opertaion.

    Example::

        import numpy as np
        import pyqpanda as pq
        from pyvqnet.qnn import pyqpanda_qft_add_to_register
        m = 1
        k = 1
        num_wires = 4

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)

        qlist = m_machine.qAlloc_many(num_wires)
        cbits = m_machine.cAlloc_many(num_wires)

        result = pyqpanda_qft_add_to_register(m,k,qlist)

    """
def pyqpanda_qft_addition(wires_m, wires_k, wires_solution, qlist): ...
def pyqpanda_qft_add_two_register(m, k, wires_m, wires_k, wires_solution, qlist, clist):
    """
    Adding two different registers.

    .. math:: \text{Sum}_2\x0bert m \rangle \x0bert k \rangle \x0bert 0 \rangle = \x0bert m \rangle \x0bert k \rangle \x0bert m+k \rangle

    In this case, we can understand the third register (which is initially
    at :math:`0`) as a counter that will tally as many units as :math:`m` and
    :math:`k` combined. The binary decomposition will
    make this simple. If we have :math:`\x0bert m \rangle = \x0bert \\overline{q_0q_1q_2} \rangle`, we will
    have to add :math:`1` to the counter if :math:`q_2 = 1` and nothing
    otherwise. In general, we should add :math:`2^{n-i-1}` units if the :math:`i`-th
    qubit is in state :math:`\x0bert 1 \rangle` and 0 otherwise.


    :param m: classic integar to embedded in register as the lhs.
    :param k: classic integar to embedded in the register as the rhs.
    :param wires_m: index of qubits to encode m.
    :param wires_k: index of qubits to encode k.
    :param wires_solution: index of qubits to encode solution.
    :param qlist: qubits list allocated by pyqpanda.
    :parma clist: classic bits  allocated by pyqpanda.

    :return:
        dict result of add opertaion.
    Example::

        import numpy as np
        import pyqpanda as pq
        from pyvqnet.qnn import pyqpanda_qft_add_two_register
        
        m = 3
        k = 4
        wires_m = [0, 1 ,2]           # qubits needed to encode m
        wires_k = [3, 4 ,5]           # qubits needed to encode k
        wires_solution = [6, 7, 8,9,10]  # qubits needed to encode the solution

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        num_wires = len(wires_m) + len(wires_k) + len(wires_solution)
        qlist = m_machine.qAlloc_many(num_wires)
        cbits = m_machine.cAlloc_many(num_wires)

        result = pyqpanda_qft_add_two_register(m,k, wires_m, wires_k, wires_solution, qlist,cbits)

        print(result)
    """
def pyqpanda_qft_multiplication(wires_m, wires_k, wires_solution, qlist): ...
def pyqpanda_qft_mul(m, k, wires_m, wires_k, wires_solution, qlist, clist):
    """
    Apply Multiplying qubits quantum opertation.

    .. math:: \text{Mul}\x0bert m \rangle \x0bert k \rangle \x0bert 0 \rangle = \x0bert m \rangle \x0bert k \rangle \x0bert m\\cdot k \rangle

    :param m: classic integar to embedded in register as the lhs.
    :param k: classic integar to embedded in the register as the rhs.
    :param wires_m: index of qubits to encode m.
    :param wires_k: index of qubits to encode k.
    :param wires_solution: index of qubits to encode solution.
    :param qlist: qubits list allocated by pyqpanda.
    :parma clist: classic bits  allocated by pyqpanda.

    :return:
        dict result of mul opertaion.

    Example::

        import numpy as np
        import pyqpanda as pq
        from pyvqnet.qnn import pyqpanda_qft_mul

        m = 3
        k = 4
        wires_m = [0, 1 ,2]           # qubits needed to encode m
        wires_k = [3, 4 ,5]           # qubits needed to encode k
        wires_solution = [6, 7, 8,9,10]  # qubits needed to encode the solution

        m_machine = pq.init_quantum_machine(pq.QMachineType.CPU)
        num_wires = len(wires_m) + len(wires_k) + len(wires_solution)
        qlist = m_machine.qAlloc_many(num_wires)
        cbits = m_machine.cAlloc_many(num_wires)

        result = pyqpanda_qft_mul(m,k, wires_m, wires_k, wires_solution, qlist,cbits)

        print(result)


    """
