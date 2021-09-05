#!/usr/bin/env python
import pathlib
import json
import logging
import pandas as pd
from N2G import drawio_diagram
from pybatfish.client.commands import *
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints
from pybatfish.datamodel import *
from colorama import Fore, init

logging.getLogger("pybatfish").setLevel(logging.ERROR)
init(autoreset=True)
diagram = drawio_diagram()

print(Fore.GREEN + "*****************************************************************************" )
print(Fore.YELLOW + " Batfish Network Visualizer v1.0 " + Fore.CYAN + "Created by Pandu Konala   " )
print(Fore.GREEN + "*****************************************************************************" )
NETWORK_NAME = "network"
BASE_SNAPSHOT_NAME = "batfish-candidate"
BASE_SNAPSHOT_PATH = "./snapshot"
bf_session.host = "127.0.0.1"

def initialise_batfish():
    load_questions()
    bf_set_network(NETWORK_NAME)
    bf_init_snapshot(BASE_SNAPSHOT_PATH, name=BASE_SNAPSHOT_NAME, overwrite=True)

def analyse_network(report_dir):

    #Batfish Queries Start
    parse_status = bfq.fileParseStatus().answer().frame() #Extract the status of configurations
    node_properties = bfq.nodeProperties().answer().frame() #Extract Node properties
    interface = bfq.interfaceProperties().answer().frame() #Extract Interface properties
    vlan_prop = bfq.switchedVlanProperties().answer().frame() #Extract VLAN properties
    ip_owners = bfq.ipOwners().answer().frame() #Extract IP Owners
    l3edge = bfq.layer3Edges().answer().frame() #Extract L3 edges
    mlag = bfq.mlagProperties().answer().frame() #Extract MPLAG properties
    ospf_config = bfq.ospfProcessConfiguration().answer().frame() #Extract OSPF configuration
    ospf_area_config = bfq.ospfAreaConfiguration().answer().frame() #Extract OSPF area configuration
    ospf_interface = bfq.ospfInterfaceConfiguration().answer().frame() #Extract OSPF interface configuration
    ospf_session = bfq.ospfSessionCompatibility().answer().frame() #Extract OSPF Session compatability
    bgp_config = bfq.bgpProcessConfiguration().answer().frame() #Extract BGP configuration
    bgp_peer_config = bfq.bgpPeerConfiguration().answer().frame() #Extract BGP peer configuration
    bgp_session = bfq.bgpSessionStatus().answer().frame() #Extract BGP session compatibility
    routing = bfq.routes().answer().frame() #Extract Routing table
    f5_vip = bfq.f5BigipVipConfiguration().answer().frame() #Extract F5 VIP configuration
    named_structure = bfq.namedStructures().answer().frame() #Extract Named Structures
    def_structure = bfq.definedStructures().answer().frame() #Extract Structure deginitions
    ref_structure = bfq.referencedStructures().answer().frame() #Extract Referenced structures
    undefined_references = bfq.undefinedReferences().answer().frame() #Extract Undefined references
    unused_structure = bfq.unusedStructures().answer().frame() #Extract Used structures
    #Batfish Queries End
    
    #Result from Batfish Start
    analysis_report_file = report_dir + "/" + NETWORK_NAME + "_analysis_result.xlsx"
    with pd.ExcelWriter(analysis_report_file) as work_book:
        parse_status.to_excel(work_book, sheet_name="parse_satus", engine="xlsxwriter")
        node_properties.to_excel(
            work_book, sheet_name="node_properties", engine="xlsxwriter"
        )
        interface.to_excel(
            work_book, sheet_name="interface_properties", engine="xlsxwriter"
        )
        vlan_prop.to_excel(work_book, sheet_name="vlan_properties", engine="xlsxwriter")
        ip_owners.to_excel(work_book, sheet_name="IPOwners", engine="xlsxwriter")
        l3edge.to_excel(work_book, sheet_name="l3edges", engine="xlsxwriter")
        mlag.to_excel(work_book, sheet_name="mlag", engine="xlsxwriter")
        ospf_session.to_excel(work_book, sheet_name="ospf_session", engine="xlsxwriter")
        ospf_config.to_excel(work_book, sheet_name="ospf_config", engine="xlsxwriter")
        ospf_area_config.to_excel(
            work_book, sheet_name="ospf_area_config", engine="xlsxwriter"
        )
        ospf_interface.to_excel(
            work_book, sheet_name="ospf_interface", engine="xlsxwriter"
        )
        bgp_config.to_excel(work_book, sheet_name="bgp_config", engine="xlsxwriter")
        bgp_peer_config.to_excel(
            work_book, sheet_name="bgp_peer_config", engine="xlsxwriter"
        )
        bgp_session.to_excel(work_book, sheet_name="bgp_session", engine="xlsxwriter")
        routing.to_excel(work_book, sheet_name="routing_table", engine="xlsxwriter")
        f5_vip.to_excel(work_book, sheet_name="f5_vip", engine="xlsxwriter")
        named_structure.to_excel(
            work_book, sheet_name="named_structure", engine="xlsxwriter"
        )
        def_structure.to_excel(
            work_book, sheet_name="defined_structures", engine="xlsxwriter"
        )
        ref_structure.to_excel(
            work_book, sheet_name="referrenced_structures", engine="xlsxwriter"
        )
        undefined_references.to_excel(
            work_book, sheet_name="undefined_references", engine="xlsxwriter"
        )
        unused_structure.to_excel(
            work_book, sheet_name="unused_structure", engine="xlsxwriter"
        )
	#Result from Batfish End
	
