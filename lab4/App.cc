#ifndef APP
#define APP

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class App: public cSimpleModule {
private:
    cMessage *sendMsgEvent;
    cStdDev delayStats;
    cOutVector delayVector;
    cStdDev hopCountStats;
    cOutVector hopCountVector;
    cOutVector countVector;
public:
    App();
    virtual ~App();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(App);

#endif /* APP */

App::App() {
}

App::~App() {
}

void App::initialize() {

    // If interArrivalTime for this node is higher than 0
    // initialize packet generator by scheduling sendMsgEvent
    if (par("interArrivalTime").doubleValue() != 0) {
        sendMsgEvent = new cMessage("sendEvent");
        scheduleAt(par("interArrivalTime"), sendMsgEvent);
    }

    // Initialize statistics
    delayStats.setName("TotalDelay");
    delayVector.setName("Delay");
    hopCountStats.setName("TotalHopCount");
    hopCountVector.setName("HopCount");
    countVector.setName("Send");
}

void App::finish() {
    // Record statistics
    recordScalar("Average delay", delayStats.getMean());
    recordScalar("Number of packets", delayStats.getCount());
    recordScalar("Average hop count", hopCountStats.getMean());
}

void App::handleMessage(cMessage *msg) {

    // if msg is a sendMsgEvent, create and send new packet
    if (msg == sendMsgEvent) {
        // create new packet
        Packet *pkt = new Packet("packet",this->getParentModule()->getIndex());
        pkt->setByteLength(par("packetByteSize"));
        pkt->setSource(this->getParentModule()->getIndex());
        pkt->setDestination(par("destination"));
        pkt->setHopCount(0);
        pkt->setHello(false);
        countVector.record(1);
        // send to net layer
        send(pkt, "toNet$o");

        // compute the new departure time and schedule next sendMsgEvent
        simtime_t departureTime = simTime() + par("interArrivalTime");
        scheduleAt(departureTime, sendMsgEvent);

    }
    // else, msg is a packet from net layer
    else {
        // compute delay and record statistics
        simtime_t delay = simTime() - msg->getCreationTime();
        delayStats.collect(delay);
        delayVector.record(delay);
        Packet *pkt = (Packet *) msg;
        hopCountStats.collect(pkt->getHopCount());
        hopCountVector.record(pkt->getHopCount());
        // delete msg
        delete (msg);
    }

}
