import time
from scapy.all import sniff, IP, TCP, UDP

flows = {}
FLOW_TIMEOUT = 0.2


def capture_and_flow_control(iface, flow_check):

    def process_packet(pkt):
        if IP not in pkt:
            return

        ts = time.time()
        ip = pkt[IP]

        payload_len = 0
        flags = 0

        if TCP in pkt:
            sport = pkt[TCP].sport
            dport = pkt[TCP].dport
            flags = pkt[TCP].flags
            proto = "0"
            payload_len = len(pkt[TCP].payload)

        elif UDP in pkt:
            sport = pkt[UDP].sport
            dport = pkt[UDP].dport
            proto = "1"
            payload_len = len(pkt[UDP].payload)

        else:
            return

        key = (ip.src, ip.dst, sport, dport)

        if key not in flows:
            flows[key] = {
                "src_port": sport,
                "dst_port": dport,
                "protocol": proto,
                "start": ts,
                "last": ts,

                "packets": 0,
                "fwd": 0,
                "bwd": 0,

                "fin": 0,
                "syn": 0,
                "rst": 0,
                "psh": 0,
                "ack": 0,
                "urg": 0,
                "ece": 0,
                "cwr": 0,

                "total_payload_bytes": 0,
                "fwd_total_payload_bytes": 0,
                "total_header_bytes": 0,

                "src_ip": ip.src
            }

        f = flows[key]

        f["packets"] += 1
        f["last"] = ts

        if ip.src == f["src_ip"]:
            f["fwd"] += 1
            f["fwd_total_payload_bytes"] += payload_len
        else:
            f["bwd"] += 1

        f["total_payload_bytes"] += payload_len

        header_len = len(pkt) - payload_len
        f["total_header_bytes"] += header_len

        #FLAGS
        if flags & 0x01: f["fin"] += 1
        if flags & 0x02: f["syn"] += 1
        if flags & 0x04: f["rst"] += 1
        if flags & 0x08: f["psh"] += 1
        if flags & 0x10: f["ack"] += 1
        if flags & 0x20: f["urg"] += 1
        if flags & 0x40: f["ece"] += 1
        if flags & 0x80: f["cwr"] += 1

        return expire_flows(ts, flow_check)
    sniff(iface=iface, prn=process_packet, store=False)


def expire_flows(now, flow_check):
    expired = []

    for key, f in flows.items():
        if now - f["last"] > FLOW_TIMEOUT:
            expired.append(key)

    for key in expired:
        f = flows[key]
        duration = f["last"] - f["start"]

        details = (f["src_port"], f["dst_port"], f["protocol"], round(duration, 5), f["packets"], f["fwd"],
                f["bwd"], f["total_payload_bytes"], f["fwd_total_payload_bytes"], f["total_header_bytes"], f["fin"], f["psh"],
                f["urg"], f["ece"], f["syn"], f["ack"], f["cwr"], f["rst"])
        flow_check(details)
        del flows[key]
