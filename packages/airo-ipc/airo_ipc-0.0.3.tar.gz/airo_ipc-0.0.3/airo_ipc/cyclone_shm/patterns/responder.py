import time
from threading import Thread
from typing import AnyStr, Callable, Type

from cyclonedds.domain import DomainParticipant
from cyclonedds.internal import InvalidSample
from cyclonedds.pub import DataWriter
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from loguru import logger

from airo_ipc.cyclone_shm.defaults import CYCLONE_DEFAULTS
from airo_ipc.cyclone_shm.idl.defaults.rpc_idl import RPCIdl
from airo_ipc.cyclone_shm.idl.defaults.rpc_status_idl import RPCStatus


class Responder:
    def __init__(
            self,
            domain_participant: DomainParticipant,
            rpc_name: AnyStr,
            idl_dataclass: Type[RPCIdl],
            callback: Callable[[RPCIdl.Request], RPCIdl.Response],
    ):
        self.participant = domain_participant
        self.callback = callback
        self.status_responder = self.__initialize_status_responder(rpc_name)

        self.request_topic = Topic(
            self.participant,
            f"{rpc_name}_request",
            idl_dataclass.Request,
            qos=CYCLONE_DEFAULTS.QOS_RPC,
        )
        self.response_topic = Topic(
            self.participant,
            f"{rpc_name}_response",
            idl_dataclass.Response,
            qos=CYCLONE_DEFAULTS.QOS_RPC,
        )

        # Initialize DDS reader and writer
        self.reader = DataReader(
            self.participant, self.request_topic, qos=CYCLONE_DEFAULTS.QOS_RPC
        )
        self.writer = DataWriter(
            self.participant, self.response_topic, qos=CYCLONE_DEFAULTS.QOS_RPC
        )

        # Start the thread to continuously listen for requests
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()
        time.sleep(0.1)

        logger.info(f'RPC Responder "{rpc_name}" active.')

    def __initialize_status_responder(self, rpc_name: AnyStr) -> Thread:
        def respond_to_status_requests():
            # Define topics for status request/response
            status_request_topic = Topic(
                self.participant,
                f"{rpc_name}_status_request",
                RPCStatus.Request,
                CYCLONE_DEFAULTS.QOS_RPC_STATUS,
            )
            status_response_topic = Topic(
                self.participant,
                f"{rpc_name}_status_response",
                RPCStatus.Response,
                CYCLONE_DEFAULTS.QOS_RPC_STATUS,
            )

            # Initialize reader and writer
            status_reader = DataReader(self.participant, status_request_topic)
            status_writer = DataWriter(self.participant, status_response_topic)

            while True:
                request = status_reader.take()
                if len(request):
                    response = RPCStatus.Response(timestamp=time.time())
                    status_writer.write(response)
                time.sleep(0.1)

        status_responder_thread = Thread(target=respond_to_status_requests)
        status_responder_thread.daemon = True
        status_responder_thread.start()

        time.sleep(0.1)  # Avoids segmentation faults while initializing DDS components
        return status_responder_thread

    def run(self):
        while True:
            try:
                samples = self.reader.take()
                for request in samples:
                    if isinstance(request, InvalidSample):
                        continue
                    response = self.callback(request)
                    response.timestamp = request.timestamp
                    self.writer.write(response)
            except IndexError:
                pass
            time.sleep(0.01)
