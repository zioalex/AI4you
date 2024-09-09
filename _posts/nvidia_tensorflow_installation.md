# Install nvidia drivers
- find the last one in 
https://www.nvidia.com/download/index.aspx?lang=en-us

Or in ubuntu use: ???
Install latest driver version from Software and Updates # The drivers included are not the latest available from nvdida. See below
reboot

The instruction to install tesnsoflow and the nvidia drivers from Nvidia are partially outdated:
https://www.nvidia.com/en-sg/data-center/gpu-accelerated-applications/tensorflow/



# check thre required Cuda and cuDNN version in this table
https://www.tensorflow.org/install/source#gpu

In my case I have TF 2.13.0 and I need cuDNN 8.6	and CUDA 11.8

Get the latest version following the guide:
https://gist.github.com/MihailCosmin/affa6b1b71b43787e9228c25fe15aeba

Find here the proper OS repo and architecture https://developer.download.nvidia.com/compute/cuda/repos

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600 
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"

Version cuDNN 8.6        and CUDA 11.8
Doesn't work updating to the latest version

CUDA 12.5 and cudnn9-cuda-12-4
# Install cuda
apt install cuda

## Test cuda - not available with the latest CUDA Version 12.5
	cd /usr/local/cuda-8.0/samples/5_Simulations/nbody
	sudo make
	./nbody

# Test
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
	2024-06-01 01:23:56.483732: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
	To enable the following instructions: AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
	2024-06-01 01:23:57.035318: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
	2024-06-01 01:23:57.454869: I tensorflow/compiler/xla/stream_executor/cuda/cuda_gpu_executor.cc:995] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero. See more at https://github.com/torvalds/linux/blob/v6.0/Documentation/ABI/testing/sysfs-bus-pci#L344-L355
	2024-06-01 01:23:57.477203: I tensorflow/compiler/xla/stream_executor/cuda/cuda_gpu_executor.cc:995] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero. See more at https://github.com/torvalds/linux/blob/v6.0/Documentation/ABI/testing/sysfs-bus-pci#L344-L355
	2024-06-01 01:23:57.477386: I tensorflow/compiler/xla/stream_executor/cuda/cuda_gpu_executor.cc:995] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero. See more at https://github.com/torvalds/linux/blob/v6.0/Documentation/ABI/testing/sysfs-bus-pci#L344-L355
	[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]


Another test
https://stackoverflow.com/questions/61178521/what-is-the-proper-way-to-benchmark-part-of-tensorflow-graph/63591009#63591009

import tensorflow as tf

tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)

import os
import time

import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

np.random.seed(2020)



def conv_block(x, kernel_size=3):
    # Define some part of graph here

    bs, h, w, c = x.shape
    in_channels = c
    out_channels = c

    with tf.compat.v1.variable_scope('var_scope'):
        w_0 = tf.compat.v1.get_variable('w_0', [kernel_size, kernel_size, in_channels, out_channels], initializer=tf.keras.initializers.glorot_normal())
        x = tf.nn.conv2d(x, w_0, [1, 1, 1, 1], 'SAME')

    return x


def get_data_batch(spatial_size, n_channels):
    bs = 1
    h = spatial_size
    w = spatial_size
    c = n_channels

    x_np = np.random.rand(bs, h, w, c)
    x_np = x_np.astype(np.float32)
    #print('x_np.shape', x_np.shape)

    return x_np


def run_graph_part(f_name, spatial_size, n_channels, n_iter=100):
    print('=' * 60)
    print(f_name.__name__)

#     tf.reset_default_graph()
    tf.compat.v1.reset_default_graph()
    
    
    with tf.compat.v1.Session() as sess:
        x_tf = tf.compat.v1.placeholder(tf.float32, [1, spatial_size, spatial_size, n_channels], name='input')
        z_tf = f_name(x_tf)
        
        sess.run(tf.compat.v1.global_variables_initializer())

        x_np = get_data_batch(spatial_size, n_channels)
        
        start_time = time.time()
        
        for _ in range(n_iter):
            z_np = sess.run(fetches=[z_tf], feed_dict={x_tf: x_np})[0]
        avr_time = (time.time() - start_time) / n_iter
        
        print('z_np.shape', z_np.shape)
        print('avr_time', round(avr_time, 3))

        n_total_params = 0
        
        for v in tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES, scope='var_scope'):
            n_total_params += np.prod(v.get_shape().as_list())
        
        print('Number of parameters:', format(n_total_params, ',d'))

        # USING TENSORFLOW BENCHMARK
        benchmark = tf.test.Benchmark()
        results = benchmark.run_op_benchmark(sess=sess, op_or_tensor=z_tf, 
                                             feed_dict={x_tf: x_np}, burn_iters=2, min_iters=n_iter,
                                             store_memory_usage=False, name='example')

        return results


if __name__ == '__main__':
    results = run_graph_part(conv_block, spatial_size=512, n_channels=32, n_iter=100)

2024-06-01 02:10:08.232720: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1639] Created device /job:localhost/replica:0/task:0/device:GPU:0 with
 4703 MB memory:  -> device: 0, name: NVIDIA GeForce RTX 2070 SUPER, pci bus id: 0000:09:00.0, compute capability: 7.5
2024-06-01 02:10:08.247904: I tensorflow/compiler/mlir/mlir_graph_optimization_pass.cc:375] MLIR V1 optimization pass is not enabled
2024-06-01 02:10:08.351612: I tensorflow/compiler/xla/stream_executor/cuda/cuda_dnn.cc:432] Loaded cuDNN version 8907
2024-06-01 02:10:08.411724: E tensorflow/compiler/xla/stream_executor/gpu/asm_compiler.cc:114] *** WARNING *** You are using ptxas 11.0.221, which is
 older than 11.1. ptxas before 11.1 is known to miscompile XLA code, leading to incorrect results or invalid-address errors.

z_np.shape (1, 512, 512, 32)
avr_time 0.022
Number of parameters: 9,216
entry {
  name: "TensorFlowBenchmark.example" 
  iters: 100
  wall_time: 0.01595771312713623
}




https://medium.com/nerd-for-tech/installing-tensorflow-with-gpu-acceleration-on-linux-f3f55dd15a9


