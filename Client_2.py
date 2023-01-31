import asyncio
import logging

from asyncua import Client, ua

url_ur5 = "opc.tcp://usertest:usertest@192.168.157.233:4840"


async def read_var_cont(nodeID):
    async with Client(url=url_ur5) as client:
        while True:
            node = client.get_node(nodeID)
            value = await node.read_value()

            print(str(nodeID) + " = " + str(value))
            await asyncio.sleep(1)


async def start_program(nodeID_start):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID_start)
        await node.write_value(True)


async def write_pos(nodeID_id, nodeID_dir, id, dir):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID_id)
        await node.write_value(id, ua.VariantType.Int32)

        node = client.get_node(nodeID_dir)
        await node.write_value(dir, ua.VariantType.Int32)


async def read_pos(nodeID_id, nodeID_dir):
    async with Client(url=url_ur5) as client:
        node = client.get_node(nodeID_id)
        value = await node.read_value()
        print(str(nodeID_id) + " = " + str(value))

        node = client.get_node(nodeID_dir)
        value = await node.read_value()
        print(str(nodeID_dir) + " = " + str(value))


async def main():
    async with Client(url=url_ur5) as client:
        while True:
            print("Counter Client")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
    # logging.basicConfig(level=logging.DEBUG)
    # asyncio.run(main(), debug=True)
