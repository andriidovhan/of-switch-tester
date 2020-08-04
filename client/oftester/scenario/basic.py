import logging

from oftester.constants import OFPP_IN_PORT
from oftester.openflow import flows
from oftester.scenario.model import Scenario


class PpsScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding push/pop rules")


class VlanScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding push/pop rules")

            self.add_flow(flows.flow_vlan_push_pop(sw.dpid, sw.snake_end_port, OFPP_IN_PORT, 'pop'))
            self.add_flow(flows.flow_vlan_push_pop(sw.dpid, sw.snake_start_port, OFPP_IN_PORT, 'push'))


class VlanScenarioShort(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding push/pop rules")
            self.add_flow(flows.flow_vlan_push_pop(sw.dpid, sw.snake_end_port, OFPP_IN_PORT, 'pop'))
            logging.info("Setting header values")
            self.add_flow(flows.flow_vlan_push_pop(sw.dpid, sw.snake_start_port, OFPP_IN_PORT, 'push', vid=42))


class VxlanScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding push/pop vxlan rules")

            self.add_flow(flows.flow_vxlan_pop(sw.dpid, sw.snake_end_port, OFPP_IN_PORT))
            logging.info("Setting header values")
            self.add_flow(flows.flow_vxlan_push(sw.dpid, sw.snake_start_port, OFPP_IN_PORT, vni=4242))


class VxlanScenarioShort(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())

            logging.info("Switch under full load adding push/pop vxlan rules")
            self.add_flow(flows.flow_vxlan_pop(sw.dpid, sw.snake_end_port, OFPP_IN_PORT))
            self.add_flow(flows.flow_vxlan_push(sw.dpid, sw.snake_start_port_, OFPP_IN_PORT, flags=0))


class SwapScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding swap fields rules")
            self.add_flow(flows.pass_through_flow(sw.dpid, sw.snake_end_port, OFPP_IN_PORT))
            self.add_flow(flows.flow_swap_fields(sw.dpid, sw.snake_start_port, OFPP_IN_PORT))


class CopyScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding copy fields rules")
            self.add_flow(flows.pass_through_flow(sw.dpid, sw.snake_end_port, OFPP_IN_PORT))
            self.add_flow(flows.flow_copy_fields(sw.dpid, sw.snake_start_port, OFPP_IN_PORT))


class MetadataScenario(Scenario):
    def run(self):
        for sw in self.environment.switches.values():
            self.prepare_snake_flows(sw.dpid, self.current_packet_size())
            logging.info("Switch under full load adding metadata_write rules")
            self.add_flow(flows.pass_through_flow(sw.dpid, sw.snake_end_port, OFPP_IN_PORT))
            for flow in flows.metadata_milti_table_flows(sw.dpid, sw.snake_start_port, OFPP_IN_PORT):
                self.add_flow(flow)
