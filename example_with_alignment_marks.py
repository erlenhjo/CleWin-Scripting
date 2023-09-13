from CleWin_cif_creator import (
    load_cif,
    write_to_cif,
    CleWin_layer,
    plotLayers,
    CIF_wire,
)
from example import example_layers
import os


def get_shifted_alignment_mark(
    x_shift, y_shift, alignment_mark_layer_index, color="blue"
):
    file_path = os.path.dirname(os.path.abspath(__file__))
    alignment_mark_filename = "/centered_alignment_mark"
    alignment_mark_layers: list[CleWin_layer] = load_cif(
        filename=file_path + alignment_mark_filename
    )

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

    alignment_mark_positions = [
        [10e6, 10e6],
        [-10e6, 10e6],
        [10e6, -10e6],
        [-10e6, -10e6],
    ]

    for alignment_mark_position in alignment_mark_positions:
        # get shapes from above function
        metalization_alignement_mark_shapes = get_shifted_alignment_mark(
            x_shift=alignment_mark_position[0],
            y_shift=alignment_mark_position[1],
            alignment_mark_layer_index=0,
            color="green",
        )
        etch_alignement_mark_shapes = get_shifted_alignment_mark(
            x_shift=alignment_mark_position[0],
            y_shift=alignment_mark_position[1],
            alignment_mark_layer_index=1,
        )

        # add shapes to desired layers
        metalization_layer.shapes.extend(metalization_alignement_mark_shapes)
        etch_layer.shapes.extend(etch_alignement_mark_shapes)

    return [metalization_layer, etch_layer]


if __name__ == "__main__":
    import numpy as np

    aligned_layers = aligned_example()

    # add smiley face
    t = np.linspace(-1 / 3 * np.pi, np.pi / 3, 10)

    wire_points_smile = [
        (i, j) for i, j in zip(550_000 * np.cos(t), 550_000 * np.sin(t))
    ]
    wire_mask = CIF_wire(points=wire_points_smile, width_nm=100e3)
    wire_mask.shift(shift_x_nm=1_000_000, shift_y_nm=0)

    wire_right_eye = CIF_wire(points=[(0, 0), (500_000, 0)], width_nm=100e3)
    wire_right_eye.shift(shift_x_nm=550_000, shift_y_nm=200_000)

    wire_left_eye = CIF_wire(points=[(0, 0), (500_000, 0)], width_nm=100e3)
    wire_left_eye.shift(shift_x_nm=550_000, shift_y_nm=-200_000)

    aligned_layers[0].shapes.extend([wire_mask, wire_right_eye, wire_left_eye])


    plotLayers(layers=aligned_layers, window_size=(30_000_000), alpha=1)
    write_to_cif(filename="aligned_hello_world", layers=aligned_layers)