import logging
import websockets
import asyncio
import json
import gzip
import config
import proto.protocol_pb2 as protocol
import proto.response_pb2 as response
import proto.astro_pb2 as astro
import proto.system_pb2 as system

import lib.my_logger as my_logger

def ws_uri(dwarf_ip):
    return f"ws://{dwarf_ip}:9900"

class StopClientException(Exception):
    pass

# new version protobuf enabled
# use a Class
class WebSocketClient:
    def __init__(self, uri, client_id, message, command, type_id, module_id, ping_interval=5):
        self.websocket = False
        self.result = False
        self.uri = uri
        self.message = message
        self.command = command
        self.type_id = type_id
        self.module_id = module_id
        self.client_id = client_id
        self.ping_interval = ping_interval
        self.ping_task = None
        self.receive_task = None
        self.stop_task = asyncio.Event()
        self.wait_pong = False

        # TEST_CALIBRATION : Test Calibration Packet or Goto Packet
        # Test Mode : Calibration Packet => TEST_CALIBRATION = True
        # Production Mode GOTO Packet => TEST_CALIBRATION = False (default)
        self.modeCalibration = False

        if hasattr(config, 'TEST_CALIBRATION'):
            if(config.TEST_CALIBRATION):
                self.modeCalibration = True

    async def abort_tasks_timeout(self, timeout):

        try:
            count = 0
            await asyncio.sleep(0.02)
            while not self.stop_task.is_set() and count < timeout:
                await asyncio.sleep(1)
                count += 1
        except Exception as e:
            # Handle other exceptions
            print(f"Timeout: Unhandled exception: {e}")
        finally:
            # Perform cleanup if needed
            if (not self.stop_task.is_set()):
                self.stop_task.set()
            await asyncio.sleep(0.02)
            print("TERMINATING TIMEOUT function.")

    async def send_ping_periodically(self):
        if not self.websocket:
            print("Error No WebSocket in send_ping_periodically")
            self.stop_task.set()

        try:
            await asyncio.sleep(2)
            while not self.stop_task.is_set():
                if self.websocket.state != websockets.protocol.OPEN:
                    print("WebSocket connection is not open.")
                    self.stop_task.set()
                else:
                    # Adjust the interval based on your requirements
                    print("Sent a PING frame")

                    await self.websocket.ping()
                    await self.websocket.send("ping")
                    # Signal to Receive to Wait the Pong Frame
                    self.wait_pong = True
                    await asyncio.sleep(self.ping_interval)
            await asyncio.sleep(0.02)

        except websockets.ConnectionClosedOK as e:
            print(f'Ping: ConnectionClosedOK', e)
        except websockets.ConnectionClosedError as e:
            print(f'Ping: ConnectionClosedError', e)
        except asyncio.CancelledError:
            print("Ping Cancelled.")
        except Exception as e:
            # Handle other exceptions
            print(f"Ping: Unhandled exception: {e}")
            if (not self.stop_task.is_set()):
                self.stop_task.set()
            await asyncio.sleep(1)
        finally:
            # Perform cleanup if needed
            print("TERMINATING PING function.")

    async def receive_messages(self):
        if not self.websocket:
            print("Error No WebSocket in receive_messages")
            self.stop_task.set()

        try:
            await asyncio.sleep(2)
            while not self.stop_task.is_set() or self.wait_pong:
                await asyncio.sleep(0.02)
                print("Wait for frames")

                if self.websocket.state != websockets.protocol.OPEN:
                    print("WebSocket connection is not open.")
                    self.wait_pong = False
                    self.stop_task.set()
                else:
                    message = await self.websocket.recv()
                    if (message):
                        if isinstance(message, str):
                            print("Receiving...")
                            print(message)
                            if (message =="pong"):
                                 self.wait_pong = False
                        elif isinstance(message, bytes):
                            print("Receiving...  data")
                            WsPacket_message = protocol.WsPacket()
                            WsPacket_message.ParseFromString(message)
                            my_logger.debug("receive cmd >>", WsPacket_message.cmd)
                            my_logger.debug("receive type >>", WsPacket_message.type)

                            # CMD_NOTIFY_WS_HOST_SLAVE_MODE = 15223; // Leader/follower mode notification
                            if (WsPacket_message.cmd==astro.CMD_NOTIFY_WS_HOST_SLAVE_MODE):
                                ResNotifyHostSlaveMode_message = response.ResNotifyHostSlaveMode()
                                ResNotifyHostSlaveMode_message.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_NOTIFY_WS_HOST_SLAVE_MODE")
                                my_logger.debug("receive Host/Slave data >>", ResNotifyHostSlaveMode_message.mode)

                                # Host = 0 Slave = 1
                                if (ResNotifyHostSlaveMode_message.mode == 1):
                                    my_logger.debug("SLAVE_MODE >> EXIT")
                                    # Signal the ping and receive functions to stop
                                    self.stop_task.set()
                                    self.result = "Error SLAVE MODE"
                                    await asyncio.sleep(5)
                                    print("Error SLAVE MODE detected")
                                else:
                                    print("Continue Decoding CMD_NOTIFY_WS_HOST_SLAVE_MODE")

                            # CMD_NOTIFY_STATE_ASTRO_CALIBRATION = 15210; // Astronomical calibration status
                            if (WsPacket_message.cmd==astro.CMD_NOTIFY_STATE_ASTRO_CALIBRATION):
                                ResNotifyStateAstroGoto_message = response.ResNotifyStateAstroCalibration()
                                ResNotifyStateAstroGoto_message.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_NOTIFY_STATE_ASTRO_CALIBRATION")
                                my_logger.debug("receive notification data >>", ResNotifyStateAstroGoto_message.state)
                                my_logger.debug("receive notification times >>", ResNotifyStateAstroGoto_message.plate_solving_times)

                                # ASTRO_STATE_IDLE = 0; // Idle state Only when Success
                                if (ResNotifyStateAstroGoto_message.state == response.ASTRO_STATE_IDLE):
                                    my_logger.debug("ASTRO CALIBRATION OK >> EXIT")
                                    # Signal the ping and receive functions to stop
                                    self.stop_task.set()
                                    self.result = "ok"
                                    await asyncio.sleep(5)
                                    print("Success ASTRO CALIBRATION OK")
                                else:
                                    print("Continue Decoding CMD_NOTIFY_STATE_ASTRO_CALIBRATION")

                            # CMD_NOTIFY_STATE_ASTRO_GOTO = 15211; // Astronomical GOTO status
                            elif (WsPacket_message.cmd==astro.CMD_NOTIFY_STATE_ASTRO_GOTO):
                                ResNotifyStateAstroGoto_message = response.ResNotifyStateAstroGoto()
                                ResNotifyStateAstroGoto_message.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_NOTIFY_STATE_ASTRO_GOTO")
                                my_logger.debug("receive notification data >>", ResNotifyStateAstroGoto_message.state)

                            # CMD_NOTIFY_STATE_ASTRO_TRACKING = 15212; // Astronomical tracking status
                            elif (WsPacket_message.cmd==astro.CMD_NOTIFY_STATE_ASTRO_TRACKING):
                                ResNotifyStateAstroGoto_message = response.ResNotifyStateAstroTracking()
                                ResNotifyStateAstroGoto_message.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_NOTIFY_STATE_ASTRO_TRACKING")
                                my_logger.debug("receive notification data >>", ResNotifyStateAstroGoto_message.state)
                                my_logger.debug("receive notification target_name >>", ResNotifyStateAstroGoto_message.target_name)

                                # ASTRO_STATE_RUNNING = 1; // Running
                                if (ResNotifyStateAstroGoto_message.state == response.ASTRO_STATE_RUNNING):
                                    my_logger.debug("ASTRO GOTO OK TRACKING >> EXIT")
                                    # Signal the ping and receive functions to stop
                                    self.stop_task.set()
                                    self.result = "ok"
                                    await asyncio.sleep(5)
                                    print("Success ASTRO GOTO TRACKING START")

                            # CMD_ASTRO_START_CALIBRATION = 11000; // Start calibration
                            elif (WsPacket_message.cmd==astro.CMD_ASTRO_START_CALIBRATION):
                                ComResponse = response.ComResponse()
                                ComResponse.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_ASTRO_START_CALIBRATION")
                                my_logger.debug("receive code data >>", ComResponse.code)

                                # CODE_ASTRO_CALIBRATION_FAILED = -11504; // Calibration failed
                                if (ComResponse.code == -11504):
                                    my_logger.debug("Error CALIBRATION >> EXIT")
                                    # Signal the ping and receive functions to stop
                                    self.stop_task.set()
                                    self.result = response.CODE_ASTRO_CALIBRATION_FAILED
                                    await asyncio.sleep(5)
                                    print("Error CALIBRATION CODE_ASTRO_CALIBRATION_FAILED")

                            # CMD_SYSTEM_SET_TIME = 13000; // Set the system time
                            elif (WsPacket_message.cmd==astro.CMD_SYSTEM_SET_TIME):
                                ComResponse = response.ComResponse()
                                ComResponse.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_SYSTEM_SET_TIME")
                                my_logger.debug("receive code data >>", ComResponse.code)

                                # Signal the ping and receive functions to stop
                                self.stop_task.set()
                                self.result = ComResponse.code
                                await asyncio.sleep(5)
                                if (ComResponse.code == response.CODE_SYSTEM_SET_TIME_FAILED):
                                    print("Error CMD_SYSTEM_SET_TIME")
                                else:
                                    print("OK CMD_SYSTEM_SET_TIME")

                            # CMD_SYSTEM_SET_TIME_ZONE = 13001; // Set the time zone
                            elif (WsPacket_message.cmd==astro.CMD_SYSTEM_SET_TIME_ZONE):
                                ComResponse = response.ComResponse()
                                ComResponse.ParseFromString(WsPacket_message.data)

                                print("Decoding CMD_SYSTEM_SET_TIME_ZONE")
                                my_logger.debug("receive code data >>", ComResponse.code)

                                # Signal the ping and receive functions to stop
                                self.stop_task.set()
                                self.result = ComResponse.code
                                await asyncio.sleep(5)
                                if (ComResponse.code == response.CODE_SYSTEM_SET_TIMEZONE_FAILED):
                                    print("Error CMD_SYSTEM_SET_TIME_ZONE")
                                else:
                                    print("OK CMD_SYSTEM_SET_TIME_ZONE")

                            elif (WsPacket_message.cmd != self.command):
                                if( WsPacket_message.type == 2):
                                    print("Decoding Other Notification Frame")
                                    ResNotifyStateAstroGoto_message = response.ResNotifyStateAstroGoto()
                                    ResNotifyStateAstroGoto_message.ParseFromString(WsPacket_message.data)

                                    my_logger.debug("receive notification data >>", ResNotifyStateAstroGoto_message.state)
                                if( WsPacket_message.type == 3):
                                    print("Decoding Other Notification Frame")
                                    ResNotifyStateAstroGoto_message = response.ResNotifyStateAstroGoto()
                                    ResNotifyStateAstroGoto_message.ParseFromString(WsPacket_message.data)

                                    my_logger.debug("receive notification data >>", ResNotifyStateAstroGoto_message.state)
                            else:
                                print("Decoding CMD_ASTRO_START_GOTO_DSO")
                                ComResponse_message = response.ComResponse()
                                ComResponse_message.ParseFromString(WsPacket_message.data)

                                my_logger.debug("receive type >>", WsPacket_message.type)
                                my_logger.debug("receive data >>", ComResponse_message.code)

                                if (ComResponse_message.code != response.NO_ERROR):
                                    my_logger.debug(f"Error GOTO {ComResponse_message.code} >> EXIT")
                                    # Signal the ping and receive functions to stop
                                    self.stop_task.set()
                                    self.result = ComResponse_message.code
                                    await asyncio.sleep(5)
                                    if (ComResponse_message.code == response.CODE_ASTRO_GOTO_FAILED):
                                        print("Error GOTO CODE_ASTRO_GOTO_FAILED")
                                    elif (ComResponse_message.code == response.CODE_STEP_MOTOR_LIMIT_POSITION_WARNING):
                                        print("Error GOTO CODE_STEP_MOTOR_LIMIT_POSITION_WARNING")
                                    elif (ComResponse_message.code == response.CODE_STEP_MOTOR_LIMIT_POSITION_HITTED):
                                        print("Error GOTO CODE_STEP_MOTOR_LIMIT_POSITION_HITTED")
                                    else:
                                        print("Error GOTO CODE " + ComResponse_message.code)
                        else:
                            print("Ignoring Unkown Type Frames")
                    else:
                        print("No Messages Rcv : close ??")
                        self.wait_pong = False
                        self.stop_task.set()
                print("Continue .....")

        except websockets.ConnectionClosedOK  as e:
            print(f'Rcv: ConnectionClosedOK', e)
        except websockets.ConnectionClosedError as e:
            print(f'Rcv: ConnectionClosedError', e)
        except asyncio.CancelledError:
            print("Rcv Cancelled.")
        except Exception as e:
            # Handle other exceptions
            print(f"Rcv: Unhandled exception: {e}")
            if (not self.stop_task.is_set()):
                self.stop_task.set()
            await asyncio.sleep(1)
        finally:
            # Perform cleanup if needed
            print("TERMINATING Receive function.")

    async def send_message(self):
        # Create a protobuf message
        # Start Sending
        major_version = 1
        minor_version = 1
        device_id = 1  # DWARF II

        if not self.websocket:
            print("Error No WebSocket in send_message")
            return

        # SEND COMMAND
        WsPacket_message = protocol.WsPacket()
        WsPacket_message.data = self.message.SerializeToString()

        WsPacket_message.major_version = major_version
        WsPacket_message.minor_version = minor_version
        WsPacket_message.device_id = device_id
        WsPacket_message.module_id = self.module_id
        WsPacket_message.cmd = self.command 
        WsPacket_message.type = self.type_id;
        WsPacket_message.client_id = self.client_id # "0000DAF2-0000-1000-8000-00805F9B34FB"  # ff03aa11-5994-4857-a872-b411e8a3a5e51
       
        try:
            # Serialize the message to bytes and send
            # Send Command
            await asyncio.sleep(0.02)

            await self.websocket.send(WsPacket_message.SerializeToString())
            my_logger.debug("Send cmd >>", WsPacket_message.cmd)
            my_logger.debug("Send type >>", WsPacket_message.type)
            my_logger.debug("Send message >>", self.message)

            print("Sendind End ....");  

        except Exception as e:
            # Handle other exceptions
            print(f"Unhandled exception1: {e}")
        finally:
            # Perform cleanup if needed
            print("TERMINATING Sending function.")

    async def start(self):
        try:
            result = False  
            #asyncio.set_event_loop(asyncio.new_event_loop())
            ping_timeout=self.ping_interval+2
            print(f"ping_interval : {self.ping_interval}")
            start_client = False
            self.stop_task.clear();
            async with websockets.connect(self.uri, ping_interval=None, extra_headers=[("Accept-Encoding", "gzip"), ("Sec-WebSocket-Extensions", "permessage-deflate")]) as websocket:
                try:
                    start_client = True
                    self.websocket = websocket
                    if self.websocket:
                        print(f"Connected to {self.uri} with {self.message} command:{self.command}")


                    # Start the task to receive messages
                    #self.receive_task = asyncio.ensure_future(self.receive_messages())
                    self.receive_task = asyncio.create_task(self.receive_messages())

                    # Start the periodic task to send pings
                    #self.ping_task = asyncio.ensure_future(self.send_ping_periodically())
                    self.ping_task = asyncio.create_task(self.send_ping_periodically())

                    # Start the periodic task to abort all task after timeout
                    self.abort_tasks_timeout = asyncio.create_task(self.abort_tasks_timeout(90))

                    await asyncio.sleep(2)

                    # Send a unique message to the server
                    try:
                        await self.send_message()

                        # For python 11
                        #async with asyncio.TaskGroup() as tg:
                        #    self.receive_task = tg.create_task(self.receive_messages())
                        #    self.ping_task = tg.create_task(self.send_ping_periodically())

                        #print(f"Both tasks have completed now: {self.receive_task.result()}, {self.ping_task.result()}")

                        results = await asyncio.gather( 
                            self.receive_task,
                            self.ping_task,
                            self.abort_tasks_timeout,
                            return_exceptions=True
                        ) 
                        print(results)
                        print("End of Current Tasks.")

                        # get the exception #raised by a task

                        try:
                            self.receive_task.result()
                            self.ping_task.result()

                        except Exception as e:
                            print(f"Exception occurred in the Gather try block: {e}")

                        print("End of Current Tasks Results.")

                    except Exception as e:
                        print(f"Exception occurred in the try block: {e}")

                except Exception as e:
                    print(f"Exception occurred in the 2nd try block: {e}")
        except Exception as e:
            print(f"unknown exception with error: {e}")
        finally:
            # Signal the ping and receive functions to stop
            self.stop_task.set()

            # Cancel the ping task when the client is done
            if self.ping_task:
                print("Closing Ping Task ....")
                self.ping_task.cancel()
                try:
                    await self.ping_task
                except Exception as e:
                    print(f"unknown exception with error: {e}")

            # Cancel the receive task when the client is done
            if self.receive_task:
                print("Closing Receive Task ....")
                self.receive_task.cancel()
                try:
                    await self.receive_task
                except Exception as e:
                    print(f"unknown exception with error: {e}")

            # Close the WebSocket connection explicitly
            if start_client:
                if self.websocket: #and self.websocket.open:
                    print("Closing Socket ....")
                    try:
                        await self.websocket.close()
                        print("WebSocket connection closed.")
                    except websockets.ConnectionClosedOK  as e:
                        print(f'Close: ConnectionClosedOK', e)
                    except websockets.ConnectionClosedError as e:
                        print(f'Close: ConnectionClosedError', e)
                    except Exception as e:
                        print(f"unknown exception with error: {e}")

                print("WebSocket Terminated.")

# Run the client
def start_socket(message, command, type_id, module_id, uri=config.DWARF_IP, client_id=config.CLIENT_ID, ping_interval=10):
    websocket_uri = ws_uri(uri)

    print(f"Try Connect to {websocket_uri} for {client_id} with:")
    print(f"{message}")
    print(f"command:{command}")

    try:
        # Create an instance of WebSocketClient
        client_instance = WebSocketClient(websocket_uri, client_id, message, command, type_id, module_id, ping_interval)

        # Call the start method to initiate the WebSocket connection and tasks
        asyncio.run(client_instance.start())
        print("WebSocket Client End.")
        return client_instance.result;

    except Exception as e:
        # Handle any errors that may occur during the close operation
        print(f"Unknown Error closing : {e}")
        pass  # Ignore this exception, it's expected during clean-up

    return False;

def connect_socket(message, command, type_id, module_id):

    result = False

    try:
        # Call the start function
        result = start_socket(message, command, type_id, module_id)
        print(f"Result : {result}")

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt separately
        print("KeyboardInterrupt received. Stopping gracefully.")
        pass  # Ignore this exception, it's expected during clean-up
    return result

