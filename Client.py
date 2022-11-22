import asyncio
import time
import asyncua as ua

from asyncua import Client

urlUR5 = "opc.tcp://172.16.2.24:4840"


async def read_var(node_id):
    async with Client(url=urlUR5) as client:
        while True:
            node = client.get_node(node_id)
            value = await node.read_value()

            print(value)
            time.sleep(1)


async def write_var(node_id):
    async with Client(url=urlUR5) as client:
        node = client.get_node(node_id)

        await node.write_value(0, ua.ua.VariantType.Int32)

node_id_1 = "ns=2;s=test"

#asyncio.run(read_var(node_id_1))
asyncio.run(write_var(node_id_1))

