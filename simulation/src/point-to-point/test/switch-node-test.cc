#include "ns3/test.h"
#include "ns3/drop-tail-queue.h"
#include "ns3/simulator.h"
#include "ns3/point-to-point-net-device.h"
#include "ns3/point-to-point-channel.h"
#include "ns3/switch-node.h"
#include "ns3/uinteger.h"

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
  Ptr<Packet> p = Create<Packet> ();
  sw->SetAttribute("CcMode", UintegerValue(11));	
  sw->SwitchNotifyDequeue (0, 0, p);
}


void
SwitchNodeTest::DoRun (void)
{
  Ptr<SwitchNode> sw = CreateObject<SwitchNode>();

  Simulator::Schedule (Seconds (1.0), &SwitchNodeTest::SendOnePacket, this, sw);

  Simulator::Run ();

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
