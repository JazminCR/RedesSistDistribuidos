packet Packet {
    int source;
    int destination;
    int hopCount;
    bool hello;
}

packet HelloPacket extends Packet {
    int table[];
}