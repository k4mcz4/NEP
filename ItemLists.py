MINERAL_TYPE_LIST = [
    {"type_id": 34, "type_name": "Tritanium"},
    {"type_id": 35, "type_name": "Pyerite"},
    {"type_id": 36, "type_name": "Mexallon"},
    {"type_id": 37, "type_name": "Isogen"},
    {"type_id": 38, "type_name": "Nocxium"},
    {"type_id": 39, "type_name": "Zydrine"},
    {"type_id": 40, "type_name": "Megacyte"}
]

MOON_GOO_TYPE_LIST = [
    {"type_id": 16633, "type_name": "Hydrocarbons"},
    {"type_id": 16634, "type_name": "Atmospheric Gases"},
    {"type_id": 16635, "type_name": "Evaporite Deposits"},
    {"type_id": 16636, "type_name": "Silicates"},
    {"type_id": 16637, "type_name": "Tungsten"},
    {"type_id": 16638, "type_name": "Titanium"},
    {"type_id": 16639, "type_name": "Scandium"},
    {"type_id": 16640, "type_name": "Cobalt"},
    {"type_id": 16641, "type_name": "Chromium"},
    {"type_id": 16642, "type_name": "Vanadium"},
    {"type_id": 16643, "type_name": "Cadmium"},
    {"type_id": 16644, "type_name": "Platinum"},
    {"type_id": 16646, "type_name": "Mercury"},
    {"type_id": 16647, "type_name": "Caesium"},
    {"type_id": 16648, "type_name": "Hafnium"},
    {"type_id": 16649, "type_name": "Technetium"},
    {"type_id": 16650, "type_name": "Dysprosium"},
    {"type_id": 16651, "type_name": "Neodymium"},
    {"type_id": 16652, "type_name": "Promethium"},
    {"type_id": 16653, "type_name": "Thulium"}
]

INTERMEDIATE_TYPE_LIST = [
    {"type_id": 16654, "type_name": "Titanium Chromide"},
    {"type_id": 16655, "type_name": "Crystallite Alloy"},
    {"type_id": 16656, "type_name": "Fernite Alloy"},
    {"type_id": 16657, "type_name": "Rolled Tungsten Alloy"},
    {"type_id": 16658, "type_name": "Silicon Diborite"},
    {"type_id": 16659, "type_name": "Carbon Polymers"},
    {"type_id": 16660, "type_name": "Ceramic Powder"},
    {"type_id": 16661, "type_name": "Sulfuric Acid"},
    {"type_id": 16662, "type_name": "Platinum Technite"},
    {"type_id": 16663, "type_name": "Caesarium Cadmide"},
    {"type_id": 16664, "type_name": "Solerium"},
    {"type_id": 16665, "type_name": "Hexite"},
    {"type_id": 16666, "type_name": "Hyperflurite"},
    {"type_id": 16667, "type_name": "Neo Mercurite"},
    {"type_id": 16668, "type_name": "Dysporite"},
    {"type_id": 16669, "type_name": "Ferrofluid"},
    {"type_id": 17769, "type_name": "Fluxed Condensates"},
    {"type_id": 17959, "type_name": "Vanadium Hafnite"},
    {"type_id": 17960, "type_name": "Prometium"},
    {"type_id": 33336, "type_name": "Thulium Hafnite"},
    {"type_id": 33337, "type_name": "Promethium Mercurite"}
]

COMPOSITE_TYPE_LIST = [
    {"type_id": 16670, "type_name": "Crystalline Carbonide"},
    {"type_id": 16671, "type_name": "Titanium Carbide"},
    {"type_id": 16672, "type_name": "Tungsten Carbide"},
    {"type_id": 16673, "type_name": "Fernite Carbide"},
    {"type_id": 16678, "type_name": "Sylramic Fibers"},
    {"type_id": 16679, "type_name": "Fullerides"},
    {"type_id": 16680, "type_name": "Phenolic Composites"},
    {"type_id": 16681, "type_name": "Nanotransistors"},
    {"type_id": 16682, "type_name": "Hypersynaptic Fibers"},
    {"type_id": 16683, "type_name": "Ferrogel"},
    {"type_id": 17317, "type_name": "Fermionic Condensates"},
    {"type_id": 33359, "type_name": "Photonic Metamaterials"},
    {"type_id": 33360, "type_name": "Terahertz Metamaterials"},
    {"type_id": 33361, "type_name": "Plasmonic Metamaterials"},
    {"type_id": 33362, "type_name": "Nonlinear Metamaterials"}
]

FUEL_TYPE_LIST = [
    {"type_id": 4051, "type_name": "Nitrogen Fuel Block"},
    {"type_id": 4246, "type_name": "Hydrogen Fuel Block"},
    {"type_id": 4247, "type_name": "Helium Fuel Block"},
    {"type_id": 4312, "type_name": "Oxygen Fuel Block"}
]

INDUSTRY_ITEM_LIST = MINERAL_TYPE_LIST + \
                     MOON_GOO_TYPE_LIST + \
                     INTERMEDIATE_TYPE_LIST + \
                     COMPOSITE_TYPE_LIST + \
                     FUEL_TYPE_LIST


def industry_item_type_list():
    type_id_list = []
    for item_list in INDUSTRY_ITEM_ARRAY:
        for item in item_list:
            type_id_list.append(item["type_id"])

    return type_id_list


INDUSTRY_ITEM_ARRAY = [
    MINERAL_TYPE_LIST,
    MOON_GOO_TYPE_LIST,
    INTERMEDIATE_TYPE_LIST,
    COMPOSITE_TYPE_LIST,
    FUEL_TYPE_LIST
]

INDUSTRY_SEQUENCE = [
    "Minerals",
    "Moon Goo",
    "Intermediate Reactions",
    "Composite Reactions",
    "Fuel"
]
