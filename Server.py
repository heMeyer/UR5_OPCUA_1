import asyncio
from asyncua import Server, ua
from asyncua.common.methods import uamethod
from asyncua.common.xmlimporter import XmlImporter
import logging


@uamethod
def func(parent, value):
    return value * 2


async def main():
    logger = logging.getLogger(__name__)

    # setup server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    # import xml nodes
    # importer = XmlImporter(server)
    # nodes = await importer.import_xml('UR5_OPCUA.xml')
    # wait importer.make_objects(nodes)
    await server.import_xml("UR5_OPCUA.xml")

    # setup namespace, not really necessary but should as spec
    uri = "https://github.com/heMeyer/UR5_OPCUA_1.git"
    idx = await server.register_namespace(uri)

    # populating address space
    # server.nodes, contains links to very common nodes like objects and root
    my_obj = await server.nodes.objects.add_object(idx, "MyObject")
    my_var = await my_obj.add_variable(idx, "MyVariable", 6.7)

    # Set MyVariable to be writable by clients
    await my_var.set_writable()
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )

    logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)
            new_val = await my_var.get_value() + 0.1
            logger.info("Set value of %s to %.1f", my_var, new_val)
            await my_var.write_value(new_val)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)


