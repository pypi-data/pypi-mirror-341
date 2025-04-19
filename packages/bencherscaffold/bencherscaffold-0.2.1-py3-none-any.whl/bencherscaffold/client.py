import time
from collections.abc import Sequence

import grpc

from bencherscaffold.protoclasses.bencher_pb2 import BenchmarkRequest, EvaluationResult
from bencherscaffold.protoclasses.bencher_pb2_grpc import BencherStub


class BencherClient:
    def __init__(
            self,
            hostname: str = '127.0.0.1',
            port: int = 50051,
            max_retries: int = 10,
            wait_time: int = 5,
    ):
        """
        Initializes the BencherClient with the given parameters.
        Args:
            hostname: The hostname of the server.
            port: The port number of the server.
            max_retries: The maximum number of retries for the request.
            wait_time: The time to wait between retries in seconds.
        """
        self.channel = grpc.insecure_channel(f"{hostname}:{port}")
        self.stub = BencherStub(self.channel)
        self.max_retries = max_retries
        self.wait_time = wait_time

    def evaluate_point(
            self,
            benchmark: str,
            point: Sequence[float],
    ) -> float:
        """
        Evaluates a point in the benchmark space.
        This method sends a request to the server to evaluate a specific point in the benchmark space.
        It retries the request if it fails, up to the maximum number of retries specified.
        If the request fails after the maximum number of retries, it raises the last exception encountered.
        The point must be a sequence of floats, and its length must match the number of dimensions of the benchmark.

        Args:
            benchmark: The name of the benchmark to evaluate.
            point:  A sequence of floats representing the point in the benchmark space to evaluate.

        Returns:
            The evaluated value of the point in the benchmark space.

        """
        request = BenchmarkRequest(
            benchmark=benchmark,
            point={'values': point}
        )
        for n_retry in range(self.max_retries):
            try:
                response: EvaluationResult = self.stub.evaluate_point(request)
                return response.value
            except grpc.RpcError as e:
                if n_retry < self.max_retries - 1:
                    print(f"Retrying... {n_retry + 1}/{self.max_retries}")
                    time.sleep(self.wait_time)
                else:
                    raise e
