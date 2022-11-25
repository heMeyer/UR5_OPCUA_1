import asyncio
from asyncua import ua
from asyncua import Client

urlUR5 = "opc.tcp://172.16.2.24:4840"

node_id1 = "ns=2;s=test"
node_id_start = "ns=2;s=start"
node_id_isBusy = "ns=2;s=isBusy"

node_id_posPick = ["ns=2;s=posXpick", "ns=2;s=posYpick", "ns=2;s=posZpick",
                   "ns=2;s=rotXpick", "ns=2;s=rotYpick", "ns=2;s=rotZpick"]

pos_pick = [-0.111, -0.448, 0.088,
            3.114, -0.264, -0.085]
# 0.36, 3.15, -0.04

async def read_var(client, node_id):
    while True:
        node = client.get_node(node_id)
        value = await node.read_value()

        print(str(node_id) + " = " + str(value))
        await asyncio.sleep(1)


async def start_program(client, var):
    node = client.get_node(node_id_start)
    await node.write_value(var)


async def write_pos(client, node_ids, pos):
    for i in range(6):
        node = client.get_node(node_ids[i])
        await node.write_value(pos[i], ua.VariantType.Double)


async def read_pos(client, node_ids):
    for i in range(6):
        node = client.get_node(node_ids[i])
        value = await node.read_value()
        print(str(node_ids[i]) + " = " + str(value))


async def main():
    async with Client(url=urlUR5) as client:

        read2 = asyncio.create_task(read_var(client, node_id_isBusy))

        await asyncio.create_task(write_pos(client, node_id_posPick, pos_pick))
        await asyncio.create_task(read_pos(client, node_id_posPick))
        await asyncio.create_task(start_program(client, True))

        await asyncio.sleep(20)

        read2.cancel()
        print("All tasks done")


if __name__ == "__main__":
    asyncio.run(main())
