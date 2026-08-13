import os
import sys
import time
from concurrent import futures
import grpc

# Import des fichiers générés protobuf (ajoutés au path)
sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

import crypto_pb2
import crypto_pb2_grpc
from crypto_service import AESGCMCrypto

class CryptoServiceServicer(crypto_pb2_grpc.CryptoServiceServicer):
    def __init__(self):
        self.crypto = AESGCMCrypto()

    def Encrypt(self, request, context):
        try:
            cipher_b64, iv_b64 = self.crypto.encrypt(request.plain_text)
            return crypto_pb2.EncryptResponse(
                cipher_text_base64=cipher_b64,
                iv_base64=iv_b64
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Encryption error: {str(e)}")
            return crypto_pb2.EncryptResponse()

    def Decrypt(self, request, context):
        try:
            plain_text = self.crypto.decrypt(request.cipher_text_base64, request.iv_base64)
            return crypto_pb2.DecryptResponse(plain_text=plain_text)
        except Exception as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Decryption error: {str(e)}")
            return crypto_pb2.DecryptResponse()

def serve():
    port = os.getenv("GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crypto_pb2_grpc.add_CryptoServiceServicer_to_server(CryptoServiceServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    print(f"🚀 Serveur gRPC Crypto démarré sur le port {port}...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()