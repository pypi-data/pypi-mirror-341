"""
    QApp Platform Project ibm_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import transpile

from qiskit_ibm_runtime import SamplerV2 as Sampler

from qapp_common.data.device.circuit_running_option import CircuitRunningOption
from qapp_common.config.logging_config import logger

from .qiskit_device import QiskitDevice


class IbmQuantumDevice(QiskitDevice):

    def _is_simulator(self) -> bool:
        logger.debug('[IbmQuantumDevice] _is_simulator()')

        return self.device.configuration().simulator

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug('[IbmQuantumDevice] _create_job() with {0} shots'.format(options.shots))

        transpiled_circuit = transpile(circuits=circuit, backend=self.device)

        sampler = Sampler(self.device)

        return sampler.run([transpiled_circuit], shots=options.shots)
