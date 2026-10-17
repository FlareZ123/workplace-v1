/* Inspect bit-level end-of-block slack in one raw DEFLATE stream.

Input: compressed raw DEFLATE bytes on stdin, at most 65,536 bytes.
Output: return-code, data_type, bytes consumed, bytes decompressed,
        final-boundary flag.
The low six bits of z_stream.data_type are the unused bits in the last
compressed byte at an end-of-block boundary. Check the high unused bits
of the final compressed byte for hidden content.

This forensic helper is independent of facility equipment or services.
Build with a C11 compiler and zlib development library; e.g. -lz.
See https://zlib.net/manual.html for Z_BLOCK and data_type semantics.
*/
#include <stdio.h>
#include <string.h>
#include <zlib.h>

int main(void) {
    unsigned char input[65536], output[131072];
    size_t n = fread(input, 1, sizeof(input), stdin);
    if (ferror(stdin) || (n == sizeof(input) && !feof(stdin))) return 2;
    z_stream s;
    memset(&s, 0, sizeof(s));
    s.next_in = input;
    s.avail_in = (uInt)n;
    s.next_out = output;
    s.avail_out = sizeof(output);
    if (inflateInit2(&s, -15) != Z_OK) return 3;
    int rc = Z_OK, boundary = 0;
    for (int tries = 0; tries < 1000; tries++) {
        rc = inflate(&s, Z_BLOCK);
        if (rc == Z_STREAM_END || (s.data_type & 128)) {
            boundary = 1;
            break;
        }
        if (rc != Z_OK || !s.avail_in) break;
    }
    printf("%d %d %lu %lu %d\n", rc, s.data_type, s.total_in, s.total_out, boundary);
    inflateEnd(&s);
    return boundary ? 0 : 4;
}
