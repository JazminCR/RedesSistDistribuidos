#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>
#include <vector>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    int sizeNed;
    int oppositeNodeIndex;
    int clockOrAntiClockWise;
    int gate;
    std::vector<int> nodes;
public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    HelloPacket *hello = new HelloPacket();
    hello->setByteLength(28);
    hello->setDestination(this->getParentModule()->getIndex());
    hello->setTableArraySize(0);
    hello->setHello(true);
    clockOrAntiClockWise = 1;
    send(hello, "toLnk$o", clockOrAntiClockWise);
}

void Net::finish() {
}


void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;

    if (pkt->getHello()) {
        HelloPacket *hello = (HelloPacket*) msg;
        if (hello->getDestination()==this->getParentModule()->getIndex()) {
            hello->setTableArraySize(hello->getTableArraySize()+1);
            hello->setTable(hello->getTableArraySize()-1, this->getParentModule()->getIndex());
            sizeNed = hello->getTableArraySize();
            oppositeNodeIndex = sizeNed/2 - 1;
            for (int i = 0; i<sizeNed; i++) {
                nodes.push_back(hello->getTable(i));
            }
            delete(msg);
        }
        else {
            hello->setTableArraySize(hello->getTableArraySize()+1);
            hello->setTable(hello->getTableArraySize()-1, this->getParentModule()->getIndex());
            send(hello, "toLnk$o", clockOrAntiClockWise);
        }
    }
    else {

        // If this node is the final destination, send to App
        if (pkt->getDestination() == this->getParentModule()->getIndex()) {
           send(msg, "toApp$o");
        }

        // If not, forward the packet to some else... to who?
        else {
            // We send to link interface #0, which is the
            // one connected to the clockwise side of the ring
            // Is this the best choice? are there others?
            for (int i=0; i<sizeNed; i++) {
                if (pkt->getDestination()==nodes[i]) {
                    if (clockOrAntiClockWise) {
                        gate = (oppositeNodeIndex < i) ? (clockOrAntiClockWise - 1) : clockOrAntiClockWise;
                    } else {
                        gate = (oppositeNodeIndex <= i) ? (clockOrAntiClockWise + 1) : clockOrAntiClockWise;
                    }
                    send(msg, "toLnk$o", gate);
                    break;
                }
            }
        }
    }
}
