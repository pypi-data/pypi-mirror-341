from typing import List, Tuple, Union

import paddle

IGNORE_ID = -1


def broadcast_shape(shp1, shp2):
    result = []
    for a, b in zip(shp1[::-1], shp2[::-1]):
        result.append(max(a, b))
    return result[::-1]


def pad_sequence(sequences: List[paddle.Tensor],
                 batch_first: bool = False,
                 padding_value: float = 0.0) -> paddle.Tensor:
    r"""Pad a list of variable length Tensors with ``padding_value``

    ``pad_sequence`` stacks a list of Tensors along a new dimension,
    and pads them to equal length. For example, if the input is list of
    sequences with size ``L x *`` and if batch_first is False, and ``T x B x *``
    otherwise.

    `B` is batch size. It is equal to the number of elements in ``sequences``.
    `T` is length of the longest sequence.
    `L` is length of the sequence.
    `*` is any number of trailing dimensions, including none.

    Example:
        >>> from ppasr.model_utils.utils.common import pad_sequence
        >>> a = paddle.ones(25, 300)
        >>> b = paddle.ones(22, 300)
        >>> c = paddle.ones(15, 300)
        >>> pad_sequence([a, b, c]).shape
        paddle.Tensor([25, 3, 300])

    Note:
        This function returns a Tensor of size ``T x B x *`` or ``B x T x *``
        where `T` is the length of the longest sequence. This function assumes
        trailing dimensions and type of all the Tensors in sequences are same.

    Args:
        sequences (list[Tensor]): list of variable length sequences.
        batch_first (bool, optional): output will be in ``B x T x *`` if True, or in
            ``T x B x *`` otherwise
        padding_value (float, optional): value for padded elements. Default: 0.

    Returns:
        Tensor of size ``T x B x *`` if :attr:`batch_first` is ``False``.
        Tensor of size ``B x T x *`` otherwise
    """

    # assuming trailing dimensions and type of all the Tensors
    # in sequences are same and fetching those from sequences[0]
    max_size = paddle.shape(sequences[0])
    # trailing_dims = max_size[1:]
    trailing_dims = tuple(max_size[1:].numpy().tolist()) if sequences[0].ndim >= 2 else ()
    max_len = max([s.shape[0] for s in sequences])
    if batch_first:
        out_dims = (len(sequences), max_len) + trailing_dims
    else:
        out_dims = (max_len, len(sequences)) + trailing_dims
    out_tensor = paddle.full(out_dims, padding_value, sequences[0].dtype)
    for i, tensor in enumerate(sequences):
        length = tensor.shape[0]
        # use index notation to prevent duplicate references to the tensor
        if batch_first:
            # out_tensor[i, :length, ...] = tensor
            if length != 0:
                out_tensor[i, :length] = tensor
            else:
                out_tensor[i, length] = tensor
        else:
            # out_tensor[:length, i, ...] = tensor
            if length != 0:
                out_tensor[:length, i] = tensor
            else:
                out_tensor[length, i] = tensor

    return out_tensor


def pad_list(xs: List[paddle.Tensor], pad_value: int):
    """Perform padding for the list of tensors.

    Args:
        xs (List): List of Tensors [(T_1, `*`), (T_2, `*`), ..., (T_B, `*`)].
        pad_value (float): Value for padding.

    Returns:
        Tensor: Padded tensor (B, Tmax, `*`).

    Examples:
        >>> x = [paddle.ones(4), paddle.ones(2), paddle.ones(1)]
        >>> x
        [tensor([1., 1., 1., 1.]), tensor([1., 1.]), tensor([1.])]
        >>> pad_list(x, 0)
        tensor([[1., 1., 1., 1.],
                [1., 1., 0., 0.],
                [1., 0., 0., 0.]])

    """
    n_batch = len(xs)
    max_len = max([x.shape[0] for x in xs])
    pad = paddle.zeros(shape=[n_batch, max_len], dtype=xs[0].dtype)
    pad = pad.fill_(value=pad_value)
    for i in range(n_batch):
        pad[i, :xs[i].shape[0]] = xs[i]
    return pad


