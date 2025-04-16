from _typeshed import Incomplete

def write_excel_xls(path, sheet_name, value) -> None:
    """将结果写入一个excel表
    Args:
        path: excel文件路径
        sheet_name: 一个字符串
        value: 待写入的结果，为二维列表
    """
def Hamiltonian_MaxCut(edge_list: Incomplete | None = None, j_list: Incomplete | None = None):
    """根据生成的随机图生成 MaxCut 问题的哈密顿量
    Args:
        edge_list: 随机图中包含的边，列表中的每个元素为一个元组，一个元组内包含边的两个顶点。
        j_list: 列表中的每个元素为每条边的权重。对于 unweighted 3-regular graphs (u3R)，每个边的权重都为1；
        unweighted 3-regular graphs (u3R)，每条边的权重为[0, 1]范围内的随机数。
    Return:
        H_p: 哈密顿量
    """
def INTERP(beta, gamma):
    """
    根据插值法，由第 p 层的最优参数给 p+1 层一个好的初参
    Args:
        beta: list, 长度为 p
        gamma: list, 长度为 p
    Return:
        new_theta: list, 长度为 2*(p+1)，前 p+1 个为 beta，后 p+1 个为gamma
    """
def pauli_zoperator_to_circuit(operator, qubits, input_ang=...):
    """ generate the quantum circuit for e^{-i * input_ang * operator}
    Args:
        operator: 在QAOA算法里， 这里需要传入的算符实际上就是目标哈密顿量 H_p
        qubits:
        input_ang: 参数 gamma
    Return:
        circuit
    """

class QAOA:
    """
    N = 4  ## 比特数
    R = 20  ## 前两层初参的随机次数
    P = 10  ## QAOA算法层数

    dir_u3r = r'./qaoa_result'   ## 输出文件所在的文件夹
    os.makedirs(dir_u3r, exist_ok=True)

    exp_file = r'\\exp.xls'
    params_file = r'\\params.xls'

    for r in range(1):
        ### MaxCut on unweighted 3-regular graphs (u3R)
        edge = random_regular_graph(3, N).edges()  ## 生成随机图
        j_list = [1] * len(edge)  ## 给定每个边的权重，这里是u3R图，所以每个边的权重都是1
        print('edge: ', edge)

        H_u3r = Hamiltonian_MaxCut(edge_list=edge,
                                   j_list=j_list)  ## 根据图生成MaxCut问题的哈密顿量
        qaoa_class = qaoa.QAOA(N, H_u3r)  ## 定义的关于QAOA算法的类
        info, params_info, _ = qaoa_class.run(layer=P,
                                              N_random=20,
                                              method='L-BFGS-B',
                                              tol=1e-5,
                                              period_gamma=0.5 * np.pi)

        write_excel_xls(exp_file, 'exp_r_poss_iter', info)
        write_excel_xls(params_file, 'beta_gamma', params_info)
    """
    n_qubits: Incomplete
    H_p: Incomplete
    exp_list: Incomplete
    iter: int
    iter_exp: Incomplete
    def __init__(self, n_qubits: Incomplete | None = None, Hamiltonian: Incomplete | None = None) -> None: ...
    def exp_of_string(self):
        """ calculate the energy of each basis state"""
    def allmin_of_list(self):
        """ find the groud state """
    def U_mixer(self, qubits, beta):
        """对于第 k 层 (1 <= k <= p )， 实现 exp(-i * beta_k * H_B), H_B = -1 * \\sum_{i=1}^n X_i
        Args:
            beta: 第 k 层的参数， 严格来说应该是 beta_k
        """
    def U_cost(self, qubits, gamma):
        """对于第 k 层 (1 <= k <= p )， 实现 exp(-i * gamma_k * H_P)
        Args:
            gamma: 第 k 层的参数， 严格来说应该是 gamma_k
        """
    def prep_state(self, params, qubits):
        """构造 p层的 QAOA 的线路
        Args:
            params: 长度为 2*p 的列表，前 p 个元素为 beta_1 ... beta_p, 后 p 个元素为 gamma_1 ... gamma_p
        """
    def expectation(self, params):
        """计算末态 |\\psi> 的期望值 exp = <\\psi| H_p |\\psi>"""
    def verb_func(self, params): ...
    def possibility_of_opt(self, params):
        """计算末态中的基态的概率"""
    def beta_gamma_params_bound_init(self, p, period_beta, period_gamma, beta_opt_1, gamma_opt_1, beta_opt, gamma_opt): ...
    def assert_beta_opt(self, beta_opt, p) -> None: ...
    def compute_params_opt(self, p, params_opt, exp_inter, exp_opt, beta_inter, gamma_inter, beta_opt_1, gamma_opt_1, beta_opt, gamma_opt): ...
    def run(self, layer: Incomplete | None = None, N_random: int = 20, method: str = 'L-BFGS-B', tol: float = 1e-05, options: Incomplete | None = None, period_beta=..., period_gamma=...):
        """运行QAOA线路，并设置初参和进行参数优化
        Args:
            layer: 想要运行的QAOA的最大线路层数
            N_random：前两层初参的随机次数
            method: 参数优化方法
            tol: 参数优化收敛精度
            options: 优化方法的一些设置
            period_beta: 参数beta的限制区间，和参数周期相关
            period_gamma: 参数gamma的限制区间，和参数周期相关
        """
