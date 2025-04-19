import os

import numpy as np
import paddle.inference as paddle_infer
from loguru import logger


class DecoderPredictor:
    def __init__(self,
                 model_dir,
                 use_gpu=True,
                 use_tensorrt=False,
                 gpu_mem=1000,
                 num_threads=10):
        """
        语音识别预测工具
        :param configs: 配置参数
        :param use_model: 使用模型的名称
        :param use_model: 是否为流式模型
        :param model_dir: 导出的预测模型文件夹路径
        :param use_gpu: 是否使用GPU预测
        :param gpu_mem: 预先分配的GPU显存大小
        :param num_threads: 只用CPU预测的线程数量
        """
        # 创建 config
        model_path = os.path.join(model_dir, 'decoder.pdmodel')
        params_path = os.path.join(model_dir, 'decoder.pdiparams')
        if not os.path.exists(model_path) or not os.path.exists(params_path):
            raise Exception("模型文件不存在，请检查%s和%s是否存在！" % (model_path, params_path))
        config = paddle_infer.Config(model_path, params_path)

        if use_gpu:
            config.enable_use_gpu(gpu_mem, 0)
            # 是否使用TensorRT
            if use_tensorrt:
                shape_file = f"{model_dir}/shape_range_info.pbtxt"
                if not os.path.exists(shape_file):
                    config.collect_shape_range_info(shape_file)
                config.enable_tensorrt_engine(workspace_size=1 << 30,
                                              max_batch_size=1,
                                              min_subgraph_size=3,
                                              precision_mode=paddle_infer.PrecisionType.Float32,
                                              use_static=False,
                                              use_calib_mode=False)
                if os.path.exists(shape_file):
                    config.enable_tuned_tensorrt_dynamic_shape(shape_file, True)
                config.exp_disable_tensorrt_ops(["Concat", "reshape2"])
        else:
            config.disable_gpu()
            # 存在精度损失问题
            # config.enable_mkldnn()
            # config.set_mkldnn_cache_capacity(1)
            config.set_cpu_math_library_num_threads(num_threads)
        config.disable_glog_info()
        # enable memory optim
        config.enable_memory_optim()
        config.switch_ir_optim(True)
        config.switch_use_feed_fetch_ops(False)

        # 根据 config 创建 predictor
        self.predictor = paddle_infer.create_predictor(config)
        logger.info(f'已加载模型：{model_path}')

        # 获取输入层
        self.hyps_handle = self.predictor.get_input_handle('hyps')
        self.hyps_lens_handle = self.predictor.get_input_handle('hyps_lens')
        self.encoder_out_handle = self.predictor.get_input_handle('encoder_out')
        self.reverse_weight_handle = self.predictor.get_input_handle('reverse_weight')
        # 获取输出的名称
        self.output_names = self.predictor.get_output_names()

    # 执行语言模型推理
    def predict(self, hyps, hyps_lens, encoder_out, reverse_weight):
        """
        :param hyps: 前缀搜索解码候选结果
        :param hyps_lens: 前缀搜索解码候选结果的长度
        :param encoder_out: 编码器输出
        :param reverse_weight: 逆向权重
        :return: 识别的文本结果和解码的得分数
        """
        if not isinstance(hyps, np.ndarray):
            hyps = hyps.numpy()
        if not isinstance(hyps_lens, np.ndarray):
            hyps_lens = hyps_lens.numpy()
        if not isinstance(reverse_weight, np.ndarray):
            reverse_weight = np.array([reverse_weight]).astype(np.float32)
        # 设置输入
        self.hyps_handle.reshape([hyps.shape[0], hyps.shape[1]])
        self.hyps_handle.copy_from_cpu(hyps)
        self.hyps_lens_handle.reshape([hyps_lens.shape[0]])
        self.hyps_lens_handle.copy_from_cpu(hyps_lens)
        self.encoder_out_handle.reshape([encoder_out.shape[0], encoder_out.shape[1], encoder_out.shape[2]])
        self.encoder_out_handle.copy_from_cpu(encoder_out)
        self.reverse_weight_handle.reshape([1])
        self.reverse_weight_handle.copy_from_cpu(reverse_weight)

        # 运行predictor
        self.predictor.run()

        # 获取输出
        decoder_out_handle = self.predictor.get_output_handle(self.output_names[0])
        decoder_out_data = decoder_out_handle.copy_to_cpu()
        r_decoder_out_handle = self.predictor.get_output_handle(self.output_names[1])
        r_decoder_out_data = r_decoder_out_handle.copy_to_cpu()
        return decoder_out_data, r_decoder_out_data
