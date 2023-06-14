

# Time domain plot
def real_image_plot(chirp: list):

    real = []
    image = []
    time = []

    for i in range(len(chirp)):
        real.append(chirp[i].real)
        image.append(chirp[i].imag)
        time.append(i / 10)

    return [time, real, image]
