# Copyright (c) 2017-2023 Origin Quantum Computing. All Right Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#pylint:disable=too-many-lines
#pylint:disable=unsubscriptable-object
#pylint:disable=no-name-in-module
#pylint:disable=bare-except
#pylint:disable=unnecessary-lambda
#pylint:disable=wrong-import-position
from .xtensor import ones, empty, zeros_like, zeros, \
    XTensor, empty_like, ones_like,_GRAD_REQ_MAP,squeeze,\
    broadcast_to,arange, stack,make_array,transpose, nonzero,\
    full_like,full,linspace,logspace,randn,randu,eye,\
    diag,sign,logical_and,logical_not,logical_or,logical_xor,\
    greater,greater_equal,lesser,lesser_equal,equal,isfinite,\
    isinf,isneginf,isposinf,isnan,max,min,flatten,tile,permute,\
    swapaxis,clip,unsqueeze,broadcast,concat,cat,\
    concatenate,round,ceil,floor,sign,neg,exp,abs,log,sqrt,square,\
    sin,cos,tan,atan,acos,asin,tanh,sinh,cosh,mean,median,var,std,\
    sum,sums,argsort,sort,reciprocal,matmul,trace,topk,argtopk,\
    frobenius_norm,maximum,minimum,power,where,tril,triu,softmax,\
    log_softmax,flip,multinomial,masked_fill,cumsum,index_select,\
    kron,xtensor,reshape,relu,sigmoid,leaky_relu,hard_sigmoid,elu,\
    soft_plus,softplus,softsign,argtopK,topK,to_xtensor,add,sub,mul,divide,\
    less,not_equal,less_equal,argmax,argmin

from .xtensor_addon import pad_sequence, pack_pad_sequence, pad_packed_sequence
from .context import cpu, cpu_pinned, gpu
from .random import seed

from .loss import SoftmaxCrossEntropy, CategoricalCrossEntropy, BinaryCrossEntropy,NLL_Loss,\
    CrossEntropyLoss,MeanSquaredError,NLLLoss,BCELoss,MSELoss

from .optimizer import SGD, Adadelta, RMSProp, RMSprop, Adagrad, Adam, Adamax

from .module import Module, Conv1D, Conv2D,ConvT1D,ConvT2D,MaxPool2D,MaxPool1D,AvgPool1D,\
    AvgPool2D,ModuleList,Embedding,LayerNorm1d,LayerNorm2d,LayerNormNd,\
    Pixel_Shuffle, Pixel_Unshuffle,Dropout,Linear

from .rnn import RNN, Dynamic_RNN
from .gru import GRU, Dynamic_GRU
from .lstm import LSTM, Dynamic_LSTM

from .storage import save_parameters, load_parameters
from .batchnorm import BatchNorm,BatchNorm1d, BatchNorm2d

from .qvc import QuantumLayer
from .qcloud import QuantumBatchAsyncQcloudLayer

from ..dtype import kbool,\
kuint8 ,\
kint8 ,\
kint16 ,\
kint32 ,\
kint64,\
kfloat32 ,\
kfloat64 ,\
kcomplex64 ,\
kcomplex128 