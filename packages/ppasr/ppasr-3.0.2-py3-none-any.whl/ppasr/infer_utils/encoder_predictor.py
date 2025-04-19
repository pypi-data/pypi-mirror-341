import os

import paddle.inference as paddle_infer
from loguru import logger


class EncoderPredictor:
    def __init__(self,
                 model_dir,
                 use_gpu=True,
                 use_tensorrt=False,
                 gpu_mem=1000,
                 num_threads=10):
        """
        语音识别预测工具
        :param model_dir: 导出的预测模型文件夹路径
        :param use_gpu: 是否使用GPU预测
        :param use_tensorrt: 是否使用TensorRT预测
        :param gpu_mem: 预先分配的GPU显存大小
        :param num_threads: 只用CPU预测的线程数量
        """
        # 创建 config
        model_path = os.path.join(model_dir, 'encoder.pdmodel')
        params_path = os.path.join(model_dir, 'encoder.pdiparams')
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
        self.speech_data_handle = self.predictor.get_input_handle('speech')
        self.speech_lengths_handle = self.predictor.get_input_handle('speech_lengths')

        # 获取输出的名称
        self.output_names = self.predictor.get_output_names()

    # 预测音频
    def predict(self, speech, speech_lengths):
        """
        预测函数，只预测完整的一句话。
        :param speech: 经过处理的音频数据
        :param speech_lengths: 音频长度
        :return: 识别的文本结果和解码的得分数
        """
        # 设置输入
        self.speech_data_handle.reshape([speech.shape[0], speech.shape[1], speech.shape[2]])
        self.speech_data_handle.copy_from_cpu(speech)
        self.speech_lengths_handle.reshape([speech.shape[0]])
        self.speech_lengths_handle.copy_from_cpu(speech_lengths)

        # 运行predictor
        self.predictor.run()

        # 获取输出
        outputs = []
        for name in self.output_names:
            output_handle = self.predictor.get_output_handle(name)
            output_data = output_handle.copy_to_cpu()
            outputs.append(output_data)
        return outputs
