import copy

class CleWin_color(object):
    def __init__(self, red: int, green: int, blue:int):
        if red < 0 or red > 255:
            raise "Color channels must have value between 0 and 255"
        if green < 0 or green > 255:
            raise "Color channels must have value between 0 and 255"
        if blue < 0 or blue > 255:
            raise "Color channels must have value between 0 and 255"
        
        self.red = int(red)
        self.green = int(green)
        self.blue = int(blue)

    def format_color_for_CleWin(self):
        return f"0f{format(self.blue, '02x')}{format(self.green, '02x')}{format(self.red, '02x')}"


class CleWin_square(object):
    def __init__(self, x_size_nm, y_size_nm, x_center_nm, y_center_nm):
        self.x_size_nm = x_size_nm
        self.y_size_nm = y_size_nm
        self.x_center_nm = x_center_nm
        self.y_center_nm = y_center_nm

    def get_CleWin_line(self):
        return f"B {int(self.x_size_nm)} {int(self.y_size_nm)} {int(self.x_center_nm)} {int(self.y_center_nm)};\n"

    def shift(self, shift_x_nm, shift_y_nm):
        self.x_center_nm += shift_x_nm
        self.y_center_nm += shift_y_nm

    def deepcopy(self):
        return copy.deepcopy(self)


class Clewin_polygon(object):
    def __init__(self, points):
        self.points = points
        
    def get_CleWin_line(self):
        string = "P"
        for point in self.points:
            x_coord = int(point[0])
            y_coord = int(point[1])
            string += f" {x_coord} {y_coord}"
        string += ";\n"

        return string 
    
    def shift(self, shift_x_nm, shift_y_nm):
        for n in range(len(self.points)):
            self.points[n][0] += shift_x_nm
            self.points[n][1] += shift_y_nm

    def deepcopy(self):
        return copy.deepcopy(self)


class CleWin_layer(object):
    def __init__(self, layer_name: str, layer_alias: str, layer_index: int, fill_color: CleWin_color, border_color: CleWin_color):
        self.layer_name = layer_name
        self.layer_alias = layer_alias
        self.layer_index = layer_index
        self.fill_color = fill_color
        self.border_color = border_color
        self.shapes: list[CleWin_square] = []   # only squares for now

    def add_shape_to_layer(self, shape: CleWin_square|Clewin_polygon):
        self.shapes.append(shape)

    def get_cif_declaration(self):
        fill_color_str = self.fill_color.format_color_for_CleWin()
        border_color_str = self.border_color.format_color_for_CleWin()

        cif_declaration = ""
        cif_declaration += f"L {self.layer_alias};\n"
        cif_declaration += f"(CleWin: {self.layer_index} {self.layer_name}/{fill_color_str} {border_color_str});\n"
        
        return cif_declaration

    def get_cif_content(self):
        cif_content = ""
        cif_content += f"L {self.layer_alias};\n"

        for shape in self.shapes:
            cif_content += shape.get_CleWin_line()

        return cif_content
    
    def deepcopy(self):
        return copy.deepcopy(self)

    def shift(self, shift_x_nm, shift_y_nm):
        for shape in self.shapes:
            shape.shift(shift_x_nm, shift_y_nm)



def write_to_cif(filename, layers:list[CleWin_layer]):
    cif = ""
    cif += "(CIF written for use with CleWin 4.1);\n"

    cif += "(Layer names:);\n"
    for layer in layers:
        cif += layer.get_cif_declaration()

    cif += "(Top level:);\n"
    cif += "DS1 1 10;\n"
    cif += "9 MainSymbol;\n"

    for layer in layers:
        cif += layer.get_cif_content()

    cif += "DF;\n"
    cif += "C 1;\n"
    cif += "E"

    with open(file=f"{filename}.cif", mode = "w") as file:
        file.write(cif)


def load_cif(filename):
    with open(file=f"{filename}.cif", mode = "r") as file:
        cif = file.read()

    cif = cif.split("DF;")[0]
    cif = cif.split("(Layer names:);\n")[1]
    layer_info = cif.split("(Top level:);\n")[0]
    shape_info = cif.split("(Top level:);\n")[1]
    
    layers = []
    for layer_info_string in layer_info.split("L ")[1:]:
        layer: CleWin_layer = layer_from_cif_string(layer_info_string)
        layers.append(layer)

    for layer_shapes_string in shape_info.split("L ")[1:]:
        layer_alias = layer_shapes_string.split(";\n")[0]
        shape_strings = layer_shapes_string.split(";\n")[1:-1]
        shapes = shapes_from_string(shape_strings)
        for layer in layers:
            if layer_alias == layer.layer_alias:
                for shape in shapes:
                    layer.add_shape_to_layer(shape)

    return layers
            
    
def shapes_from_string(shape_strings):
    shapes = []
    
    for shape_string in shape_strings:
        if shape_string[0] == "B":
            values = shape_string.split(" ")[1:]
            x_size = int(values[0])
            y_size = int(values[1])
            x_center = int(values[2])
            y_center = int(values[3])
            square = CleWin_square(
                x_size_nm = x_size,
                y_size_nm = y_size,
                x_center_nm = x_center,
                y_center_nm = y_center
            )
            shapes.append(square)

        elif shape_string[0] == "P":
            value_strings = shape_string.split(" ")[1:]
            values = []
            for value_string in value_strings:
                value_string = value_string.strip("\n")
                values.append(int(value_string))

            points = []
            for x_coord, y_coord in zip(values[::2],values[1::2]):
                point = [x_coord, y_coord]
                points.append(point)
            
            polygon = Clewin_polygon(points = points)
            shapes.append(polygon)
        else:
            raise f"Unsupported shape: {shape_string}"
        
    return shapes

def color_from_cif_string(color_string):
    red = int(f"0x{color_string[2:4]}",base=0)
    green = int(f"0x{color_string[4:6]}",base=0)
    blue = int(f"0x{color_string[6:8]}",base=0)

    return CleWin_color(red, green, blue)

def layer_from_cif_string(layer_string):
    alias = layer_string.split(";")[0]

    layer_string = layer_string.split(";")[1]
    layer_string = layer_string.split("(")[1]
    layer_string = layer_string.split(")")[0]

    index = int(layer_string.split("/")[0].split(" ")[1])
    name = " ".join(layer_string.split("/")[0].split(" ")[2:])
    fill_color_string = layer_string.split("/")[1].split(" ")[0]
    border_color_string = layer_string.split("/")[1].split(" ")[1]
    fill_color = color_from_cif_string(fill_color_string)
    border_color = color_from_cif_string(border_color_string)
    
    layer = CleWin_layer(
        layer_name = name, 
        layer_alias = alias, 
        layer_index = index, 
        fill_color = fill_color, 
        border_color = border_color
    )

    return layer

    

    














