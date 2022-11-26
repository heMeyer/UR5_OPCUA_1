import asyncio
from asyncua import ua
from asyncua import Client
import math

urlUR5 = "opc.tcp://172.16.2.24:4840"

node_id_start = "ns=2;s=start"
node_id_isBusy = "ns=2;s=isBusy"

# Pick and Place Positions
node_id_posPick = ["ns=2;s=posXpick", "ns=2;s=posYpick", "ns=2;s=posZpick",
                   "ns=2;s=rotXpick", "ns=2;s=rotYpick", "ns=2;s=rotZpick"]

pos_pick = [-0.090, -0.598, 0.228,
            0.049, -2.230, 2.228]

node_id_pos2Pick = ["ns=2;s=posX2pick", "ns=2;s=posY2pick", "ns=2;s=posZ2pick",
                    "ns=2;s=rotX2pick", "ns=2;s=rotY2pick", "ns=2;s=rotZ2pick"]

pos_2pick = [-0.090, -0.598, 0.228,
             0.049, -2.230, 2.228]

node_id_posPlace = ["ns=2;s=posXplace", "ns=2;s=posYplace", "ns=2;s=posZplace",
                    "ns=2;s=rotXplace", "ns=2;s=rotYplace", "ns=2;s=rotZplace"]

pos_place = [-0.633, -0.331, 0.220,
             1.349, 2.504, -2.595]

node_id_pos2Place = ["ns=2;s=posX2place", "ns=2;s=posY2place", "ns=2;s=posZ2place",
                     "ns=2;s=rotX2place", "ns=2;s=rotY2place", "ns=2;s=rotZ2place"]

pos_2place = [-0.633, -0.331, 0.220,
              1.349, 2.504, -2.595]


async def read_var_cont(client, node_id):
    while True:
        node = client.get_node(node_id)
        value = await node.read_value()

        print(str(node_id) + " = " + str(value))
        await asyncio.sleep(1)


async def start_program(client, var):
    node = client.get_node(node_id_start)
    await node.write_value(var)


#async def write_pos(client, node_ids, pos):
#    for i in range(6):
#        node = client.get_node(node_ids[i])
#        await node.write_value(pos[i], ua.VariantType.Double)


async def write_pos(client, node_ids, pos):
    dist = 0
    reach = 1
    for i in range(3):
        dist = dist + pos[i]
    if math.sqrt(dist) > reach:
        print("Selected position out of reach")
    else:
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

        read_is_busy = asyncio.create_task(read_var_cont(client, node_id_isBusy))

        # Define Position Pick
        await asyncio.create_task(write_pos(client, node_id_posPick, pos_pick))
        await asyncio.create_task(read_pos(client, node_id_posPick))

        # Define Position 2Pick
        await asyncio.create_task(write_pos(client, node_id_pos2Pick, pos_2pick))
        await asyncio.create_task(read_pos(client, node_id_pos2Pick))

        # Define Position Place
        await asyncio.create_task(write_pos(client, node_id_posPlace, pos_place))
        await asyncio.create_task(read_pos(client, node_id_posPlace))

        # Define Position 2Place
        await asyncio.create_task(write_pos(client, node_id_pos2Place, pos_2place))
        await asyncio.create_task(read_pos(client, node_id_pos2Place))

        # Start Program
        await asyncio.create_task(start_program(client, False))

        await asyncio.sleep(20)

        read_is_busy.cancel()
        print("All tasks done")


if __name__ == "__main__":
    asyncio.run(main())
