import asyncio
import logging
import datetime

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from Client_2 import read_pos, write_pos, start_program

# Node IDs for communication with the OPC UA server of the robot (control)
node_id_start = "ns=2;s=start"
node_id_isBusy = "ns=2;s=isBusy"

node_id_module_pick_nr = "ns=2;s=module_pick_nr"
node_id_module_pick_dir = "ns=2;s=module_pick_dir"

node_id_module_place_nr = "ns=2;s=module_place_nr"
node_id_module_place_dir = "ns=2;s=module_place_dir"


# method to set pick and place position and start the process
@uamethod
async def pick_and_place(node_id, module_id_pick, module_dir_pick, module_id_place, module_dir_place):
    print(node_id)

    # Give id for Position of Pick/Place and site of where the module is located to the robot
    await asyncio.create_task(
        write_pos(node_id_module_pick_nr, node_id_module_pick_dir, module_id_pick, module_dir_pick))
    await asyncio.create_task(read_pos(node_id_module_pick_nr, node_id_module_pick_dir))

    await asyncio.create_task(
        write_pos(node_id_module_place_nr, node_id_module_place_dir, module_id_place, module_dir_place))
    await asyncio.create_task(read_pos(node_id_module_place_nr, node_id_module_place_dir))

    # Start Program
    await asyncio.create_task(start_program(True, node_id_start))


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
    module_id_pick = ua.Argument()
    module_id_pick.Name = "module_id_pick"
    module_id_pick.DataType = ua.NodeId(ua.ObjectIds.Int32)
    module_id_pick.ValueRank = -1
    module_id_pick.ArrayDimensions = []
    module_id_pick.Description = ua.LocalizedText("ID of the module for picking")
    direction_id_pick = ua.Argument()
    direction_id_pick.Name = "direction_id_pick"
    direction_id_pick.DataType = ua.NodeId(ua.ObjectIds.Int32)
    direction_id_pick.ValueRank = -1
    direction_id_pick.ArrayDimensions = []
    direction_id_pick.Description = ua.LocalizedText("ID of the direction for picking")

    module_id_place = ua.Argument()
    module_id_place.Name = "module_id_place"
    module_id_place.DataType = ua.NodeId(ua.ObjectIds.Int32)
    module_id_place.ValueRank = -1
    module_id_place.ArrayDimensions = []
    module_id_place.Description = ua.LocalizedText("ID of the module for placing")
    direction_id_place = ua.Argument()
    direction_id_place.Name = "direction_id_place"
    direction_id_place.DataType = ua.NodeId(ua.ObjectIds.Int32)
    direction_id_place.ValueRank = -1
    direction_id_place.ArrayDimensions = []
    direction_id_place.Description = ua.LocalizedText("ID of the direction for placing")

    result = ua.Argument()
    result.Name = "result"
    result.DataType = ua.NodeId(ua.ObjectIds.Boolean)
    result.ValueRank = -1
    result.ArrayDimensions = []
    result.Description = ua.LocalizedText("Call successfull")
    # Maintenance position

    # Populating address space
    await objects.add_method(idx, "pick_and_place", pick_and_place,
                             [module_id_pick, direction_id_pick, module_id_place, direction_id_place], [result])

    # Running Server
    logger.info("Starting server!")
    async with server:
        while True:
            print("Counter Server")
            await asyncio.sleep(1)

            now = datetime.datetime.now


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
