import asyncio
import logging
import datetime

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from Client_2 import write_pos, start_program

# Node IDs for communication with the OPC UA server of the robot (control)
node_id_start = "ns=2;s=start"
node_id_isBusy = "ns=2;s=isBusy"

node_id_module_pick_nr = "ns=2;s=module_pick_nr"
node_id_module_pick_dir = "ns=2;s=module_pick_dir"

node_id_module_place_nr = "ns=2;s=module_place_nr"
node_id_module_place_dir = "ns=2;s=module_place_dir"


# method to set pick and place position and start the process
@uamethod
def pick_and_place(module_id, direction_id, aua):
    print("Hello from the other seite")

    # Give id for Position of Pick/Place and site of where the module is located to the robot
    asyncio.run(write_pos(node_id_module_pick_nr, node_id_module_pick_dir, 1, 1))
    # await asyncio.create_task(write_pos(node_id_module_place_nr, node_id_module_place_dir, 2, 2))

    # Start Program
    # await asyncio.create_task(start_program(True))

    return True


async def main():
    logger = logging.getLogger(__name__)

    # setup server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")
    server.set_server_name("Digital Factory Transfer")

    # setup namespace, not really necessary but should as spec
    uri = "https://github.com/heMeyer/UR5_OPCUA_1.git"
    idx = await server.register_namespace(uri)

    # Create root node for our stuff
    objects = server.nodes.objects

    # prepare arguments for methods
    # Pick and place
    module_id = ua.Argument()
    module_id.Name = "module_id"
    module_id.DataType = ua.NodeId(ua.ObjectIds.Int64)
    module_id.ValueRank = -1
    module_id.ArrayDimensions = []
    module_id.Description = ua.LocalizedText("ID of the module")
    direction_id = ua.Argument()
    direction_id.Name = "direction_id"
    direction_id.DataType = ua.NodeId(ua.ObjectIds.Int64)
    direction_id.ValueRank = -1
    direction_id.ArrayDimensions = []
    direction_id.Description = ua.LocalizedText("ID of the direction")
    result = ua.Argument()
    result.Name = "result"
    result.DataType = ua.NodeId(ua.ObjectIds.Boolean)
    result.ValueRank = -1
    result.ArrayDimensions = []
    result.Description = ua.LocalizedText("Call successfull")
    # Maintenance position

    # Populating address space
    await objects.add_method(idx, "pick and place", pick_and_place, [module_id, direction_id], [result])

    # Running Server
    logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1)

            now = datetime.datetime.now
            print("hallu")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
