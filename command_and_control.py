import ecdsa
import os


class CommandAndControl:
    def create_signature(self, msg):
        # load or generate the ECDSA key pair
        if os.path.isfile("private.key"):
            # load the existing private key
            with open("private.key", "rb") as f:
                private_key_bytes = f.read()
            sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

        else:
            # generate a new ECDSA key pair
            sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            private_key_bytes = sk.to_string()

            # save the private key to a file
            with open("private.key", "wb") as f:
                f.write(private_key_bytes)

        # get the public key
        vk = sk.verifying_key

        # save public key to file
        with open('public_key.pem', 'wb') as f:
            f.write(vk.to_pem())  # PEM is the standard format for storing public keys

        # sign a message
        message = bytes(msg, "utf-8")
        signature = sk.sign_deterministic(message)
        print(signature)

        # verify the signature
        assert vk.verify(signature, message)

        return signature.hex()