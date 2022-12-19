import asyncio
from asyncua import Server, ua
from asyncua.common.methods import uamethod
import logging


@uamethod
def pick_and_place(parent, value):
    return True


async def main():
    logger = logging.getLogger(__name__)

    # setup server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    # import nodes from AAS in xml format
    await server.import_xml("UR5_OPCUA.xml")

    # setup namespace, not really necessary but should as spec
    uri = "https://github.com/heMeyer/UR5_OPCUA_1.git"
    idx = await server.register_namespace(uri)

    # Reference to existing variables from AAS
    payload = server.get_node("ns=3;i=550")

    # Reference to existing Methods from AAS
    # pick_and_place = server.get_node("ns=3;i=")
    # server.link_method(pick_and_place, pick_and_place)

    # Running Server
    logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)



            # await payload.write_value(3, ua.VariantType.Int32)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)

