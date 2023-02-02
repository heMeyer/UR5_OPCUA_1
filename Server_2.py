import asyncio
import logging
import queue

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from Client_2 import read_var, read_pos, write_pos, start_program

# Node IDs for communication with the OPC UA server of the robot control
nodeID_start = "ns=2;s=start"
nodeID_isBusy = "ns=2;s=isBusy"

nodeID_pick_id = "ns=2;s=pick_id"
nodeID_pick_dir = "ns=2;s=pick_dir"

nodeID_place_id = "ns=2;s=place_id"
nodeID_place_dir = "ns=2;s=place_dir"

# Fifo queue for storing pick and place requests, max 5 elements
pap_queue = queue.Queue(5)


# Function to set pick and place position and start the process
@uamethod
async def pick_and_place(node_id, pick_id, pick_dir, place_id, place_dir):
    # Check if queue already full, put request in queue
    if pap_queue.full():
        return False
    else:
        pap_queue.put([pick_id, pick_dir, place_id, place_dir])
        return True


async def pap_action(pick_id, pick_dir, place_id, place_dir):
    # Set ID of module and its direction, start Process
    # Pick
    await asyncio.create_task(write_pos(nodeID_pick_id, nodeID_pick_dir, pick_id, pick_dir))
    await asyncio.create_task(read_pos(nodeID_pick_id, nodeID_pick_dir))
    # Place
    await asyncio.create_task(write_pos(nodeID_place_id, nodeID_place_dir, place_id, place_dir))
    await asyncio.create_task(read_pos(nodeID_place_id, nodeID_place_dir))
    # Start
    await asyncio.create_task(start_program(nodeID_start))


async def main():
    logger = logging.getLogger(__name__)

    # Setup server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")
    server.set_server_name("Digital Factory Transfer")

    # Setup namespace
    uri = "https://github.com/heMeyer/UR5_OPCUA_1.git"
    idx = await server.register_namespace(uri)

    # Create root node for upcoming functions, variables...
    objects = server.nodes.objects

    # prepare arguments for methods
    # Pick and place
    pick_id = ua.Argument()  # Implementation as a argument
    pick_id.Name = "pick_id"  # Display name
    pick_id.DataType = ua.NodeId(ua.ObjectIds.Int32)  # Data type
    pick_id.ValueRank = -1  # Amount of array dimensions (-1 equals scalar value)
    pick_id.ArrayDimensions = []  # amount of values in each array dimension
    pick_id.Description = ua.LocalizedText("ID of the module for picking")  # Display explanation
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

    result_pap = ua.Argument()
    result_pap.Name = "result_pap"
    result_pap.DataType = ua.NodeId(ua.ObjectIds.Boolean)
    result_pap.ValueRank = -1
    result_pap.ArrayDimensions = []
    result_pap.Description = ua.LocalizedText("Call successfull")

    # Service positions, as integer to enable possibility of different actions/positions
    service = ua.Argument()
    service.Name = "maintenance"
    service.DataType = ua.DataType = ua.NodeId(ua.ObjectIds.Int32)
    service.ValueRank = -1
    service.ArrayDimensions = []
    service.Description = ua.LocalizedText("Service Positions: 0 = none, 1 = Inspection, 2 = Gripper change")

    result_s = ua.Argument()
    result_s.Name = "result_s"
    result_s.DataType = ua.NodeId(ua.ObjectIds.Boolean)
    result_s.ValueRank = -1
    result_s.ArrayDimensions = []
    result_s.Description = ua.LocalizedText("Call successfull")

    # Populating address space
    await objects.add_method(idx, "pick_and_place", pick_and_place, [pick_id, pick_dir, place_id, place_dir],
                             [result_pap])

    # Running Server
    logger.info("Starting server!")
    async with server:
        while True:
            # Read/update variables
            robotBusy = read_var(nodeID_isBusy)

            # Send pick and place instruction if one in queue
            if not pap_queue.empty() and not robotBusy:
                instruction = pap_queue.get()
                await asyncio.create_task(pap_action(instruction.pick_id, pick_dir, place_id, place_dir))

            # basic server functions
            print("Counter Server")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
    # logging.basicConfig(level=logging.DEBUG)
    # asyncio.run(main(), debug=True)
