from CleWin_cif_creator import load_cif, write_to_cif, CleWin_layer
from example import example_layers

def aligned_example():
    alignment_mark_filename = "centered_alignment_mark"
    alignment_mark_layers: list[CleWin_layer] = load_cif(filename = alignment_mark_filename)
    alignement_mark_metalization = alignment_mark_layers[0]
    alignement_mark_etch = alignment_mark_layers[1]

    hello_world_layers: list[CleWin_layer] = example_layers()
    metalization_layer = hello_world_layers[0]
    etch_layer = hello_world_layers[1]

    alignment_mark_positions = [[10e6, 10e6],
                                [-10e6, 10e6],
                                [10e6, -10e6],
                                [-10e6,-10e6]]

    for alignment_mark_position in alignment_mark_positions:
        shift_x = alignment_mark_position[0]
        shift_y = alignment_mark_position[1]
        
        # for each layer
        for shape in alignement_mark_metalization.shapes:
            # take a deep copy of each shape 
            new_shape = shape.deepcopy()
            # and move it to the correct position
            new_shape.shift(shift_x_nm=shift_x, shift_y_nm=shift_y)
            # then add it to the desired layer
            metalization_layer.add_shape_to_layer(new_shape)

        for shape in alignement_mark_etch.shapes:
            # take a deep copy of each shape 
            new_shape = shape.deepcopy()
            # and move it to the correct position
            new_shape.shift(shift_x_nm=shift_x, shift_y_nm=shift_y)
            # then add it to the desired layer
            etch_layer.add_shape_to_layer(new_shape)

        
    return [metalization_layer, etch_layer]
    

if __name__ == "__main__":
    aligned_layers = aligned_example()
    write_to_cif(filename = "aligned_hello_world", layers = aligned_layers)