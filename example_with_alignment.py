from CleWin_cif_creator import load_cif, write_to_cif

filename = "centered_alignment_mark"

alignment_mark_layers = load_cif(filename=filename)

write_to_cif(filename = "test", layers = alignment_mark_layers)



with open("test_2.cif", "r") as file: 
    test = file.read()

with open(f"{filename}.cif") as file:
    original = file.read()

print(test == original)