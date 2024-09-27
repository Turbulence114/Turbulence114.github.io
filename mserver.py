from enum import Enum
import hivemind
import time
import threading

import hivemind.utils

logger = hivemind.utils.get_logger(__name__)
get_dht_time = hivemind.utils.get_dht_time()
time_to_next_update = 10

class CMD(Enum):
    STOP = "stop"
    START = "start"
    END_SCHEDULE = "end_schedule"


class MServer:
    def __init__(
        self,
        zone_key: str,
    ):
        self.dht = hivemind.DHT(start=True)
        self.zone_key = zone_key
        self.id_map = dict()
        self.span_list = dict()
        self.zone_span_id = 0
        self.update_thread_handler = threading.Thread(target = self.update_block_models_in_background, daemon= True)
        self.update_thread_handler.start()

    def update_block_models_in_background(self):
        while True:

            response = self.dht.get(self.zone_key, latest=True)
            current_time = get_dht_time
            if isinstance(response, hivemind.utils.ValueWithExpiration) and isinstance(response.value, dict):
                for _, span_info in response.value.items():
                    try:
                        (flop, memory, peer_id), expiration_time = span_info
                        if expiration_time < current_time:
                            # the peer is invalid, we need remove the item from span_list and id_map
                            span_id = self.id_map.get(peer_id)
                            if span_id != None:
                                print("the peer is invalid, will remove it")
                                self.span_list.pop(span_id)
                                self.id_map.pop(peer_id)
                        else:
                            span_id = self.id_map.get(peer_id)
                            if span_id == None:
                                print("allocate span_id for peer", peer_id)
                                self.zone_span_id += 1
                                self.id_map[peer_id] = self.zone_span_id
                            # self.id_map.update()
                            # store span_info (flop, memory, peer_id) for resource allocated
                                self.span_list[self.zone_span_id] = (flop,memory,peer_id)

                    except Exception as e:
                        logger.warning(f"Skipping span_info  {span_info} (exc={e})")
            else:
                logger.warning(
                    f"Could not refresh experts, dht info key contains {response}, "
                    f"will retry in {time_to_next_update}s"
                )
            
            time.sleep(time_to_next_update)
        
    def allocate_span(self):
        for span_id, span_info in self.span_list.items():
            print(f"span_id {span_id}, span_info {span_info}")
    

        

     
