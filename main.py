import can
import time


from can.interfaces.zlgcan import ZCanBus
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import isotp


from zlgcan import ZCANDeviceType, ZCANCanTransType

# with can.Bus(bustype='zlgcan', device_type=ZCANDeviceType.ZCAN_USBCAN2, resend=True,
#              configs=[{'bitrate': 500000}]  # 2通道配置
#              ) as bus:
#     while True:
#         msg = can.Message(
#             arbitration_id=0x01,
#             is_extended_id=False,
#             channel=0,
#             data=[0x01, 0x02, 0x01, 0x02, 0x01, 0x02, 0x01, 0x02],
#             is_rx=False,
#         )
#         bus.send(msg, trans_type=ZCANCanTransType.NORMAL)
#         time.sleep(0.05)
#         print(bus.recv(1))



# Refer to isotp documentation for full details about parameters
isotp_params = {
   'stmin' : 32,                          # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
   'blocksize' : 8,                       # Request the sender to send 8 consecutives frames before sending a new flow control message
   'wftmax' : 0,                          # Number of wait frame allowed before triggering an error
   'tx_data_length' : 8,                  # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
   'tx_data_min_length' : None,           # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
   'tx_padding' : 0,                      # Will pad all transmitted CAN messages with byte 0x00.
   'rx_flowcontrol_timeout' : 1000,       # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
   'rx_consecutive_frame_timeout' : 1000, # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
   'squash_stmin_requirement' : False,    # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
   'max_frame_size' : 4095                # Limit the size of receive frame.
}


# from can.interfaces.vector import VectorBus
bus = ZCanBus(device_type=ZCANDeviceType.ZCAN_USBCAN2, configs=[{'bitrate': 500000}])                                          # Link Layer (CAN protocol)
tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x123, rxid=0x456) # Network layer addressing scheme
stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)               # Network/Transport layer (IsoTP protocol)
stack.set_sleep_timing(0, 0)                                                        # Speed First (do not sleep)
conn = PythonIsoTpConnection(stack)                                                 # interface between Application and Transport layer
with Client(conn, request_timeout=1) as client:                                     # Application layer (UDS1 protocol)
   client.change_session(1)
   # ...



