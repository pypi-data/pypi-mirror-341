from .. import dist_cal_src as dist_cal_src
from _typeshed import Incomplete
from pyvqnet.tensor import tensor as tensor

comm: Incomplete
is_dist_init: bool

def is_initialized(): ...
def is_available(): ...
def get_host_hash(string): ...
def get_host_name(): ...
def allgather_host_name(): ...
def get_local_rank():
    """
    A method to get the process number on the current host.

    Example::

        from pyvqnet.distributed import get_local_rank
                
        local_rank = get_local_rank()
        
        # mpirun -n 2 -f hosts python test.py 
    """
def get_rank():
    """
    A method to get the current process number.

    Example::

        from pyvqnet.distributed import get_rank
        cur_rank = get_rank()
        
    """
get_global_rank = get_rank

def get_size():
    """
    A method to get all process numbers.

    Example::

        from pyvqnet.distributed import get_size        
        size = get_size()
        
    """
get_world_size = get_size

def get_group(): ...
def get_name(): ...
def init_group(rank_lists): ...

class CommController:
    '''
    CommController: A method for generating distributed computing communications controller

    :param backend: Create a cpu(mpi) or gpu(nccl) communication controller.

    Example::

        from pyvqnet.distributed import CommController
        Comm_OP = CommController("nccl") # init nccl controller
    '''
    backend: Incomplete
    nccl_op: Incomplete
    rank: Incomplete
    size: Incomplete
    localrank: Incomplete
    groupComm: Incomplete
    send: Incomplete
    recv: Incomplete
    barrier: Incomplete
    barrier_group: Incomplete
    allreduce: Incomplete
    allreduce_group: Incomplete
    reduce: Incomplete
    reduce_group: Incomplete
    broadcast: Incomplete
    broadcast_group: Incomplete
    allgather: Incomplete
    allgather_group: Incomplete
    group_size: int
    def __init__(self, backend: str = 'mpi') -> None: ...
    def is_nccl_available():
        """Check if the NCCL backend is available."""
    def getRank(self):
        '''
        A method to get the current process number.

        Example::

            from pyvqnet.distributed import CommController
            Comm_OP = CommController("nccl") # init nccl controller
            
            Comm_OP.getRank()
        '''
    def getSize(self):
        '''
        A method to get all process numbers.

        Example::

            from pyvqnet.distributed import CommController
            Comm_OP = CommController("nccl") # init nccl controller
            
            Comm_OP.getSize()
            # mpirun -n 2 python test.py 
            # 2
        '''
    def getLocalRank(self):
        '''
        A method to get the process number on the current host.

        Example::

            from pyvqnet.distributed import CommController
            Comm_OP = CommController("nccl") # init nccl controller
            
            Comm_OP.getLocalRank()
            # mpirun -n 2 -f hosts python test.py 
        '''
    def ncclSplitGroup(self, rankL) -> None:
        '''
        A method for grouping processes (gpu).

        :param rankL: Process Group List.
        
        Example::

            from pyvqnet.distributed import CommController
            Comm_OP = CommController("nccl")
            
            Comm_OP.ncclSplitGroup([[0, 1]])
            # mpirun -n 2 -f hosts python test.py
        '''
    def GetDeviceNum(self):
        '''
        A method to get the number of graphics cards on the current node.

        Example::

            from pyvqnet.distributed import CommController
            Comm_OP = CommController("nccl")
            
            Comm_OP.GetDeviceNum()
            # 2
        '''
    def grad_allreduce(self, optimizer) -> None:
        '''
        Allreduce optimizer grad.

        :param optimizer: optimizer.
        
        Example::

            from pyvqnet.distributed import CommController,get_rank,get_local_rank
            from pyvqnet.tensor import tensor
            from pyvqnet.nn.module import Module
            from pyvqnet.nn.linear import Linear
            from pyvqnet.nn.loss import MeanSquaredError
            from pyvqnet.optim import Adam
            from pyvqnet.nn import activation as F
            import numpy as np
            Comm_OP = CommController("nccl")

            class Net(Module):
                def __init__(self):
                    super(Net, self).__init__()
                    self.fc = Linear(input_channels=5, output_channels=1)
                def forward(self, x):
                    x = F.ReLu()(self.fc(x))
                    return x
                
            model = Net().toGPU(1000+ get_local_rank())
            opti = Adam(model.parameters(), lr=0.01)
            actual = tensor.QTensor([1,1,1,1,1,0,0,0,0,0],dtype=6).reshape((10,1)).toGPU(1000+ get_local_rank())
            x = tensor.randn((10, 5)).toGPU(1000+ get_local_rank())
            for i in range(10):
                opti.zero_grad()
                model.train()
                result = model(x)
                loss = MeanSquaredError()(actual, result)
                loss.backward()
                # print(f"rank {get_rank()} grad is {model.parameters()[0].grad} para {model.parameters()[0]}")
                Comm_OP.grad_allreduce(opti)
                # print(Comm_OP._allgather(model.parameters()[0]))
                if get_rank() == 0 :
                    print(f"rank {get_rank()} grad is {model.parameters()[0].grad} para {model.parameters()[0]} after")
                opti.step()
            # mpirun -n 2 python test.py
        '''
    def param_allreduce(self, model) -> None:
        '''
        Allreduce model parameters.

        :param model: model.
        
        Example::

            from pyvqnet.distributed import CommController,get_rank,get_local_rank
            from pyvqnet.tensor import tensor
            from pyvqnet.nn.module import Module
            from pyvqnet.nn.linear import Linear
            from pyvqnet.nn import activation as F
            import numpy as np
            Comm_OP = CommController("nccl")

            class Net(Module):
                def __init__(self):
                    super(Net, self).__init__()
                    self.fc = Linear(input_channels=5, output_channels=1)
                def forward(self, x):
                    x = F.ReLu()(self.fc(x))
                    return x
                
            model = Net().toGPU(1000+ get_local_rank())
            print(f"rank {get_rank()} parameters is {model.parameters()}")
            Comm_OP.param_allreduce(model)
                
            if get_rank() == 0:
                print(model.parameters())
        '''
    def broadcast_model_params(self, model, root: int = 0) -> None:
        '''
        Broadcast model parameter from a specified process to all process.
        
        :param: model: `Module`.
        :param: root: the specified rank.
        
        Example::
        
            from pyvqnet.distributed import CommController,get_rank,get_local_rank
            from pyvqnet.tensor import tensor
            from pyvqnet.nn.module import Module
            from pyvqnet.nn.linear import Linear
            from pyvqnet.nn import activation as F
            import numpy as np
            Comm_OP = CommController("nccl")

            class Net(Module):
                def __init__(self):
                    super(Net, self).__init__()
                    self.fc = Linear(input_channels=5, output_channels=1)
                def forward(self, x):
                    x = F.ReLu()(self.fc(x))
                    return x
                
            model = Net().toGPU(1000+ get_local_rank())
            print(f"bcast before rank {get_rank()}:{model.parameters()}")
            Comm_OP.broadcast_model_params(model, 0)
            # model = model
            print(f"bcast after rank {get_rank()}: {model.parameters()}")
        
        '''
    def acc_allreduce(self, acc):
        '''
        Allreduce model accuracy.
        
        :param: acc: model accuracy.
        
        Example::
        
            from pyvqnet.distributed import CommController,get_rank,get_local_rank
            from pyvqnet.tensor import tensor
            from pyvqnet.nn.module import Module
            from pyvqnet.nn.linear import Linear
            from pyvqnet.nn.loss import MeanSquaredError
            from pyvqnet.optim import Adam
            from pyvqnet.nn import activation as F
            import numpy as np
            Comm_OP = CommController("nccl")

            def get_accuary(result, label):
                result = (result > 0.5).astype(4)
                score = tensor.sums(result == label)
                return score

            class Net(Module):
                def __init__(self):
                    super(Net, self).__init__()
                    self.fc = Linear(input_channels=5, output_channels=1)
                def forward(self, x):
                    x = F.ReLu()(self.fc(x))
                    return x
            model = Net().toGPU(1000+ get_local_rank())
            opti = Adam(model.parameters(), lr=0.01)
            actual = tensor.QTensor([1,1,1,1,1,0,0,0,0,0],dtype=6).reshape((10,1)).toGPU(1000+ get_local_rank())
            x = tensor.randn((10, 5)).toGPU(1000+ get_local_rank())
            accuary = 0
            count = 0
            for i in range(100):
                opti.zero_grad()
                model.train()
                result = model(x)
                loss = MeanSquaredError()(actual, result)
                loss.backward()
                opti.step()
                
                count += 1
                accuary += get_accuary(result, actual.reshape([-1,1]))
            print(
                    f"rank {get_rank()} #####accuray:{accuary/count} #### {Comm_OP.acc_allreduce(accuary)/count}"
                )
        '''
    def __del__(self) -> None: ...