def plot_ospf_graph():

    ospfneigh = bfq.ospfSessionCompatibility().answer().frame()
    if ospfneigh.empty:
        print(Fore.RED + " # No OSPF Neighhbors Detected...")
    else:
        print(Fore.YELLOW + " --> Visualized OSPF Tables!")
        ospfneigh_json = json.loads(ospfneigh.to_json(orient="index"))
        # print (json.dumps(ospfneigh_json, indent=4))
        mapped_node = []
        mapped_link_list = []
        diagram.add_diagram("OSPF")
        for key in ospfneigh_json:
            current_link = []
            current_link_reverse = []
            neighbor = ospfneigh_json[key]
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            current_link = [f"{node_id}", f"{remote_node_id}"]
            current_link_reverse = [f"{remote_node_id}", f"{node_id}"]
            if current_link not in mapped_link_list:
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["IP"]})(AreaID={neighbor["Area"]})'
                    f' == {neighbor["Session_Status"]}'
                    f" == {remote_node_id}"
                    f'({neighbor["Remote_IP"]})(AreaID={neighbor["Remote_Area"]}',
                )
                mapped_link_list.append(current_link)
                mapped_link_list.append(current_link_reverse)

def plot_bgp_graph():

    bgpneigh = bfq.bgpSessionStatus().answer().frame()
    if bgpneigh.empty:
        print(Fore.RED + " # No BGP Peers Detected...")
    else:
        print(Fore.YELLOW + " --> Visualized BGP Tables!")
        bgpneigh_json = json.loads(bgpneigh.to_json(orient="index"))
        mapped_node = []
        mapped_link_list = []
        diagram.add_diagram("BGP")
        for key in bgpneigh_json:
            current_link = []
            current_link_reverse = []
            neighbor = bgpneigh_json[key]
            node_id = f'{neighbor["Node"]}\n({neighbor["Local_AS"]})'
            remote_node_id = f'{neighbor["Remote_Node"]}\n({neighbor["Remote_AS"]})'
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            current_link = [f"{node_id}", f"{remote_node_id}"]
            current_link_reverse = [f"{remote_node_id}", f"{node_id}"]
            if current_link not in mapped_link_list:
                diagram.add_link(
                    f"{node_id}",
                    f"{remote_node_id}",
                    label=f'{node_id}({neighbor["Local_IP"]})'
                    f' == {neighbor["Established_Status"]}'
                    f' == {remote_node_id}({neighbor["Remote_IP"]})',
                )
                mapped_link_list.append(current_link)
                mapped_link_list.append(current_link_reverse)

def plot_l3_graph():
    l3edges = bfq.layer3Edges().answer().frame()
    if l3edges.empty:
        print(Fore.RED + " # No L3 Adjencies Detected...")
    else:
        print(Fore.YELLOW + " --> Visualized L3 Network!")
        l3edges_json = json.loads(l3edges.to_json(orient="index"))
        mapped_node = []
        diagram.add_diagram("L3")
        for key in l3edges_json:
            neighbor = l3edges_json[key]
            node_id = f'{neighbor["Interface"]["hostname"]}'
            remote_node_id = f'{neighbor["Remote_Interface"]["hostname"]}'
            if node_id not in mapped_node:
                diagram.add_node(id=f"{node_id}")
                mapped_node.append(node_id)
            if remote_node_id not in mapped_node:
                diagram.add_node(id=f"{remote_node_id}")
                mapped_node.append(remote_node_id)
            diagram.add_link(
                f"{node_id}",
                f"{remote_node_id}",
                label=f'{node_id}({neighbor["IPs"]})'
                f" == VLAN {key}"
                f' == {remote_node_id}({neighbor["Remote_IPs"]})',
            )

def main():

    initialise_batfish()
    report_dir = "results"
    pathlib.Path(report_dir).mkdir(exist_ok=True)
    print(Fore.CYAN + "\n$ Analysing Configurations...")
    analyse_network(report_dir)
    print(Fore.CYAN + "\n$ Visualizing Network...")
    plot_ospf_graph()
    plot_bgp_graph()
    plot_l3_graph()
    diagram.layout(algo="kk")
    diagram_file_name = report_dir + "/" + "network_map.drawio"
    diagram.dump_file(filename=diagram_file_name, folder="./")

    print(Fore.GREEN + "\n$ Network Visualization Complete!")
    print(Fore.BLUE + "\n***  Open the output file at " + Fore.RED + "https://app.diagrams.net" + Fore.BLUE + "  ***"+ "\n")
    print(Fore.GREEN + "*****************************************************************************" )

if __name__ == "__main__":
    main()
