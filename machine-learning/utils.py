import tensorflow as tf


def setup_gpu_memory():
    # there are 2 GPUs with 32GB mem each on groucho. Need to set memory limit to 30G for each to avoid
    # running exceptions
    tf.config.experimental.set_memory_growth = True
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if len(gpus) == 2:
      try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
        tf.config.experimental.set_virtual_device_configuration(
            gpus[1],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024*30)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
      except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)

