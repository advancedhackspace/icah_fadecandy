y_offset = 16.5
z_offset = 15.5

with open('snake_grid.json', 'w') as json:
    json.write('[\n')

    # Write 55 blank pixels
    for i in range(0, 55):
        json.write('    {\"point\": [0.00, 0.00, 0.00]},\n')

    # Write grid pixels
    for i in range(0, 34):
        for j in range(0, 32):
            y = (i - y_offset) / 10
            if i % 2 == 0:
                z = (j - z_offset) / 10
            else:
                z = (31 - j - z_offset) / 10
            z = -z
            json.write('    {\"point\": [0.00, %.2f, %.2f]},\n' % (y, z))
    json.write(']')