def add_sos_eos(ys_pad: paddle.Tensor, sos: int, eos: int, ignore_id: int) -> Tuple[paddle.Tensor, paddle.Tensor]:
    """Add <sos> and <eos> labels.

    Args:
        ys_pad (paddle.Tensor): batch of padded target sequences (B, Lmax)
        sos (int): index of <sos>
        eos (int): index of <eeos>
        ignore_id (int): index of padding

    Returns:
        ys_in (paddle.Tensor) : (B, Lmax + 1)
        ys_out (paddle.Tensor) : (B, Lmax + 1)

    Examples:
        >>> sos_id = 10
        >>> eos_id = 11
        >>> ignore_id = -1
        >>> ys_pad
        tensor([[ 1,  2,  3,  4,  5],
                [ 4,  5,  6, -1, -1],
                [ 7,  8,  9, -1, -1]], dtype=paddle.int32)
        >>> ys_in,ys_out=add_sos_eos(ys_pad, sos_id , eos_id, ignore_id)
        >>> ys_in
        tensor([[10,  1,  2,  3,  4,  5],
                [10,  4,  5,  6, 11, 11],
                [10,  7,  8,  9, 11, 11]])
        >>> ys_out
        tensor([[ 1,  2,  3,  4,  5, 11],
                [ 4,  5,  6, 11, -1, -1],
                [ 7,  8,  9, 11, -1, -1]])
    """
    _sos = paddle.to_tensor(data=[sos], dtype=ys_pad.dtype, place=ys_pad.place, stop_gradient=True)
    _eos = paddle.to_tensor(data=[eos], dtype=ys_pad.dtype, place=ys_pad.place, stop_gradient=True)
    ys = [y[y != ignore_id] for y in ys_pad]
    ys_in = [paddle.concat(x=[_sos, y], axis=0) for y in ys]
    ys_out = [paddle.concat(x=[y, _eos], axis=0) for y in ys]
    return pad_list(ys_in, eos), pad_list(ys_out, ignore_id)


def th_accuracy(pad_outputs: paddle.Tensor,
                pad_targets: paddle.Tensor,
                ignore_label: int) -> float:
    """Calculate accuracy.
    Args:
        pad_outputs (Tensor): Prediction tensors (B * Lmax, D).
        pad_targets (LongTensor): Target label tensors (B, Lmax, D).
        ignore_label (int): Ignore label id.
    Returns:
        float: Accuracy value (0.0 - 1.0).
    """
    pad_pred = pad_outputs.reshape([pad_targets.shape[0], pad_targets.shape[1], pad_outputs.shape[1]]).argmax(2)
    mask = pad_targets != ignore_label
    numerator = (pad_pred.masked_select(mask) == pad_targets.masked_select(mask))
    numerator = paddle.sum(numerator.astype(pad_targets.dtype))
    denominator = paddle.sum(mask.astype(pad_targets.dtype))
    return float(numerator) / float(denominator)


def reverse_pad_list(ys_pad: paddle.Tensor,
                     ys_lens: paddle.Tensor,
                     pad_value: float = -1.0) -> paddle.Tensor:
    """Reverse padding for the list of tensors.
    Args:
        ys_pad (tensor): The padded tensor (B, Tokenmax).
        ys_lens (tensor): The lens of token seqs (B)
        pad_value (int): Value for padding.
    Returns:
        Tensor: Padded tensor (B, Tokenmax).
    Examples:
        >>> x
        tensor([[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 0, 0]])
        >>> pad_list(x, 0)
        tensor([[4, 3, 2, 1],
                [7, 6, 5, 0],
                [9, 8, 0, 0]])
    """
    r_ys_pad = pad_sequence([(paddle.flip(y.astype(paddle.int32)[:i], [0]))
                             for y, i in zip(ys_pad, ys_lens)], True, pad_value)
    return r_ys_pad


def get_activation(act):
    """Return activation function."""
    # Lazy load to avoid unused import
    activation_funcs = {
        "hardshrink": paddle.nn.Hardshrink,
        "hardswish": paddle.nn.Hardswish,
        "hardtanh": paddle.nn.Hardtanh,
        "tanh": paddle.nn.Tanh,
        "relu": paddle.nn.ReLU,
        "relu6": paddle.nn.ReLU6,
        "leakyrelu": paddle.nn.LeakyReLU,
        "selu": paddle.nn.SELU,
        "swish": paddle.nn.Swish,
        "gelu": paddle.nn.GELU,
        "elu": paddle.nn.ELU,
    }

    return activation_funcs[act]()
