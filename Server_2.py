import asyncio
import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from Client_2 import read_pos, write_pos, start_program

# Node IDs for communication with the OPC UA server of the robot (control)
nodeID_start = "ns=2;s=start"
nodeID_isBusy = "ns=2;s=isBusy"

nodeID_pick_id = "ns=2;s=module_pick_nr"
nodeID_pick_dir = "ns=2;s=module_pick_dir"

nodeID_place_id = "ns=2;s=module_place_nr"
nodeID_place_dir = "ns=2;s=module_place_dir"


# method to set pick and place position and start the process
@uamethod
async def pick_and_place(pick_id, pick_dir, place_id, place_dir):
    # Give id for Position of Pick/Place and site of where the module is located to the robot
    await asyncio.create_task(write_pos(nodeID_pick_id, nodeID_pick_dir, pick_id, pick_dir))
    await asyncio.create_task(read_pos(nodeID_pick_id, nodeID_pick_dir))

    await asyncio.create_task(write_pos(nodeID_place_id, nodeID_place_dir, place_id, place_dir))
    await asyncio.create_task(read_pos(nodeID_place_id, nodeID_place_dir))

    # Start Program
    await asyncio.create_task(start_program(nodeID_start))


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
    pick_id = ua.Argument()
    pick_id.Name = "pick_id"
    pick_id.DataType = ua.NodeId(ua.ObjectIds.Int32)
    pick_id.ValueRank = -1
    pick_id.ArrayDimensions = []
    pick_id.Description = ua.LocalizedText("ID of the module for picking")
    pick_dir = ua.Argument()
    pick_dir.Name = "pick_dir"
    pick_dir.DataType = ua.NodeId(ua.ObjectIds.Int32)
    pick_dir.ValueRank = -1
    pick_dir.ArrayDimensions = []
    pick_dir.Description = ua.LocalizedText("Direction of the direction for picking")

    place_id = ua.Argument()
    place_id.Name = "place_id"
    place_id.DataType = ua.NodeId(ua.ObjectIds.Int32)
    place_id.ValueRank = -1
    place_id.ArrayDimensions = []
    place_id.Description = ua.LocalizedText("ID of the module for placing")
    place_dir = ua.Argument()
    place_dir.Name = "place_dir"
    place_dir.DataType = ua.NodeId(ua.ObjectIds.Int32)
    place_dir.ValueRank = -1
    place_dir.ArrayDimensions = []
    place_dir.Description = ua.LocalizedText("Direction of the direction for placing")

    result = ua.Argument()
    result.Name = "result"
    result.DataType = ua.NodeId(ua.ObjectIds.Boolean)
    result.ValueRank = -1
    result.ArrayDimensions = []
    result.Description = ua.LocalizedText("Call successfull")

    # Maintenance position
    # ...

    # Populating address space
    await objects.add_method(idx, "pick_and_place", pick_and_place, [pick_id, pick_dir, place_id, place_dir], [result])

    # Running Server
    logger.info("Starting server!")
    async with server:
        while True:
            print("Counter Server")
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
    # logging.basicConfig(level=logging.DEBUG)
    # asyncio.run(main(), debug=True)
