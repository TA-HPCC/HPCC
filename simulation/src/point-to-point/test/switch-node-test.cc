#include "ns3/test.h"
#include "ns3/drop-tail-queue.h"
#include "ns3/simulator.h"
#include "ns3/point-to-point-net-device.h"
#include "ns3/point-to-point-channel.h"
#include "ns3/switch-node.h"
#include "ns3/uinteger.h"
#include <ns3/seq-ts-header.h>
#include <ns3/udp-header.h>
#include <ns3/ipv4-header.h>
#include "ns3/ppp-header.h"
#include "ns3/qbb-net-device.h"
#include "ns3/broadcom-egress-queue.h"
#include "ns3/data-rate.h"

namespace ns3 {

class SwitchNodeTestBase : public TestCase
{
public:
  SwitchNodeTestBase (std::string name, uint32_t ccMode);

  virtual void DoRun (void);

private:
  void SendOnePacket (Ptr<SwitchNode> sw);
  void SwitchNotifyDequeueWithStep (Ptr<SwitchNode> sw, Ptr<Packet> p);
  uint32_t m_ccMode;
};

SwitchNodeTestBase::SwitchNodeTestBase (std::string name, uint32_t ccMode)
  : TestCase (name),
    m_ccMode (ccMode)
{
}

void SwitchNodeTestBase::SwitchNotifyDequeueWithStep (Ptr<SwitchNode> sw, Ptr<Packet> p)
{
  sw->SwitchNotifyDequeue (0, 0, p);
}

void
SwitchNodeTestBase::SendOnePacket (Ptr<SwitchNode> sw)
{
  Ptr<Packet> p = Create<Packet> (1096);

  UdpHeader udpHeader;
  udpHeader.SetDestinationPort (0);
  udpHeader.SetSourcePort (0);
  p->AddHeader (udpHeader);
  // add ipv4 header
  Ipv4Header ipHeader;
  ipHeader.SetSource (Ipv4Address(1));
  ipHeader.SetDestination (Ipv4Address(2));
  ipHeader.SetProtocol (0x11);
  ipHeader.SetPayloadSize (p->GetSize());
  ipHeader.SetTtl (64);
  ipHeader.SetTos (0);
  p->AddHeader(ipHeader);
  // add ppp header
  PppHeader ppp;
  ppp.SetProtocol (0x0021); // EtherToPpp(0x800), see point-to-point-net-device.cc
  p->AddHeader (ppp);

  DataRate defaultRate;
  Ptr<QbbNetDevice> dev = CreateObject<QbbNetDevice>();
  dev->SetAddress (Mac48Address::Allocate ());
  dev->SetQueue (CreateObject<BEgressQueue> ());
  dev->SetDataRate (defaultRate);
  sw->AddDevice(dev);

  sw->SetAttribute("CcMode", UintegerValue(m_ccMode));
  if (m_ccMode == 11){
	for (size_t i = 0; i < 16; i++)
	{
		Simulator::Schedule (NanoSeconds (1+i), &SwitchNodeTestBase::SwitchNotifyDequeueWithStep, this, sw, p);
	}

	
  }
  else {
  for (size_t i = 0; i < 16; i++)
	{
		Simulator::Schedule (NanoSeconds (1+i), &SwitchNodeTestBase::SwitchNotifyDequeueWithStep, this, sw, p);
	}
  }
  
}

void
SwitchNodeTestBase::DoRun (void)
{
  Ptr<SwitchNode> sw = CreateObject<SwitchNode>();

  Simulator::Schedule (Seconds (0), &SwitchNodeTestBase::SendOnePacket, this, sw);

  Simulator::Run ();
	 
  if (m_ccMode == 11){ //DINT Test
	// Test if function is called
	NS_TEST_EXPECT_MSG_NE(sw->packets_cnt_reg.at(0), 0, "update_telemetry_insertion_time function not called");
	NS_TEST_EXPECT_MSG_NE(sw->obs_last_seen_reg.at(0), 0, "update_telemetry_insertion_time function not called");
	NS_TEST_EXPECT_MSG_NE(sw->count_reg.at(0), 0, "update_delta function not called");
	
	//Logic test
	NS_TEST_EXPECT_MSG_NE(sw->delta_reg.at(0), 300, "delta is not updated");
	NS_TEST_EXPECT_MSG_EQ(sw->packets_cnt_reg.at(0), 16, "wrong packet count");
	NS_TEST_EXPECT_MSG_EQ((sw->previous_insertion_reg.at(0)).GetNanoSeconds(), 16, "last insertion is not at last nanosec");

  }	
  else { //LINT Test
  NS_TEST_EXPECT_MSG_NE(sw->past_device_obs_reg.at(0), 0, "ReportMetrics function not called");
  NS_TEST_EXPECT_MSG_NE(sw->past_reported_obs_reg.at(0), 0, "ReportMetrics function not called");
  NS_TEST_EXPECT_MSG_NE(sw->previous_insertion_reg.at(0), 0, "previous insertion is not updated");

  }
  Simulator::Destroy ();
}

class SwitchNodeTestDINT : public SwitchNodeTestBase
{
public:
  SwitchNodeTestDINT ()
    : SwitchNodeTestBase ("SwitchNodeTestDINT", 11)
  {
  }
};

class SwitchNodeTestLINT : public SwitchNodeTestBase
{
public:
  SwitchNodeTestLINT ()
    : SwitchNodeTestBase ("SwitchNodeTestLINT", 12)
  {
  }
};

class SwitchNodeTestSuite : public TestSuite
{
public:
  SwitchNodeTestSuite ();
};

SwitchNodeTestSuite::SwitchNodeTestSuite ()
  : TestSuite ("switch-node", UNIT)
{
  AddTestCase (new SwitchNodeTestDINT);
  AddTestCase (new SwitchNodeTestLINT);
}

static SwitchNodeTestSuite g_SwitchNodeTestSuite;

} // namespace ns3
