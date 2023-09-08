from CleWin_cif_creator import load_cif, write_to_cif, CleWin_layer
from example import example_layers

def get_shifted_alignment_mark(x_shift, y_shift, alignment_mark_layer_index):
    alignment_mark_filename = "centered_alignment_mark"
    alignment_mark_layers: list[CleWin_layer] = load_cif(filename = alignment_mark_filename)

    # get desired layer
    alignement_mark: CleWin_layer = alignment_mark_layers[alignment_mark_layer_index]

    # shift the entire layer by the desired amount
    alignement_mark.shift(shift_x_nm=x_shift, shift_y_nm=y_shift)

    # return list of shapes
    return alignement_mark.shapes

def aligned_example():
    hello_world_layers: list[CleWin_layer] = example_layers()
    metalization_layer = hello_world_layers[0]
    etch_layer = hello_world_layers[1]

    alignment_mark_positions = [[10e6, 10e6],
                                [-10e6, 10e6],
                                [10e6, -10e6],
                                [-10e6,-10e6]]

    for alignment_mark_position in alignment_mark_positions:
        # get shapes from above function
        metalization_alignement_mark_shapes = get_shifted_alignment_mark(
            x_shift=alignment_mark_position[0],
            y_shift=alignment_mark_position[1],
            alignment_mark_layer_index=0
        )
        etch_alignement_mark_shapes = get_shifted_alignment_mark(
            x_shift=alignment_mark_position[0],
            y_shift=alignment_mark_position[1],
            alignment_mark_layer_index=1
        )

        # add shapes to desired layers
        metalization_layer.shapes.extend(metalization_alignement_mark_shapes)
        etch_layer.shapes.extend(etch_alignement_mark_shapes)
        
        
    return [metalization_layer, etch_layer]
    

if __name__ == "__main__":
    aligned_layers = aligned_example()
    write_to_cif(filename = "aligned_hello_world", layers = aligned_layers)