Title: Programmatically set the pixel density (DPI) of a PNG image
Date: 2024-11-03
Author: Simon Larsén
Category: Programming
Image: {photo}set_png_dpi/qrcode_without_dpi.png
Slug: set-png-dpi
Tags: python,png,dpi

Earlier this week, I came across a situation where someone wanted a QR code to
"have 300 DPI so it looks good when printed". As I don't have much experience
with image formats, it took me a while to figure out what the actual request
was: to print the QR code on paper at a size of 2-3 cm, with sufficient
resolution for even the crappiest of phone cameras to be able to scan it.

The resolution was easily solved as the QR code library supported it, but the
size of the image on paper was a different story. I didn't even _really_ know
what DPI meant in the context of image metadata. While I knew that I could get the
task done in a heartbeat or two if I brought in a third party PNG library,
bringing in an entire PNG library just to do a single tiny alteration felt a bit
heavy-handed, not to mention that I wouldn't really understand what the library
was doing. So I decided to roll my own. And then write an article about how I
did it.

> **Note:** The code in this article is not the actual code written for my
> employer. It's not written in the same language and does not have the same
> constraints.

[TOC]

# What is this DPI thing?
My first order of business was figuring out what _dots per inch_ (DPI) even
means in relation to a digital image. I knew DPI only as a printer setting to
set the quality of the output, but had no particular insight into how that
relates to images that are themselves just a bunch of pixels.

Turns out, it's pretty much exactly what it sounds like: the amount of dots to
print per inch. As metadata on a digital image, it's essentially a scaling
factor for displaying the image, particularly when printing on physical media.
For example, if you print an image that is 100x100 pixels with a DPI of 100,
the image will be 1 inch by 1 inch on the physical paper. If you set the DPI to
50 instead, the image will be 2 inches by 2 inches, smearing one pixel over two
dots in each direction.

<div style="display: flex; justify-content: center; gap: 20%;">
    <figure style="text-align: center;">
        <img alt="PNG image without pixel density set" src="/images/set_png_dpi/qrcode_without_dpi.png" style="width: 116px;"/>
        <figcaption>Pixel density set to 100 DPI</figcaption>
    </figure>
    <figure style="text-align: center;">
        <img alt="PNG image with pixel density set" src="/images/set_png_dpi/qrcode_without_dpi.png" style="width: 228px;" />
        <figcaption>Pixel density set to 50 DPI</figcaption>
    </figure>
</div>
<br/>

Actually, the above captions aren't entirely truthful. The images are one and
the same, just scaled with CSS. In general, DPI does not affect how the image
is represented on a monitor, we have other scaling tools in the digital world
(such as CSS). That is not to say that there are _no_ image viewers that care
about DPI metadata, I'm sure there are, but none of the ones I currently have
installed seem to care. Including my web browser.

<div style="display: flex; justify-content: center; gap: 20%;">
    <figure style="text-align: center;">
        <img alt="PNG image without pixel density set" src="/images/set_png_dpi/qrcode_100_dpi.png" />
        <figcaption>Pixel density set to 100 DPI (for real)</figcaption>
    </figure>
    <figure style="text-align: center;">
        <img alt="PNG image with pixel density set" src="/images/set_png_dpi/qrcode_50_dpi.png" />
        <figcaption>Pixel density set to 50 DPI (for real)</figcaption>
    </figure>
</div>

