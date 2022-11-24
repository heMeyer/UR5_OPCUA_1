import asyncio
from asyncua import ua
from asyncua import Client

urlUR5 = "opc.tcp://172.16.2.24:4840"
node_id1 = "ns=2;s=test"

node_id_start = "ns=2;s=start"
node_id_isBusy = "ns=2;s=isBusy"

node_id_posXpick = "ns=2;s=posXpick"
node_id_posYpick = "ns=2;s=posYpick"
node_id_posZpick = "ns=2;s=posZpick"
node_id_rotXpick = "ns=2;S=rotXpick"
node_id_rotYpick = "ns=2;S=rotYpick"
node_id_rotZpick = "ns=2;S=rotZpick"


async def read_var(client, node_id):
    while True:
        node = client.get_node(node_id)
        value = await node.read_value()

        print("start variable: " + str(value))
        print("isBusy variable: ")
        await asyncio.sleep(1)


async def start_program(client):
    node = client.get_node(node_id_start)

    await node.write_value(True)


async def main():
    async with Client(url=urlUR5) as client:

        asyncio.create_task(read_var(client, node_id_start))
        # asyncio.create_task(read_var(client, node_id_isBusy))

        # await asyncio.create_task(start_program(client))

        await asyncio.sleep(5)
        read_var(client, node_id_isBusy).close()
        read_var(client, node_id_start).close()
        print("All tasks done")


if __name__ == "__main__":
    asyncio.run(main())

