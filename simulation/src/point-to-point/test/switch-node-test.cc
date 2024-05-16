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

class SwitchNodeTest : public TestCase
{
public:
  SwitchNodeTest ();

  virtual void DoRun (void);

private:
  void SendOnePacket (Ptr<SwitchNode> sw);
};

SwitchNodeTest::SwitchNodeTest ()
  : TestCase ("SwitchNode")
{
}

void
SwitchNodeTest::SendOnePacket (Ptr<SwitchNode> sw)
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
  // ipHeader.SetIdentification (qp->m_ipid);
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
  
  sw->SetAttribute("CcMode", UintegerValue(12));  
  sw->SwitchNotifyDequeue (0, 0, p);
}


void
SwitchNodeTest::DoRun (void)
{
  Ptr<SwitchNode> sw = CreateObject<SwitchNode>();

  Simulator::Schedule (Seconds (1.0), &SwitchNodeTest::SendOnePacket, this, sw);

  Simulator::Run ();
  NS_TEST_ASSERT_MSG_EQ(sw->delta_reg[0], 0, "Some failure message");
  Simulator::Destroy ();
}
//-----------------------------------------------------------------------------
class SwitchNodeTestSuite : public TestSuite
{
public:
  SwitchNodeTestSuite ();
};

SwitchNodeTestSuite::SwitchNodeTestSuite ()
  : TestSuite ("switch-node", UNIT)
{
  AddTestCase (new SwitchNodeTest);
}

static SwitchNodeTestSuite g_SwitchNodeTestSuite;

} // namespace ns3
