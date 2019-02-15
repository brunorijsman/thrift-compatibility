import model.ttypes

import thrift.protocol.TBinaryProtocol
import thrift.transport.TTransport

def make_old_car():
    car = model.ttypes.OldCar(brand="Honda",
                              model="Accord",
                              fuel=model.ttypes.OldFuel.gasoline,
                              weight=2200,
                              wheels=4)
    return car

def make_new_car():
    color_scheme = model.ttypes.NewColorScheme(interior_color="Beige",
                                               exterior_color="Red")
    car = model.ttypes.NewCar(brand="Toyota",
                              model="Camry",
                              fuel=model.ttypes.NewFuel.electric,   # New enum value
                              weight=2400,
                              wheels=4,
                              height=170,                 # New optional field
                              doors=2,                    # New optional field with default value
                              color_scheme=color_scheme)  # New optional field using new struct
    return car

def make_bad_car():
    car = model.ttypes.BadCar(brand="Porsche",
                              model="Carrera",
                              fuel=model.ttypes.OldFuel.gasoline,
                              weight=1800,
                              wheels=4,
                              max_speed=240);             # New required field
    return car

def encode_car(car):
    transport_out = thrift.transport.TTransport.TMemoryBuffer()
    protocol_out = thrift.protocol.TBinaryProtocol.TBinaryProtocol(transport_out)
    car.write(protocol_out)
    encoded_car = transport_out.getvalue()
    return encoded_car

def decode_as_old_car(encoded_car):
    transport_in = thrift.transport.TTransport.TMemoryBuffer(encoded_car)
    protocol_in = thrift.protocol.TBinaryProtocol.TBinaryProtocol(transport_in)
    old_car = model.ttypes.OldCar()
    try:
        old_car.read(protocol_in)
    except Exception as exception:
        print("old_car decoding failed:", exception)
        return None
    return old_car

def decode_as_new_car(encoded_car):
    transport_in = thrift.transport.TTransport.TMemoryBuffer(encoded_car)
    protocol_in = thrift.protocol.TBinaryProtocol.TBinaryProtocol(transport_in)
    new_car = model.ttypes.NewCar()
    try:
        new_car.read(protocol_in)
    except Exception as exception:
        print("new_car decoding failed:", exception)
        return None
    return new_car

def decode_as_bad_car(encoded_car):
    transport_in = thrift.transport.TTransport.TMemoryBuffer(encoded_car)
    protocol_in = thrift.protocol.TBinaryProtocol.TBinaryProtocol(transport_in)
    bad_car = model.ttypes.BadCar()
    try:
        bad_car.read(protocol_in)
    except Exception as exception:
        print("bad_car decoding failed:", exception)
        return None
    return bad_car

def check_new_rx_old():
    print("** Checking backward compatibility: good new code can receive old messages **")
    old_car = make_old_car()
    print("old_car =", old_car)
    encoded_old_car = encode_car(old_car)
    new_car = decode_as_new_car(encoded_old_car)
    if new_car is None:
        print("could not decode as new_car")
    else:
        print("new_car =", new_car)
        try:
            new_car.validate()
        except Exception as exception:
            print("new_car validation failed:", exception)
        else:
            print("new_car validation ok")

def check_old_rx_new():
    print("** Checking forward compatibility: old code can receive good new messages **")
    new_car = make_new_car()
    print("new_car =", new_car)
    encoded_new_car = encode_car(new_car)
    old_car = decode_as_old_car(encoded_new_car)
    if old_car is None:
        print("could not decode as old_car")
    else:
        print("old_car =", old_car)
        try:
            old_car.validate()
        except Exception as exception:
            print("old car validation failed:", exception)
        else:
            print("old_car validation ok")

def check_bad_rx_old():
    print("** Checking backward compatibility: bad new code can receive old messages **")
    old_car = make_old_car()
    print("old_car =", old_car)
    encoded_old_car = encode_car(old_car)
    bad_car = decode_as_bad_car(encoded_old_car)
    if bad_car is None:
        print("could not decode as bad_car")
    else:
        print("bad_car =", bad_car)
        try:
            bad_car.validate()
        except Exception as exception:
            print("bad_car validation failed:", exception)
        else:
            print("bad_car validation ok")

def check_old_rx_bad():
    print("** Checking forward compatibility: old code can receive bad new messages **")
    bad_car = make_bad_car()
    print("bad_car =", bad_car)
    encoded_bad_car = encode_car(bad_car)
    old_car = decode_as_old_car(encoded_bad_car)
    if old_car is None:
        print("could not decode as old_car")
    else:
        print("old_car =", old_car)
        try:
            old_car.validate()
        except Exception as exception:
            print("old car validation failed:", exception)
        else:
            print("old_car validation ok")

if __name__ == "__main__":
    check_new_rx_old()
    check_old_rx_new()
    check_bad_rx_old()
    check_old_rx_bad()