# The structure of a PNG image
To be able to set the pixel density of a PNG image, we need to dive into the
image format. As luck would have it, PNG is a [relatively simple
format](https://www.w3.org/TR/png-3/#5DataRep). The spec defines the data format
as follows.

> The PNG datastream consists of a PNG signature followed by a sequence of
> chunks.

Scanning through the available chunks, it seems like the ancillary[ref]That's
fancy speak for "optional"[/ref] [`pHYs`
chunk](https://www.w3.org/TR/png-3/#11pHYs) is the one where we can set pixel
density for printing. I'm guessing "pHYs" is short for "physical".

Quickly scanning through the PNG that I needed to amend[ref]The PNG chunk types
are readable as plaintext. Open a PNG in any text editor that isn't afraid to
read a file that isn't entirely plaintext, and you'll most often be able to tell
if a chunk is present or not.[/ref], I could quickly determine that it simply
lacked this chunk, so the task is simply to add it to the chunk sequence. But
how do we know where to place it? And what it should look like? Let's dive into
the format and find out.

## The PNG signature
The signature makes up the first eight bytes of the file, and looks like this in
hex.

```
89 50 4E 47 0D 0A 1A 0A
```

> `50 4E 47` maps to the ASCII characters `P N G`. That's the name of the
> movie!

If a file does _not_ start with this signature, it's not a PNG file. But if it
does there, it's a PNG file and there should now be a bunch of chunks for us to
sink our teeth into.

## Chunk format and order
Each chunk in the PNG format has [four
fields](https://www.w3.org/TR/png-3/#5Chunk-layout):

* Length: 4 bytes defining the amount of bytes in the data chunk.
* Type: 4 bytes defining the chunk type.
* Data: As many bytes of data as defined in the length field. This field
  can be empty (and then the length field is 0).
* CRC checksum: A CRC32 checksum computed over the type and data fields.

Every PNG datastream starts with an [IHDR
chunk](https://www.w3.org/TR/png-3/#11IHDR) and ends with an [IEND
chunk](https://www.w3.org/TR/png-3/#11IEND). Everything in between is mostly
unordered[ref]There are some ordering rules. For example, if there are multiple
`IDAT` chunks, [they must appear consecutively, with no other kinds of chunks in
between](https://www.w3.org/TR/png-3/#11IDAT).[/ref]

Assuming we have a file without a `pHYs` chunk, which is the situation I found
myself in earlier this week, it's therefore very simple to find out _where_ to
place the `pHYs` chunk: after the required `IHDR` chunk, which just happens to
[always be 25 bytes large](https://www.w3.org/TR/png-3/#11IHDR).

This means that we can safely squeeze in our `pHYs` chunk `8 + 25 = 33` bytes
into the file. With Python, that would look something like this:

```python
PNG_SIGNATURE = b'\x89\x50\x4e\x47\x0D\x0A\x1A\x0A'

IHDR_SIZE = 25

def with_dpi(data: bytes, dots_per_inch: int) -> bytes:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Not a PNG image")

    signature_and_ihdr = data[:len(PNG_SIGNATURE) + IHDR_SIZE]
    rest = data[len(signature_and_ihdr):]

    phys_chunk = create_phys_chunk(dots_per_inch)

    return signature_and_ihdr + phys_chunk + rest
```

Now all we need to figure out is what the `pHYs` chunk should look like. In
other words, we need to implement the `create_phys_chunk()` function!

## The `pHYs` chunk
The [`pHYs` chunk](https://www.w3.org/TR/png-3/#11pHYs) is simple. It follows
the format [outlined above](#chunk-format-and-order), with a type field o `70 48
59 73` (which decodes to `pHYs` in ASCII) and a 9-byte data chunk on the
following format:

* 4 bytes of pixels per unit (X-axis)
* 4 bytes of pixels per unit (Y-axis)
* 1 byte of unit specifier which is either 0 or 1
    - 0: The unit is _unknown_ and the "pixels per unit" only defines aspect
      ratio. This does not help us define DPI.
    - 1: The unit is "meter". This is what we want.

So, apparently, the PNG format supports pixel density if we set the final byte
to `1`, but it's natively in _pixels per meter_. With `1 inch = 2.54cm`, we get
the nice and round conversion factor `100 [cm/m] / 2.54 [cm/inch] ≈ 39.37008
[inch/m]`. Finally, we also need to compute the CRC32 checksum, which
conveniently is implemented in the Python standard library [`binascii`
module](https://docs.python.org/3/library/binascii.html#binascii.crc32).

There's one more important piece of information, namely how to represent
multi-byte integers.

> All integers that require more than one byte shall be in network byte order
> (as illustrated in Figure 17 ): the most significant byte comes first, then
> the less significant bytes in descending order of significance (MSB LSB for
> two-byte integers, MSB B2 B1 LSB for four-byte integers).
>
> [Source](https://www.w3.org/TR/png-3/#7Integers-and-byte-order)

Network byte order is the same as [big-endian](https://en.wikipedia.org/wiki/Endianness),
and is how us humans write numbers. For example, the `pHYs` length field, which
has a value of 9, is encoded as `00 00 00 09`.

With this knowledge, let's write some code.

```python
import binascii

def create_phys_chunk(dots_per_inch: int) -> bytes:
    length_field = b"\x00\x00\x00\x09"
    type_field = b"pHYs"
    
    inches_per_meter = 39.37008
    dots_per_meter = int(dots_per_inch * inches_per_meter)
    pixels_per_meter_field = dots_per_meter.to_bytes(length=4, byteorder="big")
    unit_field = b"\x01"

    type_and_data = type_field + pixels_per_meter_field + pixels_per_meter_field + unit_field
    checksum = binascii.crc32(type_and_data).to_bytes(length=4, byteorder="big")
    
    return length_field + type_and_data + checksum
```

That's actually all there is to creating the `pHYs` chunk. Putting this
together with the previous code snippet, we have a fully functioning _addition_
of a `pHYs` chunk to a PNG file!

## Validating the results
While most image viewers will display the DPI of a PNG image somewhere, it can
be useful to have more deliberate tooling for the job.
[pngcheck](http://www.libpng.org/pub/png/apps/pngcheck.html), whose homepage is
one of the last remaining bastions of plain `http` on the web, is a useful tool
for inspecting the chunks of a PNG file.

Inspecting the original `qrcode_without_dpi.png`, we get the following output.

```bash
$ pngcheck -v qrcode_without_dpi.png
File: qrcode_without_dpi.png (484 bytes)
  chunk IHDR at offset 0x0000c, length 13
    116 x 116 image, 1-bit grayscale, non-interlaced
  chunk cHRM at offset 0x00025, length 32
    White x = 0.3127 y = 0.329,  Red x = 0.64 y = 0.33
    Green x = 0.3 y = 0.6,  Blue x = 0.15 y = 0.06
  chunk bKGD at offset 0x00051, length 2
    gray = 0x0000
  chunk tIME at offset 0x0005f, length 7:  2 Nov 2024 17:25:43 UTC
  chunk IDAT at offset 0x00072, length 200
    zlib: deflated, 2K window, maximum compression
  chunk tEXt at offset 0x00146, length 37, keyword: date:create
  chunk tEXt at offset 0x00177, length 37, keyword: date:modify
  chunk tEXt at offset 0x001a8, length 40, keyword: date:timestamp
  chunk IEND at offset 0x001dc, length 0
No errors detected in qrcode_without_dpi.png (9 chunks, 72.2% compression).
```

It reports the chunks in the order it scans them, and some details about each,
and summarizes with a status line about any errors (of which there should be
none), the total number of chunks as well as the overall compression of the
file.

If we do the same with the modified `qrcode_50_dpi.png`, we can see the added
`pHYs` chunk just after the `IHDR` chunk.

```bash
$ pngcheck -v qrcode_50_dpi.png
File: qrcode_50_dpi.png (505 bytes)
  chunk IHDR at offset 0x0000c, length 13
    116 x 116 image, 1-bit grayscale, non-interlaced
  chunk pHYs at offset 0x00025, length 9: 1968x1968 pixels/meter (50 dpi)
  chunk cHRM at offset 0x0003a, length 32
    White x = 0.3127 y = 0.329,  Red x = 0.64 y = 0.33
    Green x = 0.3 y = 0.6,  Blue x = 0.15 y = 0.06
  chunk bKGD at offset 0x00066, length 2
    gray = 0x0000
  chunk tIME at offset 0x00074, length 7:  2 Nov 2024 17:25:43 UTC
  chunk IDAT at offset 0x00087, length 200
    zlib: deflated, 2K window, maximum compression
  chunk tEXt at offset 0x0015b, length 37, keyword: date:create
  chunk tEXt at offset 0x0018c, length 37, keyword: date:modify
  chunk tEXt at offset 0x001bd, length 40, keyword: date:timestamp
  chunk IEND at offset 0x001f1, length 0
No errors detected in qrcode_50_dpi.png (10 chunks, 71.0% compression).
```

`pngcheck` is kind enough to report both the literal value, 1968x1968
pixels/meter, as well as the more industry standard 50 DPI. Note also how the
final status line still reports no errors, and that there are now 10 chunks in
total.

If you just want to check the integrity of the PNG file, running `pngcheck`
without the `-v` returns only a single, summarized status line.

```bash
$ pngcheck -v qrcode_50_dpi.png
OK: qrcode_50_dpi.png (116x116, 1-bit grayscale, non-interlaced, 71.0%).
```

> **Note:** For a more comprehensive set of image inspection and manipulation
> commands, I recommend [ImageMagick](https://imagemagick.org/). Its [identify
> command](https://imagemagick.org/script/identify.php) can do many of the same
> things as `pngcheck`, and is also more general purpose and can work with a
> wide variety of image formats. I chose not to use it for this article as it's
> a significantly more complicated tool than `pngcheck`.

## Caveat - what if there already is a `pHYs` chunk in the file?
As you may have noted, this implementation relies on the fact that there isn't
already a `pHYs` chunk in the PNG file, and therefore we can simply add one
after the `IHDR` chunk. For a more generalized solution, we should parse the PNG
file and replace any existing `pHYs` chunk. That's really not very difficult,
given how all the chunks start with the data chunk length and are therefore easy
to skip over[ref]The length of a chunk is always `12 + len(data)`, due to the
fixed size of the length, type and checksum fields.[/ref], but it was still
well beyond what was needed for my implementation.

# And now you know how to set the DPI on a PNG!
Working with binary formats may seem daunting if you're not used to it, but most
often, it really isn't that difficult. In fact, the PNG format is _very_ easy to
work with due to the consistent layout of the chunks. I think the challenge lies
primarily in reading and understanding specifications, and that's something that
takes a bit of practice.

Some may still think that I should have just pulled in a library for this, but I
strongly disagree. Not only is the final solution [both fairly short and
simple](#putting-it-all-together), but I also now have a solid understanding for
the fundamentals of the PNG file format and have improved my understanding of
image formats in general.

# Putting it all together
Putting this all together in a fully functioning Python script, it could look
like this:

```python
import binascii
import pathlib

PNG_SIGNATURE = b'\x89\x50\x4e\x47\x0D\x0A\x1A\x0A'

# the IHDR field is 25 bytes: [ length | 4 bytes ] [ type | 4 bytes ] [ data | 13 bytes ] [ checksum | 4 bytes ]
IHDR_SIZE = 25

def main():
    qrcode_path = pathlib.Path("qrcode.png").absolute()
    qrcode_data = qrcode_path.read_bytes()
    qrcode_data_with_adjusted_dpi = with_dpi(qrcode_data, dots_per_inch=100)
    pathlib.Path("qrcode_with_dpi.png").write_bytes(qrcode_data_with_adjusted_dpi)

def with_dpi(data: bytes, dots_per_inch: int) -> bytes:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("Not a PNG image")

    signature_and_ihdr = data[:len(PNG_SIGNATURE) + IHDR_SIZE]
    rest = data[len(signature_and_ihdr):]

    phys_chunk = create_phys_chunk(dots_per_inch)

    return signature_and_ihdr + phys_chunk + rest


def create_phys_chunk(dots_per_inch: int) -> bytes:
    """Create a pHYs chunk with the specified dots per inch, converted to the
    PNG native pixels per meter.
    """
    length_field = b"\x00\x00\x00\x09"
    type_field = b"pHYs"
    
    inches_per_meter = 39.37008
    dots_per_meter = int(dots_per_inch * inches_per_meter)
    pixels_per_meter_field = dots_per_meter.to_bytes(length=4, byteorder="big")
    unit_field = b"\x01"

    type_and_data = type_field + pixels_per_meter_field + pixels_per_meter_field + unit_field
    checksum = binascii.crc32(type_and_data).to_bytes(length=4, byteorder="big")
    
    return length_field + type_and_data + checksum


if __name__ == "__main__":
    main()
```
