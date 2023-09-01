from CleWin_cif_creator import CleWin_color, CleWin_square, CleWin_layer, write_to_cif

metalization_layer = CleWin_layer(
    layer_name = "Metalization",
    layer_alias = "L0",
    layer_index = 0,
    fill_color = CleWin_color(128, 128, 128),
    border_color = CleWin_color(0, 0, 255) 
    )

etch_layer = CleWin_layer(
    layer_name = "Etch",
    layer_alias = "L1",
    layer_index = 1,
    fill_color = CleWin_color(0, 255, 0),
    border_color = CleWin_color(255, 0, 0) 
    )

square1 = CleWin_square(
    x_size_nm = 200e3, 
    y_size_nm = 1000e3,
    x_center_nm = 100e3,
    y_center_nm  = 0
    )
square2 = CleWin_square(
    x_size_nm = 200e3, 
    y_size_nm = 200e3,
    x_center_nm = -600e3,
    y_center_nm  = 0
    )

square3 = CleWin_square(
    x_size_nm = 200e3, 
    y_size_nm = 1000e3,
    x_center_nm = -800e3,
    y_center_nm  = 0
    )
square4 = CleWin_square(
    x_size_nm = 200e3, 
    y_size_nm = 1000e3,
    x_center_nm = -400e3,
    y_center_nm  = 0
    )

etch_layer.add_square_to_layer(square = square1)
etch_layer.add_square_to_layer(square = square2)

metalization_layer.add_square_to_layer(square = square3)
metalization_layer.add_square_to_layer(square = square4)
    
layers = [etch_layer, metalization_layer]

filename = "hello_world"
write_to_cif(filename = filename, layers = layers)

