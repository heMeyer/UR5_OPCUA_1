import asyncio
import asyncua

from asyncua import Client, ua

client = Client


async def read_var_cont(client, node_id):
    while True:
        node = client.get_node(node_id)
        value = await node.read_value()

        print(str(node_id) + " = " + str(value))
        await asyncio.sleep(1)


async def start_program(var, node_id_start):
    node = client.get_node(node_id_start)
    await node.write_value(var)


async def write_pos(node_id_module_id, node_id_module_dir, id, dir):
    node = client.get_node(node_id_module_id)
    await node.write_value(id, ua.VariantType.Int32)

    node = client.get_node(node_id_module_dir)
    await node.write_value(dir, ua.VariantType.Int32)


async def read_pos(client, node_id_module_id, node_id_module_dir):
        node = client.get_node(node_id_module_id)
        value = await node.read_value()
        print(str(node_id_module_id) + " = " + str(value))

        node = client.get_node(node_id_module_dir)
        value = await node.read_value()
        print(str(node_id_module_dir) + " = " + str(value))


async def main():
    url_ur5 = "opc.tcp://192.168.157.233:4840"
    async with Client(url=url_ur5) as client:  # --> Hier könnte n Fehler sein...
        client = client
        # read_is_busy = asyncio.create_task(read_var_cont(client, node_id_isBusy))

        # Give id for Position of Pick/Place and site of where the module is located to the robot
        # await asyncio.create_task(write_pos(client, node_id_module_pick_nr, node_id_module_pick_dir, 1, 1))
        # await asyncio.create_task(read_pos(client, node_id_module_pick_nr, node_id_module_pick_dir))

        # await asyncio.create_task(write_pos(client, node_id_module_place_nr, node_id_module_place_dir, 2, 2))
        # await asyncio.create_task(read_pos(client, node_id_module_place_nr, node_id_module_place_dir))

        # Start Program
        # await asyncio.create_task(start_program(client, True))

        while True:
            await asyncio.sleep(1)



if __name__ == "__main__":
    asyncio.run(main())
