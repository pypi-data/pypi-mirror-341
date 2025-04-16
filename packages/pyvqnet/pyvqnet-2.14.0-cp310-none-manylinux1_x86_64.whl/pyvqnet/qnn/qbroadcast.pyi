from _typeshed import Incomplete

OPTIONS: Incomplete

def subset(wires, indices, periodic_boundary: bool = False): ...
def wires_ring(wires):
    """Wire sequence for the ring pattern"""
def wires_pyramid(wires):
    """Wire sequence for the pyramid pattern."""
def wires_all_to_all(wires):
    """Wire sequence for the all-to-all pattern"""

PATTERN_TO_WIRES: Incomplete
PATTERN_TO_NUM_PARAMS: Incomplete

def broadcast(unitary, wires, pattern, parameters: Incomplete | None = None, qubits: Incomplete | None = None):
    '''
    Applies a unitary multiple times to a specific pattern of wires.

    :param unitary: input quantum gate
    :param parameters: parameters of the template
    :param wires (Wires): wires that template acts on
    :param pattern (str): specifies the wire pattern
    :param qubits: input quantum bits

    :return: quantum circuits

    .. note::

        ``pattern="single"`` applies a single-wire unitary to each one of the :math:`M` wires.
        ``pattern="double"`` applies a two-wire unitary to :math:`\\lfloor \\frac{M}{2} \\rfloor`.
        ``pattern="double_odd"`` applies a two-wire unitary to :math:`\\lfloor \\frac{M-1}{2} \\rfloor`.
        ``pattern="chain"`` applies a two-wire unitary to all :math:`M-1` neighbouring pairs of wires.
        ``pattern="ring"`` applies a two-wire unitary to all :math:`M` neighbouring pairs of wires,where the last wire is considered to be a neighbour to the first one.
        ``pattern="pyramid"`` applies a two-wire unitary to wire pairs shaped in a pyramid declining to the right.
        ``pattern="all_to_all"`` applies a two-wire unitary to wire pairs that connect all wires to each other.
        A custom pattern can be passed by providing a list of wire lists to ``pattern``. The ``unitary`` is applied
      to each set of wires specified in the list.

    **Broadcasting single gates**

    In the simplest case:

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars = [1, 1, 0.1]
        cir_qbr = qbr(unitary=pq.RX, pattern="single", wires=[0, 1, 2], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    This is equivalent to the following circuit:

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars = [1, 1, 0.1]

        def template(qubits, pars):
            cir = pq.QCircuit()
            cir.insert(pq.RX(qubits[0], pars[0]))
            cir.insert(pq.RX(qubits[1], pars[1]))
            cir.insert(pq.RX(qubits[2], pars[2]))
            return cir

        cir_qbr = pq.QCircuit()
        cir_qbr.insert(template(qubits, pars))
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    **Broadcasting templates**

    Alternatively, one can broadcast a built-in or user-defined template:

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars = [1, 1, 0.1]

        def template(qubits, pars):
            cir = pq.QCircuit()
            cir.insert(pq.H(qubits))
            cir.insert(pq.RY(qubits, pars))
            return cir

        cir_qbr = qbr(unitary=template, pattern="single", wires=[0, 1, 2], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    **Constant unitaries**

    the ``unitary`` argument does not take parameters.

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        cir_qbr = qbr(unitary=pq.H, pattern="single", wires=[0, 1, 2], qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    **Multiple parameters in unitary**

    The unitary, whether it is a single gate or a user-defined template, can take multiple parameters.

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars = [[1, 1], [2, 1], [0.1, 1]]

        def template(qubits, pars):
            cir = pq.QCircuit()
            cir.insert(pq.H(qubits))
            cir.insert(pq.RY(qubits, pars[0]))
            cir.insert(pq.RX(qubits, pars[1]))
            return cir

        cir_qbr = qbr(unitary=template, pattern="single", wires=[0, 1, 2], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    **Different patterns**

    The basic usage of the different patterns works as follows:

    * Double pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 4
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [-1, 2.5, 3]
        pars2 = [-1, 4, 2]
        par = [pars1, pars2]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="double", wires=[0, 1, 2, 3], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * Double-odd pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 4
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [-5.3, 2.3, 3]
        par = [pars1]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="double_odd", wires=[0, 1, 2, 3], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        prog.insert(pq.BARRIER(qubits))  # block the operating qubit
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * Chain pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 4
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [1.8, 2, 3]
        pars2 = [-1, 3, 1]
        pars3 = [2, -1.2, 4]
        par = [pars1, pars2, pars3]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="chain", wires=[0, 1, 2, 3], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * Ring pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 3
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [1, -2.2, 3]
        pars2 = [-1, 3, 1]
        pars3 = [2.6, 1, 4]
        par = [pars1, pars2, pars3]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="ring", wires=[0, 1, 2], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    However, there is an exception for 2 wires, where only one set of parameters is needed.
    This avoids repeating a gate over the
    same wires twice:

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 2
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [-3.2, 2, 1.2]
        par = [pars1]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="ring", wires=[0, 1], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * Pyramid pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 4
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [1.1, 2, 3]
        pars2 = [-1, 3, 1]
        pars3 = [2, 1, 4.2]
        par = [pars1, pars2, pars3]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="pyramid", wires=[0, 1, 2, 3], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * All-to-all pattern

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 4
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pars1 = [1, 2, 3]
        pars2 = [-1, 3, 1]
        pars3 = [2, 1, 4]
        pars4 = [-1, -2, -3]
        pars5 = [2, 1, 4]
        pars6 = [3, -2, -3]
        par = [pars1, pars2, pars3, pars4, pars5, pars6]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern="all_to_all", wires=[0, 1, 2, 3], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    * Custom pattern

    For a custom pattern, the wire lists for each application of the unitary is
              passed to ``pattern``:

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 5
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pattern = [[0, 1], [3, 4]]
        cir_qbr = qbr(unitary=pq.CNOT, pattern=pattern, wires=np.arange(5), qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)

    When using a parametrized unitary, make sure that the number of wire lists in ``pattern`` corresponds to the
    number of parameters in ``parameters``.

    Example::

        import pyqpanda as pq
        from pyvqnet.qnn.qbroadcast import broadcast as qbr
        from pyvqnet.qnn.measure import expval

        num_qubits = 5
        machine = pq.CPUQVM()  # outside
        machine.init_qvm()  # outside
        qubits = machine.qAlloc_many(num_qubits)
        pattern = [[0, 1], [3, 4]]
        pars1 = [1, 2, 3]
        pars2 = [-1, 3, 1]
        par = [pars1, pars2]
        pars = par
        cir_qbr = qbr(unitary=pq.CU, pattern=pattern, wires=[0, 1, 2, 3, 4], parameters=pars, qubits=qubits)
        print(cir_qbr)

        prog = pq.QProg()
        prog.insert(cir_qbr)
        pauli_str = {"Z0": 1.0}
        exp = expval(machine, prog, pauli_str, qubits)
        print(exp)


    '''
