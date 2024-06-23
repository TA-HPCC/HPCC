import sys
import re


def set_error_rates_topology(topo_file_path,new_error_rate):
    # Read the input file
    try:
        
        for topo_file in topo_file_path:
            with open(topo_file, 'r') as file:
                lines = file.readlines()

            # Update the error rate in the specified lines
            start_line = 2  # 0-based index, so line 3 is index 2
            for i in range(start_line, len(lines)):
                columns = lines[i].strip().split()
                if len(columns) >= 5:
                    columns[4] = str(new_error_rate)
                    lines[i] = ' '.join(columns) + '\n'
                else:
                    break

            # Write the updated lines back to the same file
            with open(topo_file, 'w') as file:
                file.writelines(lines)
    except IOError:
        print "File topologi tidak ditemukan."

def set_error_rate_third_cc(third_cc_path,new_error_rate):
    try:
        # Buka file C++ untuk dibaca
        with open(third_cc_path, 'r') as file:
            # Baca semua baris
            lines = file.readlines()

        # Loop melalui setiap baris
        for i, line in enumerate(lines):
            # Cari baris yang mengandung deklarasi error_rate_per_link
            if 'double error_rate_per_link' in line:
                # Ubah nilai error_rate_per_link
                lines[i] = 'double error_rate_per_link = {};\n'.format(new_error_rate)
                break

        # Tulis kembali perubahan ke file
        with open(third_cc_path, 'w') as file:
            file.writelines(lines)

    except IOError:
        print "File tidak ditemukan."
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python set_error_rate.py  <new_error_rate>")
        sys.exit(1)

    try:
        new_error_rate = float(sys.argv[1])
    except ValueError:
        print("Error: new_error_rate must be a int/float.")
        sys.exit(1)

    topo_file_path = [
    'simulation/mix/mesh_topology.txt',
    'simulation/mix/star_topology.txt',
    'simulation/mix/fat.txt',
    ]
    third_cc_path = 'simulation/scratch/third.cc'
    set_error_rates_topology(topo_file_path,new_error_rate)
    set_error_rate_third_cc(third_cc_path,new_error_rate)
    print("Error rates updated successfully.")
