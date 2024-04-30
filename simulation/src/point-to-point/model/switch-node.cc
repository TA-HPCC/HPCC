#include "ns3/ipv4.h"
#include "ns3/packet.h"
#include "ns3/ipv4-header.h"
#include "ns3/pause-header.h"
#include "ns3/flow-id-tag.h"
#include "ns3/boolean.h"
#include "ns3/uinteger.h"
#include "ns3/double.h"
#include "switch-node.h"
#include "qbb-net-device.h"
#include "ppp-header.h"
#include "ns3/int-header.h"
#include <cmath>

namespace ns3 {

TypeId SwitchNode::GetTypeId (void)
{
  static TypeId tid = TypeId ("ns3::SwitchNode")
    .SetParent<Node> ()
    .AddConstructor<SwitchNode> ()
	.AddAttribute("EcnEnabled",
			"Enable ECN marking.",
			BooleanValue(false),
			MakeBooleanAccessor(&SwitchNode::m_ecnEnabled),
			MakeBooleanChecker())
	.AddAttribute("CcMode",
			"CC mode.",
			UintegerValue(0),
			MakeUintegerAccessor(&SwitchNode::m_ccMode),
			MakeUintegerChecker<uint32_t>())
	.AddAttribute("AckHighPrio",
			"Set high priority for ACK/NACK or not",
			UintegerValue(0),
			MakeUintegerAccessor(&SwitchNode::m_ackHighPrio),
			MakeUintegerChecker<uint32_t>())
	.AddAttribute("MaxRtt",
			"Max Rtt of the network",
			UintegerValue(9000),
			MakeUintegerAccessor(&SwitchNode::m_maxRtt),
			MakeUintegerChecker<uint32_t>())
  ;
  return tid;
}

SwitchNode::SwitchNode(){
	m_ecmpSeed = m_id;
	m_node_type = 1;
	m_mmu = CreateObject<SwitchMmu>();
	for (uint32_t i = 0; i < pCnt; i++)
		for (uint32_t j = 0; j < pCnt; j++)
			for (uint32_t k = 0; k < qCnt; k++)
				m_bytes[i][j][k] = 0;
	for (uint32_t i = 0; i < pCnt; i++)
		m_txBytes[i] = 0;
	for (uint32_t i = 0; i < pCnt; i++)
		m_lastPktSize[i] = m_lastPktTs[i] = 0;
	for (uint32_t i = 0; i < pCnt; i++)
		m_u[i] = 0;
	past_byte_cnt_reg.assign(pCnt,0);
	obs_last_seen_reg.assign(pCnt, Time());
	tel_insertion_window_reg.assign(pCnt, Time());
	delta_reg.assign(pCnt, 0);
	n_last_values_reg.assign(pCnt, 0);
	count_reg.assign(pCnt, 0);
	pres_byte_cnt_reg.assign(pCnt,0);
	telemetry_byte_cnt_reg.assign(pCnt,0);
	packets_cnt_reg.assign(pCnt,0);
	previous_insertion_reg.assign(pCnt, Time());
	past_device_obs_reg.assign(pCnt, 0);
	past_reported_obs_reg.assign(pCnt, 0);
}

// Updates the dynamic threshold according to the SIMPLE MOVING AVERAGE function of the last k measured throughputs
void SwitchNode::update_delta(uint32_t &ifIndex, uint32_t comparator, int32_t &delta) {
    uint32_t ct, sum;
    ct = count_reg.at(ifIndex);
    sum = n_last_values_reg.at(ifIndex);
    if (ct == k) {
        int32_t mean, old_m;
        mean = sum >> div_shift;

        delta = static_cast<int32_t>(((div_10 * static_cast<int64_t>(mean)) >> 32));

        delta_reg.at(ifIndex) = delta;
        sum = 0;
        ct = 0;
    }

    sum += comparator;
    ct++;

    n_last_values_reg.at(ifIndex) = sum;
    count_reg.at(ifIndex) = ct;
}

uint32_t max(uint32_t v1,uint32_t v2){
    if(v1 > v2) return v1;
    else return v2;
}

uint32_t min(uint32_t v1,uint32_t v2){
    if(v1 < v2) return v1;
    else return v2;
}


int SwitchNode::GetOutDev(Ptr<const Packet> p, CustomHeader &ch){
	// look up entries
	auto entry = m_rtTable.find(ch.dip);

	// no matching entry
	if (entry == m_rtTable.end())
		return -1;

	// entry found
	auto &nexthops = entry->second;

	// pick one next hop based on hash
	union {
		uint8_t u8[4+4+2+2];
		uint32_t u32[3];
	} buf;
	buf.u32[0] = ch.sip;
	buf.u32[1] = ch.dip;
	if (ch.l3Prot == 0x6)
		buf.u32[2] = ch.tcp.sport | ((uint32_t)ch.tcp.dport << 16);
	else if (ch.l3Prot == 0x11)
		buf.u32[2] = ch.udp.sport | ((uint32_t)ch.udp.dport << 16);
	else if (ch.l3Prot == 0xFC || ch.l3Prot == 0xFD)
		buf.u32[2] = ch.ack.sport | ((uint32_t)ch.ack.dport << 16);

	uint32_t idx = EcmpHash(buf.u8, 12, m_ecmpSeed) % nexthops.size();
	return nexthops[idx];
}

void SwitchNode::CheckAndSendPfc(uint32_t inDev, uint32_t qIndex){
	Ptr<QbbNetDevice> device = DynamicCast<QbbNetDevice>(m_devices[inDev]);
	if (m_mmu->CheckShouldPause(inDev, qIndex)){
		device->SendPfc(qIndex, 0);
		m_mmu->SetPause(inDev, qIndex);
	}
}
void SwitchNode::CheckAndSendResume(uint32_t inDev, uint32_t qIndex){
	Ptr<QbbNetDevice> device = DynamicCast<QbbNetDevice>(m_devices[inDev]);
	if (m_mmu->CheckShouldResume(inDev, qIndex)){
		device->SendPfc(qIndex, 1);
		m_mmu->SetResume(inDev, qIndex);
	}
}

void SwitchNode::SendToDev(Ptr<Packet>p, CustomHeader &ch){
	int idx = GetOutDev(p, ch);
	if (idx >= 0){
		NS_ASSERT_MSG(m_devices[idx]->IsLinkUp(), "The routing table look up should return link that is up");

		// determine the qIndex
		uint32_t qIndex;
		if (ch.l3Prot == 0xFF || ch.l3Prot == 0xFE || (m_ackHighPrio && (ch.l3Prot == 0xFD || ch.l3Prot == 0xFC))){  //QCN or PFC or NACK, go highest priority
			qIndex = 0;
		}else{
			qIndex = (ch.l3Prot == 0x06 ? 1 : ch.udp.pg); // if TCP, put to queue 1
		}

		// admission control
		FlowIdTag t;
		p->PeekPacketTag(t);
		uint32_t inDev = t.GetFlowId();
		if (qIndex != 0){ //not highest priority
			if (m_mmu->CheckIngressAdmission(inDev, qIndex, p->GetSize()) && m_mmu->CheckEgressAdmission(idx, qIndex, p->GetSize())){			// Admission control
				m_mmu->UpdateIngressAdmission(inDev, qIndex, p->GetSize());
				m_mmu->UpdateEgressAdmission(idx, qIndex, p->GetSize());
			}else{
				return; // Drop
			}
			CheckAndSendPfc(inDev, qIndex);
		}
		m_bytes[inDev][idx][qIndex] += p->GetSize();
		m_devices[idx]->SwitchSend(qIndex, p, ch);
	}else
		return; // Drop
}

uint32_t SwitchNode::EcmpHash(const uint8_t* key, size_t len, uint32_t seed) {
  uint32_t h = seed;
  if (len > 3) {
    const uint32_t* key_x4 = (const uint32_t*) key;
    size_t i = len >> 2;
    do {
      uint32_t k = *key_x4++;
      k *= 0xcc9e2d51;
      k = (k << 15) | (k >> 17);
      k *= 0x1b873593;
      h ^= k;
      h = (h << 13) | (h >> 19);
      h += (h << 2) + 0xe6546b64;
    } while (--i);
    key = (const uint8_t*) key_x4;
  }
  if (len & 3) {
    size_t i = len & 3;
    uint32_t k = 0;
    key = &key[i - 1];
    do {
      k <<= 8;
      k |= *key--;
    } while (--i);
    k *= 0xcc9e2d51;
    k = (k << 15) | (k >> 17);
    k *= 0x1b873593;
    h ^= k;
  }
  h ^= len;
  h ^= h >> 16;
  h *= 0x85ebca6b;
  h ^= h >> 13;
  h *= 0xc2b2ae35;
  h ^= h >> 16;
  return h;
}

void SwitchNode::SetEcmpSeed(uint32_t seed){
	m_ecmpSeed = seed;
}

void SwitchNode::AddTableEntry(Ipv4Address &dstAddr, uint32_t intf_idx){
	uint32_t dip = dstAddr.Get();
	m_rtTable[dip].push_back(intf_idx);
}

void SwitchNode::ClearTable(){
	m_rtTable.clear();
}

// This function can only be called in switch mode
bool SwitchNode::SwitchReceiveFromDevice(Ptr<NetDevice> device, Ptr<Packet> packet, CustomHeader &ch){
	SendToDev(packet, ch);
	return true;
}

void SwitchNode::SwitchNotifyDequeue(uint32_t ifIndex, uint32_t qIndex, Ptr<Packet> p){
	FlowIdTag t;
	p->PeekPacketTag(t);
	if (qIndex != 0){
		uint32_t inDev = t.GetFlowId();
		m_mmu->RemoveFromIngressAdmission(inDev, qIndex, p->GetSize());
		m_mmu->RemoveFromEgressAdmission(ifIndex, qIndex, p->GetSize());
		m_bytes[inDev][ifIndex][qIndex] -= p->GetSize();
		if (m_ecnEnabled){
			bool egressCongested = m_mmu->ShouldSendCN(ifIndex, qIndex);
			if (egressCongested){
				PppHeader ppp;
				Ipv4Header h;
				p->RemoveHeader(ppp);
				p->RemoveHeader(h);
				h.SetEcn((Ipv4Header::EcnType)0x03);
				p->AddHeader(h);
				p->AddHeader(ppp);
			}
		}
		//CheckAndSendPfc(inDev, qIndex);
		CheckAndSendResume(inDev, qIndex);
	}
	if (1){
		uint8_t* buf = p->GetBuffer();
		if (buf[PppHeader::GetStaticSize() + 9] == 0x11){ // udp packet
			IntHeader *ih = (IntHeader*)&buf[PppHeader::GetStaticSize() + 20 + 8 + 6]; // ppp, ip, udp, SeqTs, INT
			Ptr<QbbNetDevice> dev = DynamicCast<QbbNetDevice>(m_devices[ifIndex]);
			if (m_ccMode == 3){ // HPCC
				ih->PushHop(Simulator::Now().GetTimeStep(), m_txBytes[ifIndex], dev->GetQueue()->GetNBytesTotal(), dev->GetDataRate().GetBitRate());
			}else if (m_ccMode == 10){ // HPCC-PINT
				uint64_t t = Simulator::Now().GetTimeStep();
				uint64_t dt = t - m_lastPktTs[ifIndex];
				if (dt > m_maxRtt)
					dt = m_maxRtt;
				uint64_t B = dev->GetDataRate().GetBitRate() / 8; //Bps
				uint64_t qlen = dev->GetQueue()->GetNBytesTotal();
				double newU;

				/**************************
				 * approximate calc
				 *************************/
				int b = 20, m = 16, l = 20; // see log2apprx's paremeters
				int sft = logres_shift(b,l);
				double fct = 1<<sft; // (multiplication factor corresponding to sft)
				double log_T = log2(m_maxRtt)*fct; // log2(T)*fct
				double log_B = log2(B)*fct; // log2(B)*fct
				double log_1e9 = log2(1e9)*fct; // log2(1e9)*fct
				double qterm = 0;
				double byteTerm = 0;
				double uTerm = 0;
				if ((qlen >> 8) > 0){
					int log_dt = log2apprx(dt, b, m, l); // ~log2(dt)*fct
					int log_qlen = log2apprx(qlen >> 8, b, m, l); // ~log2(qlen / 256)*fct
					qterm = pow(2, (
								log_dt + log_qlen + log_1e9 - log_B - 2*log_T
								)/fct
							) * 256;
					// 2^((log2(dt)*fct+log2(qlen/256)*fct+log2(1e9)*fct-log2(B)*fct-2*log2(T)*fct)/fct)*256 ~= dt*qlen*1e9/(B*T^2)
				}
				if (m_lastPktSize[ifIndex] > 0){
					int byte = m_lastPktSize[ifIndex];
					int log_byte = log2apprx(byte, b, m, l);
					byteTerm = pow(2, (
								log_byte + log_1e9 - log_B - log_T
								)/fct
							);
					// 2^((log2(byte)*fct+log2(1e9)*fct-log2(B)*fct-log2(T)*fct)/fct) ~= byte*1e9 / (B*T)
				}
				if (m_maxRtt > dt && m_u[ifIndex] > 0){
					int log_T_dt = log2apprx(m_maxRtt - dt, b, m, l); // ~log2(T-dt)*fct
					int log_u = log2apprx(int(round(m_u[ifIndex] * 8192)), b, m, l); // ~log2(u*512)*fct
					uTerm = pow(2, (
								log_T_dt + log_u - log_T
								)/fct
							) / 8192;
					// 2^((log2(T-dt)*fct+log2(u*512)*fct-log2(T)*fct)/fct)/512 = (T-dt)*u/T
				}
				newU = qterm+byteTerm+uTerm;

				#if 0
				/**************************
				 * accurate calc
				 *************************/
				double weight_ewma = double(dt) / m_maxRtt;
				double u;
				if (m_lastPktSize[ifIndex] == 0)
					u = 0;
				else{
					double txRate = m_lastPktSize[ifIndex] / double(dt); // B/ns
					u = (qlen / m_maxRtt + txRate) * 1e9 / B;
				}
				newU = m_u[ifIndex] * (1 - weight_ewma) + u * weight_ewma;
				printf(" %lf\n", newU);
				#endif

				/************************
				 * update PINT header
				 ***********************/
				uint16_t power = Pint::encode_u(newU);
				if (power > ih->GetPower())
					ih->SetPower(power);

				m_u[ifIndex] = newU;
			} else if (m_ccMode == 12){ // LINT
				Time now = Simulator::Now();
                uint32_t time = now.GetNanoSeconds();
                
                uint32_t amt_bytes;
                amt_bytes = pres_byte_cnt_reg.at(ifIndex);
                amt_bytes += p->GetSize();
				pres_byte_cnt_reg.at(ifIndex) = amt_bytes;

                uint32_t previousInsertion;
				previousInsertion = previous_insertion_reg.at(ifIndex).GetNanoSeconds();

                if (previousInsertion == 0) // Init previous insertion on first ts
                    {
                        previousInsertion = time;
                        previous_insertion_reg.at(ifIndex) = now;
                    }
                if (time - previousInsertion >= obs_window)
                    {
                        bool report = ReportMetrics(ifIndex, amt_bytes);

                        if (report)
                            {
								// std::cout << report << " "; // for testing
                                ih->PushHop(Simulator::Now().GetTimeStep(), m_txBytes[ifIndex], dev->GetQueue()->GetNBytesTotal(), dev->GetDataRate().GetBitRate());
                                previous_insertion_reg.at(ifIndex) = now;
                            }
						// previous_insertion_reg.at(ifIndex) = now; // test
                        pres_byte_cnt_reg.at(ifIndex) = 0;
                    }
            } else if (m_ccMode == 11){ // DINT
                // Get current simulator time
                Time now = Simulator::Now();
				Time obs_last_seen = obs_last_seen_reg.at(ifIndex);
				// If no tel_insertion_window, set it to min
				uint64_t val_tel_insertion_window;
				Time tel_insertion_window;
				if (tel_insertion_window.IsZero())
				{
					val_tel_insertion_window = Time(tel_insertion_min_window).GetNanoSeconds();
					tel_insertion_window_reg.at(ifIndex) = Time(val_tel_insertion_window);
				}
				
				// Get current and past amount of bytes
				uint32_t amt_packets, pres_amt_bytes, delta, past_amt_bytes;

				amt_packets = packets_cnt_reg.at(ifIndex)+1;
				packets_cnt_reg.at(ifIndex) = amt_packets;
				pres_amt_bytes = pres_byte_cnt_reg.at(ifIndex) + p->GetSize();
				pres_byte_cnt_reg.at(ifIndex) = pres_amt_bytes;
				telemetry_byte_cnt_reg.at(ifIndex) = telemetry_byte_cnt_reg.at(ifIndex) + p->GetSize();
				past_amt_bytes = past_byte_cnt_reg.at(ifIndex);
				// Set delta
				int32_t dint_delta = 0;
				if(delta_reg.at(ifIndex) == 0) {
					dint_delta = base_delta;
				} else {
					dint_delta = delta_reg.at(ifIndex);
				}
				delta_reg.at(ifIndex) = dint_delta;
                // pseudo code DINT
				// If no last time, then set it to now
				if (obs_last_seen.IsZero())
				{
					obs_last_seen_reg.at(ifIndex) = now;
					obs_last_seen = now;
				}
                if (now.GetNanoSeconds() - obs_last_seen.GetNanoSeconds() >= obs_window){
                    int32_t diff_bytes = pres_amt_bytes - past_amt_bytes;
					// std::cout << diff_bytes;
					// std::cout << "\n";
                    if (diff_bytes > dint_delta || diff_bytes < -1*dint_delta){
                        val_tel_insertion_window = tel_insertion_min_window;
                    } else {
                        val_tel_insertion_window = min(max_t, ((val_tel_insertion_window*alpha_1)>>alpha_2));
                    }
                    update_delta(ifIndex, pres_amt_bytes, dint_delta);
					past_byte_cnt_reg.at(ifIndex) = pres_amt_bytes;
					pres_byte_cnt_reg.at(ifIndex) = 0;
					// Update tel insertion window
					tel_insertion_window_reg.at(ifIndex) = Time(val_tel_insertion_window);
					obs_last_seen_reg.at(ifIndex) = now;
                    //
                }
				// Update telemetry insertion time
				Time previousInsertion = previous_insertion_reg.at(ifIndex);
				Time telInsertionWindow = tel_insertion_window_reg.at(ifIndex);

				if(previousInsertion.IsZero()){
					previousInsertion = now;
					previous_insertion_reg.at(ifIndex) = now;
				}
				
				if(now.GetNanoSeconds() - previousInsertion.GetNanoSeconds() >= telInsertionWindow.GetNanoSeconds()){
					 // Insert telemetry
					
                   	ih->PushHop(Simulator::Now().GetTimeStep(), m_txBytes[ifIndex], dev->GetQueue()->GetNBytesTotal(), dev->GetDataRate().GetBitRate());
					previous_insertion_reg.at(ifIndex) = now;
				}
            }
		}
	}
	m_txBytes[ifIndex] += p->GetSize();
	m_lastPktSize[ifIndex] = p->GetSize();
	m_lastPktTs[ifIndex] = Simulator::Now().GetTimeStep();
}

int SwitchNode::logres_shift(int b, int l){
	static int data[] = {0,0,1,2,2,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5};
	return l - data[b];
}

int SwitchNode::log2apprx(int x, int b, int m, int l){
	int x0 = x;
	int msb = int(log2(x)) + 1;
	if (msb > m){
		x = (x >> (msb - m) << (msb - m));
		#if 0
		x += + (1 << (msb - m - 1));
		#else
		int mask = (1 << (msb-m)) - 1;
		if ((x0 & mask) > (rand() & mask))
			x += 1<<(msb-m);
		#endif
	}
	return int(log2(x) * (1<<logres_shift(b, l)));
}

bool SwitchNode::ReportMetrics(uint32_t &flowId, uint32_t presAmtBytes) {    
    bool report = false;

    int32_t currentObs = presAmtBytes;

    uint32_t pastDeviceObs = past_device_obs_reg.at(flowId);
    uint32_t pastReportedObs = past_reported_obs_reg.at(flowId);

    int32_t latestDeviceObs = (currentObs - pastDeviceObs) >> alpha;
    latestDeviceObs = latestDeviceObs + pastDeviceObs;
    if (pastDeviceObs == 0)
    {
        latestDeviceObs = currentObs;
    }

    int32_t deviation = latestDeviceObs - pastReportedObs;
    if (deviation > (latestDeviceObs >> delta) || deviation < -1 * (latestDeviceObs >> delta))
    {
        report = true;

        int32_t latestReportedObs = (currentObs - pastReportedObs) >> alpha;
        latestReportedObs = latestReportedObs + pastReportedObs;
        if (pastReportedObs == 0)
        {
            latestReportedObs = currentObs;
        }
        past_reported_obs_reg.at(flowId) = latestReportedObs;
    }

    past_device_obs_reg.at(flowId) = latestDeviceObs;

    return report;
}



}