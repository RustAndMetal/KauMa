import argparse
import socketserver
from . import MyPaddingHandler


if __name__ == "__main__":
    """creates a server and listens on the specified host and port, end it with Ctrl+C
    """
    parser = argparse.ArgumentParser(description="Padding Oracle Server")
    parser.add_argument("--host", type=str, default="localhost", help="The host to listen on")
    parser.add_argument("--port", type=int, default=9999, help="The port to listen on")
    args = parser.parse_args()
    host, port = args.host, args.port


    with socketserver.TCPServer((host, port), MyPaddingHandler) as server:
        print("Listening on {}:{}".format(host, port))
        server.serve_forever()