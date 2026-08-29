import double_crunch_marketplace as dc
import os

input_file = "SaveClip.App_AQNi8EMLn5F4Gp-h1VNqbQXxUm0PFOT3kjcgbRUV5ai4-bwm54VaHkSFkT6u2YtRTQZjI7HRxn7VZPFEIrluejp2.mp4.cdv6"
output_file = "test_gui_restored.mp4"
try:
    dc.iterative_decompress(os.path.abspath(input_file), os.path.abspath(output_file))
except Exception as e:
    print("CRASHED:", e)
