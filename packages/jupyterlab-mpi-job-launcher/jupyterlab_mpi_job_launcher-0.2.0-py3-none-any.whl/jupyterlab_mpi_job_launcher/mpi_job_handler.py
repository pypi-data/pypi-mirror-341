import json
from loguru import logger
import tornado
import tornado.web

import grpc
from .proto import service_pb2
from .proto import service_pb2_grpc

from jupyter_server.base.handlers import APIHandler

from .config import settings

GRPC_SERVER = settings.GRPC_SERVER
LOG_LEVEL = settings.LOG_LEVEL

IS_DEV = LOG_LEVEL == "DEBUG"

logger.remove()
logger.add(
    "mpi_job_handler.log",
    rotation="00:00",
    retention="7 days",
    compression="zip",
    level=LOG_LEVEL,
)

if IS_DEV:
    logger.add(lambda msg: print(msg, end=""), level=LOG_LEVEL)


# Refresh API Key handler
class MpiJobHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self):
        try:
            json_body = self.get_json_body()
            logger.info("Received request body: {}", json_body)

            # Validación del JSON recibido
            if json_body is None:
                raise ValueError("Request body is missing.")

            # Validar sección 'launcher'
            launcher = json_body.get("launcher")
            if launcher is None:
                raise ValueError("Launcher information is missing.")
            for field in ["cpu", "memory", "image", "command"]:
                if launcher.get(field) is None:
                    raise ValueError(f"Launcher parameter '{field}' is missing.")

            # Validar sección 'worker'
            worker = json_body.get("worker")
            if worker is None:
                raise ValueError("Worker information is missing.")
            for field in ["cpu", "memory", "image", "replicas"]:
                if worker.get(field) is None:
                    raise ValueError(f"Worker parameter '{field}' is missing.")

            # Construir el objeto payload con la nueva estructura
            json_payload = {
                "dry-run": True,
                "launcher": {
                    "cpu": launcher["cpu"],
                    "memory": launcher["memory"],
                    "image": launcher["image"],
                    "command": launcher["command"],
                },
                "worker": {
                    "cpu": worker["cpu"],
                    "memory": worker["memory"],
                    "image": worker["image"],
                    "replicas": worker["replicas"],
                },
            }

            logger.debug("Sending payload to GRPC_SERVER: {}", json_payload)
            with grpc.insecure_channel(GRPC_SERVER) as channel:
                stub = service_pb2_grpc.MPIJobServiceStub(channel)
                request = service_pb2.JobRequest(json_payload=json.dumps(json_payload))
                response = stub.SubmitJob(request)
                print("Response:", response.message)

            self.write({"message": response.message})

        except (ValueError, KeyError) as e:
            logger.error("Error en el cuerpo de la solicitud: {}", e)
            self.set_status(400)
            self.finish(json.dumps({"error": str(e)}))

        except Exception as e:
            logger.exception("Excepción no controlada en MpiJobHandler: {}", e)
            self.set_status(500)
            self.finish(json.dumps({"error": "Error interno del servidor."}))
