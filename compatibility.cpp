#include <iostream>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include "model_types.h"

using namespace std;

shared_ptr<apache::thrift::transport::TMemoryBuffer> encode_old_car()
{
    OldCar car;
    car.brand = "Honda";
    car.model = "Accord";
    car.fuel = OldFuel::gasoline;
    car.weight = 2200;
    car.__isset.weight = true;
    car.wheels = 4;
    car.__isset.wheels = true;
    cout << "old_car = " << car << endl;
    shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer(
        new apache::thrift::transport::TMemoryBuffer());
    apache::thrift::protocol::TBinaryProtocolFactoryT<apache::thrift::transport::TMemoryBuffer>
        protocol_factory;
    shared_ptr<apache::thrift::protocol::TProtocol> protocol = protocol_factory.getProtocol(buffer);
    try {
        buffer->resetBuffer();
        car.write(protocol.get());
        return buffer;
    } catch (std::exception& e) {
        cout << "Couldn't encode old_car: " << e.what() << endl;
        return 0;
    }
}

void decode_old_car(shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer)
{
    apache::thrift::protocol::TBinaryProtocolFactoryT<apache::thrift::transport::TMemoryBuffer>
        protocol_factory;
    shared_ptr<apache::thrift::protocol::TProtocol> protocol = protocol_factory.getProtocol(buffer);
    try {
        OldCar car;
        car.read(protocol.get());
        cout << "old_car = " << car << endl;
    } catch (std::exception& e) {
        cout << "Couldn't decode old_car: " << e.what() << endl;
    }
}

shared_ptr<apache::thrift::transport::TMemoryBuffer> encode_new_car()
{
    NewColorScheme color_scheme;
    color_scheme.interior_color = "Beige";
    color_scheme.exterior_color = "Red";
    NewCar car;
    car.brand = "Toyota";
    car.model = "Camry";
    car.fuel = NewFuel::electric;
    car.weight = 2400;
    car.__isset.weight = true;
    car.wheels = 4;
    car.__isset.wheels = true;
    car.height = 170;
    car.__isset.height = true;
    car.doors = 2;
    car.__isset.doors = true;
    car.color_scheme = color_scheme;
    car.__isset.color_scheme = true;
    cout << "new_car = " << car << endl;
    shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer(
        new apache::thrift::transport::TMemoryBuffer());
    apache::thrift::protocol::TBinaryProtocolFactoryT<apache::thrift::transport::TMemoryBuffer>
        protocol_factory;
    shared_ptr<apache::thrift::protocol::TProtocol> protocol = protocol_factory.getProtocol(buffer);
    try {
        buffer->resetBuffer();
        car.write(protocol.get());
        return buffer;
    } catch (std::exception& e) {
        cout << "Couldn't encode new_car: " << e.what() << endl;
        return 0;
    }
}

void decode_new_car(shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer)
{
    apache::thrift::protocol::TBinaryProtocolFactoryT<apache::thrift::transport::TMemoryBuffer>
        protocol_factory;
    shared_ptr<apache::thrift::protocol::TProtocol> protocol = protocol_factory.getProtocol(buffer);
    try {
        NewCar car;
        car.read(protocol.get());
        cout << "new_car = " << car << endl;
    } catch (std::exception& e) {
        cout << "Couldn't decode new_car: " << e.what() << endl;
    }
}

void check_backward_compatibility()
{
    cout << "** Checking backward compatibility: good new code can receive old messages **" << endl;
    shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer = encode_old_car();
    decode_new_car(buffer);
}

void check_forward_compatibility()
{
    cout << "** Checking forward compatibility: old code can receive new messages **" << endl;
    shared_ptr<apache::thrift::transport::TMemoryBuffer> buffer = encode_new_car();
    decode_old_car(buffer);
}

int main()
{
    check_backward_compatibility();
    check_forward_compatibility();
    return 0;
}
