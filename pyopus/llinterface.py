# -*- coding: utf-8 -*-

'''Low-level interface to libopus.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'strerror',
        'get_version_string',

        'encoder_get_size',
        'encoder_create',
        'encoder_init',
        'encode',
        'encode_float',
        'encoder_destroy',
        'encoder_ctl',

        'decoder_get_size',
        'decoder_create',
        'decoder_init',
        'decode',
        'decode_float',
        'decoder_ctl',
        'decoder_destroy',

        'repacketizer_get_size',
        'repacketizer_init',
        'repacketizer_create',
        'repacketizer_destroy',
        ]

from .binding import ffi, C
from .constants import OK


class OpusError(RuntimeError):
    def __init__(self, errno):
        msg = strerror(errno)
        super(OpusError, self).__init__(errno, msg)

        self.errno, self.message = errno, msg

    def __unicode__(self):
        return '[Opus Error {0}] {1}'.format(self.errno, self.message)

    def __str__(self):
        return str(self.__unicode__())


# const char *opus_strerror(int error);
def strerror(error):
    return ffi.string(C.opus_strerror(error)).decode('utf-8')


# const char *opus_get_version_string(void);
def get_version_string():
    return ffi.string(C.opus_get_version_string()).decode('utf-8')


# int opus_encoder_get_size(int channels);
def encoder_get_size(channels):
    return C.opus_encoder_get_size(channels)


# OpusEncoder *opus_encoder_create(
#         opus_int32 Fs,
#         int channels,
#         int application,
#         int *error
#         );
def encoder_create(Fs, channels, application):
    error_p = ffi.new('int[1]')

    st = C.opus_encoder_create(Fs, channels, application, error_p)
    error = error_p[0]

    if error != OK:
        raise OpusError(error)

    return st


# int opus_encoder_init(
#         OpusEncoder *st,
#         opus_int32 Fs,
#         int channels,
#         int application
#         );
def encoder_init(st, Fs, channels, application):
    error = C.opus_encoder_init(st, Fs, channels, application)

    if error != OK:
        raise OpusError(error)


# opus_int32 opus_encode(
#         OpusEncoder *st,
#         const opus_int16 *pcm,
#         int frame_size,
#         unsigned char *data,
#         opus_int32 max_data_bytes
#         );
def encode(st, pcm, frame_size, data, max_data_bytes):
    result = C.opus_encode(st, pcm, frame_size, data, max_data_bytes)

    if result < 0:
        raise OpusError(result)

    return result


# opus_int32 opus_encode_float(
#         OpusEncoder *st,
#         const float *pcm,
#         int frame_size,
#         unsigned char *data,
#         opus_int32 max_data_bytes
#         );
def encode_float(st, pcm, frame_size, data, max_data_bytes):
    result = C.opus_encode_float(st, pcm, frame_size, data, max_data_bytes)

    if result < 0:
        raise OpusError(result)

    return result


# void opus_encoder_destroy(OpusEncoder *st);
def encoder_destroy(st):
    C.opus_encoder_destroy(st)


# int opus_encoder_ctl(OpusEncoder *st, int request, ...);
def encoder_ctl(st, request, *args):
    error = C.opus_encoder_ctl(st, request, *args)

    if error != OK:
        raise OpusError(error)


# int opus_decoder_get_size(int channels);
def decoder_get_size(channels):
    return C.opus_decoder_get_size(channels)


# OpusDecoder *opus_decoder_create(opus_int32 Fs, int channels, int *error);
def decoder_create(Fs, channels):
    error_p = ffi.new('int[1]')

    st = C.opus_decoder_create(Fs, channels, error_p)
    error = error_p[0]

    if error != OK:
        raise OpusError(error)

    return st


# int opus_decoder_init(OpusDecoder *st, opus_int32 Fs, int channels);
def decoder_init(st, Fs, channels):
    error = C.opus_decoder_init(st, Fs, channels)

    if error != OK:
        raise OpusError(error)


# int opus_decode(
#         OpusDecoder *st,
#         const unsigned char *data,
#         opus_int32 len,
#         opus_int16 *pcm,
#         int frame_size,
#         int decode_fec
#         );
def decode(st, data, len, pcm, frame_size, decode_fec):
    result = C.opus_decode(st, data, len, pcm, frame_size, decode_fec)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_decode_float(
#         OpusDecoder *st,
#         const unsigned char *data,
#         opus_int32 len,
#         float *pcm,
#         int frame_size,
#         int decode_fec
#         );
def decode_float(st, data, len, pcm, frame_size, decode_fec):
    result = C.opus_decode_float(st, data, len, pcm, frame_size, decode_fec)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_decoder_ctl(OpusDecoder *st, int request, ...);
def decoder_ctl(st, request, *args):
    error = C.opus_decoder_ctl(st, request, *args)

    if error != OK:
        raise OpusError(error)


# void opus_decoder_destroy(OpusDecoder *st);
def decoder_destroy(st):
    C.opus_decoder_destroy(st)


# int opus_packet_parse(
#         const unsigned char *data,
#         opus_int32 len,
#         unsigned char *out_toc,
#         const unsigned char *frames[48],
#         opus_int16 size[48],
#         int *payload_offset
#         );
# This is an internal function according to the libopus documentation, so
# we don't wrap it here.

# int opus_packet_get_bandwidth(const unsigned char *data);
def packet_get_bandwidth(data):
    result = C.opus_packet_get_bandwidth(data)

    if result < 0:
        # actually it is an OPUS_INVALID_PACKET, according to docs
        raise OpusError(result)

    return result


# int opus_packet_get_samples_per_frame(
#         const unsigned char *data,
#         opus_int32 Fs
#         );
def packet_get_samples_per_frame(data, Fs):
    result = C.opus_packet_get_samples_per_frame(data, Fs)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_packet_get_nb_channels(const unsigned char *data);
def packet_get_nb_channels(data):
    result = C.opus_packet_get_nb_channels(data)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_packet_get_nb_frames(const unsigned char packet[], opus_int32 len);
def packet_get_nb_frames(packet, len):
    result = C.opus_packet_get_nb_frames(packet, len)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_packet_get_nb_samples(
#         const unsigned char packet[],
#         opus_int32 len,
#         opus_int32 Fs
#         );
def packet_get_nb_samples(packet, len, Fs):
    result = C.opus_packet_get_nb_samples(packet, len, Fs)

    if result < 0:
        raise OpusError(result)

    return result


# int opus_decoder_get_nb_samples(
#         const OpusDecoder *dec,
#         const unsigned char packet[],
#         opus_int32 len
#         );
def decoder_get_nb_samples(dec, packet, len):
    result = C.opus_decoder_get_nb_samples(dec, packet, len)

    if result < 0:
        raise OpusError(result)

    return result


# void opus_pcm_soft_clip(
#         float *pcm,
#         int frame_size,
#         int channels,
#         float *softclip_mem
#         );
def pcm_soft_clip(pcm, frame_size, channels, softclip_mem):
    C.opus_pcm_soft_clip(pcm, frame_size, channels, softclip_mem)


# int opus_repacketizer_get_size(void);
def repacketizer_get_size():
    return C.opus_repacketizer_get_size()


# OpusRepacketizer *opus_repacketizer_init(OpusRepacketizer *rp);
def repacketizer_init(rp):
    return C.opus_repacketizer_init(rp)


# OpusRepacketizer *opus_repacketizer_create(void);
def repacketizer_create():
    return C.opus_repacketizer_create()


# void opus_repacketizer_destroy(OpusRepacketizer *rp);
def repacketizer_destroy(rp):
    C.opus_repacketizer_destroy(rp)


# int opus_repacketizer_cat(
#         OpusRepacketizer *rp,
#         const unsigned char *data,
#         opus_int32 len
#         );
# opus_int32 opus_repacketizer_out_range(
#         OpusRepacketizer *rp,
#         int begin,
#         int end,
#         unsigned char *data,
#         opus_int32 maxlen
#         );
# int opus_repacketizer_get_nb_frames(OpusRepacketizer *rp);
# opus_int32 opus_repacketizer_out(
#         OpusRepacketizer *rp,
#         unsigned char *data,
#         opus_int32 maxlen
#         );
# int opus_packet_pad(
#         unsigned char *data,
#         opus_int32 len,
#         opus_int32 new_len
#         );
# opus_int32 opus_packet_unpad(unsigned char *data, opus_int32 len);
# int opus_multistream_packet_pad(
#         unsigned char *data,
#         opus_int32 len,
#         opus_int32 new_len,
#         int nb_streams
#         );
# opus_int32 opus_multistream_packet_unpad(
#         unsigned char *data,
#         opus_int32 len,
#         int nb_streams
#         );


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
