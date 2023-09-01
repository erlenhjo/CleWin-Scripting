class CleWin_color(object):
    def __init__(self, red: int, green: int, blue:int):
        if red < 0 or red > 255:
            raise "Color channels must have value between 0 and 255"
        if green < 0 or green > 255:
            raise "Color channels must have value between 0 and 255"
        if blue < 0 or blue > 255:
            raise "Color chennels must have value between 0 and 255"
        
        self.red = red
        self.green = green
        self.blue = blue

    def format_color_for_CleWin(self):
        return f"0f{format(self.red, '02x')}{format(self.green, '02x')}{format(self.blue, '02x')}"



class CleWin_square(object):
    def __init__(self, x_size_nm, y_size_nm, x_center_nm, y_center_nm):
        self.x_size_nm = x_size_nm
        self.y_size_nm = y_size_nm
        self.x_center_nm = x_center_nm
        self.y_center_nm = y_center_nm

    def get_CleWin_line(self):
        return f"B {int(self.x_size_nm)} {int(self.y_size_nm)} {int(self.x_center_nm)} {int(self.y_center_nm)};\n"



class CleWin_layer(object):
    def __init__(self, layer_name: str, layer_alias: str, layer_index: int, fill_color: CleWin_color, border_color: CleWin_color):
        self.layer_name = layer_name
        self.layer_alias = layer_alias
        self.layer_index = layer_index
        self.fill_color = fill_color
        self.border_color = border_color
        self.shapes: list[CleWin_square] = []   # only squares for now

    def add_square_to_layer(self, square: CleWin_square):
        self.shapes.append(square)

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


def write_to_cif(filename, layers:list[CleWin_layer]):
    cif = ""
    cif += "(CIF written by CleWin 4.1);\n"

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