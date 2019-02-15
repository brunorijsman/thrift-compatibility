# Old model

enum OldFuel {
    gasoline = 0,
    diesel = 1
}

struct OldCar {
    1: required string brand;
    2: required string model;
    3: required OldFuel fuel;
    4: optional i16 weight;
    5: optional i16 wheels = 4;
}

# New model

enum NewFuel {
    gasoline = 0,
    diesel = 1,
    electric = 2                # New enum value
}

struct NewColorScheme {         # New struct (used as new optional field in NewCar)
    1: required string interior_color;
    2: required string exterior_color;
}

struct NewCar {
    1: required string brand;
    2: required string model;
    3: required NewFuel fuel;
    4: optional i16 weight;
    5: optional i16 wheels = 4;
    6: optional i16 height;                     # New optional field  
    7: optional i16 doors = 4;                  # New optional field with default value
    8: optional NewColorScheme color_scheme;    # New optional field using new structure
}

