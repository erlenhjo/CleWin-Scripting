from CleWin_cif_creator import CleWin_color, CIF_rectangle, CleWin_layer, write_to_cif


def example_layers():
    metalization_layer = CleWin_layer(
        layer_name="Metalization",
        layer_alias="L0",
        layer_index=0,
        fill_color=CleWin_color(int("0x39", 0), int("0x9a", 0), int("0xd5", 0)),
        border_color=CleWin_color(0, 255, 0),
    )

    etch_layer = CleWin_layer(
        layer_name="Etch",
        layer_alias="L1",
        layer_index=1,
        fill_color=CleWin_color(255, 0, 0),
        border_color=CleWin_color(0, 0, 255),
    )

    square1 = CIF_rectangle(
        x_size_nm=200e3, y_size_nm=1000e3, x_center_nm=-800e3, y_center_nm=0
    )
    square2 = CIF_rectangle(
        x_size_nm=200e3, y_size_nm=1000e3, x_center_nm=-400e3, y_center_nm=0
    )

    square3 = CIF_rectangle(
        x_size_nm=200e3, y_size_nm=1000e3, x_center_nm=100e3, y_center_nm=0
    )
    square4 = CIF_rectangle(
        x_size_nm=200e3, y_size_nm=200e3, x_center_nm=-600e3, y_center_nm=0
    )

    metalization_layer.add_shape_to_layer(shape=square1)
    metalization_layer.add_shape_to_layer(shape=square2)

    etch_layer.add_shape_to_layer(shape=square3)
    etch_layer.add_shape_to_layer(shape=square4)

    layers = [metalization_layer, etch_layer]

    return layers


if __name__ == "__main__":
    layers = example_layers()
    filename = "hello_world"
    write_to_cif(filename=filename, layers=layers)
