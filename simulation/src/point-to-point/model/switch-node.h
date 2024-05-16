#ifndef SWITCH_NODE_H
#define SWITCH_NODE_H

#include <unordered_map>
#include <ns3/node.h>
#include "qbb-net-device.h"
#include "switch-mmu.h"
#include "pint.h"

namespace ns3 {

class Packet;

class SwitchNode : public Node{
	static const uint32_t pCnt = 257;	// Number of ports used
	static const uint32_t qCnt = 8;	// Number of queues/priorities used
	uint32_t m_ecmpSeed;
	std::unordered_map<uint32_t, std::vector<int> > m_rtTable; // map from ip address (u32) to possible ECMP port (index of dev)

	// monitor of PFC
	uint32_t m_bytes[pCnt][pCnt][qCnt]; // m_bytes[inDev][outDev][qidx] is the bytes from inDev enqueued for outDev at qidx
	
	uint64_t m_txBytes[pCnt]; // counter of tx bytes

	uint32_t m_lastPktSize[pCnt];
	uint64_t m_lastPktTs[pCnt]; // ns
	double m_u[pCnt];

protected:
	bool m_ecnEnabled;
	uint32_t m_ccMode;
	uint64_t m_maxRtt;
	Time last_obs;
	uint32_t m_ackHighPrio; // set high priority for ACK/NACK

private:
	int GetOutDev(Ptr<const Packet>, CustomHeader &ch);
	void SendToDev(Ptr<Packet>p, CustomHeader &ch);
	static uint32_t EcmpHash(const uint8_t* key, size_t len, uint32_t seed);
	void CheckAndSendPfc(uint32_t inDev, uint32_t qIndex);
	void CheckAndSendResume(uint32_t inDev, uint32_t qIndex);
	//For DINT
	void update_delta(uint32_t &flow_id, uint32_t comparator, uint32_t &delta);
	void update_telemetry_insertion_time(uint32_t &ifIndex, uint32_t pres_amt_bytes, uint32_t& delta);
	uint64_t dint_min(uint64_t v1,uint64_t v2);
	// LINT
	bool ReportMetrics(uint32_t &flowId, uint32_t presAmtBytes);
public:
	Ptr<SwitchMmu> m_mmu;

	static TypeId GetTypeId (void);
	SwitchNode();
	void SetEcmpSeed(uint32_t seed);
	void AddTableEntry(Ipv4Address &dstAddr, uint32_t intf_idx);
	void ClearTable();
	bool SwitchReceiveFromDevice(Ptr<NetDevice> device, Ptr<Packet> packet, CustomHeader &ch);
	void SwitchNotifyDequeue(uint32_t ifIndex, uint32_t qIndex, Ptr<Packet> p);

	// for approximate calc in PINT
	int logres_shift(int b, int l);
	int log2apprx(int x, int b, int m, int l); // given x of at most b bits, use most significant m bits of x, calc the result in l bits

	//DINT
	static const uint64_t tel_insertion_min_window = 1000;
	static const int64_t obs_window = 1000; // 1 Seg = 1000000 microseg
	static const uint64_t max_t = 10000;

	static const int64_t alpha_1 = 5;
	static const int8_t alpha_2 = 2; //shift divisor


	static const int32_t k = 8;
	static const int8_t div_shift = 3;

	/***************************************************************/

	static const int64_t div_10 = 0x1999999A; /// Used to divide a number by 10
	// static const int64_t div_100 = 0x28F5C29;
	static const int32_t base_delta = 300;
	std::array<uint32_t,pCnt> past_byte_cnt_reg;
	std::array<Time,pCnt> obs_last_seen_reg;
	std::array<Time,pCnt> tel_insertion_window_reg;
	std::array<uint32_t,pCnt> delta_reg;
	std::array<uint32_t,pCnt> n_last_values_reg;
	std::array<uint32_t,pCnt> count_reg;
	
	//end

	//LINT
	static const int64_t obs_window_lint = 1000;
	static const uint8_t alpha = 1; // Equals to 2^-1
	static const uint8_t delta = 6; // Equals to 2^-1

	std::array<uint32_t,pCnt> pres_byte_cnt_reg;
	std::array<uint32_t,pCnt> packets_cnt_reg;

	std::array<Time,pCnt> previous_insertion_reg;
	// std::array<uint64_t,pCnt> previous_bytes_reg; // For different PushHop approach

	std::array<uint32_t,pCnt> past_device_obs_reg;
	std::array<uint32_t,pCnt> past_reported_obs_reg;
	//end
};

} /* namespace ns3 */

#endif /* SWITCH_NODE_H */
