Hello everyone. This is a fairly simple and primitive numeric image encoder.
Its initial purpose (with some modifications) will be to receive real-time data to construct an image from a device that transmits numerical data, such as LORA or XBEE.

In this first version, you can feed the file <colores_encontrados.csv>—the more images you encode, the more references it will contain. Once the file has enough references, it can be used as a static file for both the encoder and decoder.

The encoder program loads an image, analyzes it pixel by pixel, converts its colors into a numerical matrix, stores them by ID in a text file, and adds any new colors found to the CSV.

The decoder program receives a text file with the image encoded using the color IDs and reconstructs the image using the data from the CSV, then saves it.

