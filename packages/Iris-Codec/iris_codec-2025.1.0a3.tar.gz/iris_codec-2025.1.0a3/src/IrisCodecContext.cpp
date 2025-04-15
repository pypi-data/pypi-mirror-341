//
//  IrisCodecContext.cpp
//  Iris
//
//  Created by Ryan Landvater on 1/9/24.
//
#include <sstream>
#include "IrisCodecPriv.hpp"
#include "IrisCoreVulkan.hpp"
#include <turbojpeg.h>
#include <avif/avif.h>

static const avifRGBImage AVIF_RGB_BLANK_IMAGE {
    .width              = TILE_PIX_LENGTH,
    .height             = TILE_PIX_LENGTH,
    .depth              = 0,
    .format             = AVIF_RGB_FORMAT_COUNT,
    .chromaUpsampling   = AVIF_CHROMA_UPSAMPLING_AUTOMATIC,
    .chromaDownsampling = AVIF_CHROMA_DOWNSAMPLING_AUTOMATIC,
    .avoidLibYUV        = AVIF_FALSE,
    .ignoreAlpha        = AVIF_FALSE,
    .alphaPremultiplied = AVIF_FALSE,
    .isFloat            = AVIF_FALSE,
    .maxThreads         = 1,
    .pixels             = NULL,
    .rowBytes           = 0,
};

namespace IrisCodec {
inline Quality CHECK_QUALITY_BOUNDS (Quality quality)
{
    if (quality > 100) {
        std::cerr << "Quality exceeds the definined maximum of 100\n";
        return 100;
    } return quality;
}
inline int BITS_PER_PIXEL (Format format)
{
    switch (format) {
        case Iris::FORMAT_UNDEFINED:
        std::cerr << "Undefined format provided. Returning 0 bpp\n";
            return 0;
        case Iris::FORMAT_B8G8R8:
        case Iris::FORMAT_R8G8B8:       return 3;
        case Iris::FORMAT_B8G8R8A8:
        case Iris::FORMAT_R8G8B8A8:     return 4;
    }
    std::cerr << "Invalid format provided. Returning 0 bpp\n";
    return 0;
}
inline int BIT_DEPTH (Format format)
{
    switch (format) {
            
        case Iris::FORMAT_UNDEFINED:
            std::cerr << "Undefined format provided. Returning 0 bit depth\n";
                return 0;
        case Iris::FORMAT_B8G8R8:
        case Iris::FORMAT_R8G8B8:
        case Iris::FORMAT_B8G8R8A8:
        case Iris::FORMAT_R8G8B8A8: return 8;
    }
    std::cerr << "Invalid format provided. Returning 0 bit depth\n";
    return 0;
}
inline Subsampling CHECK_SUBSAMPLING (Subsampling subsample)
{
    switch (subsample) {
        case SUBSAMPLE_444:
        case SUBSAMPLE_422:
        case SUBSAMPLE_420:
            return subsample;
    }
    std::cerr << "Invalid subsampling provided, using default";
    return SUBSAMPLE_DEFAULT;
}
inline Format CHECK_PIXEL_FORMAT (Format format)
{
    switch (format) {
        case Iris::FORMAT_B8G8R8:
        case Iris::FORMAT_R8G8B8:
        case Iris::FORMAT_B8G8R8A8:
        case Iris::FORMAT_R8G8B8A8:     return format;
        case Iris::FORMAT_UNDEFINED:    break;
    }
    std::cerr << "Pixel format check failed. Invalid pixel format provided.";
    return FORMAT_UNDEFINED;
}
inline TJSAMP CONVERT_TO_TJSAMP (Subsampling subsample)
{
    switch (subsample) {
        case SUBSAMPLE_444: return TJSAMP_444;
        case SUBSAMPLE_422: return TJSAMP_422;
        case SUBSAMPLE_420: return TJSAMP_420;
    }
    std::cerr << "Invalid subsampling provided, using TJSAMP_444";
    return TJSAMP_444;
}
inline TJPF CONVERT_TO_TJPIXEL_FORMAT(Format format)
{
    switch (format) {
        case Iris::FORMAT_UNDEFINED:
            std::cerr << "FORMAT_UNDEFINED provided, returning TJPF_UNKNOWN";
            return TJPF_UNKNOWN;
            
        case Iris::FORMAT_B8G8R8:       return TJPF_BGR;
        case Iris::FORMAT_R8G8B8:       return TJPF_RGB;
        case Iris::FORMAT_B8G8R8A8:     return TJPF_BGRA;
        case Iris::FORMAT_R8G8B8A8:     return TJPF_RGBA;
    }
    std::cerr << "Invalid format provided, returning TJPF_UNKNOWN";
    return TJPF_UNKNOWN;
}
inline avifPixelFormat CONVERT_TO_AVIF_SAMP (Subsampling subsample)
{
    switch (subsample) {
        case SUBSAMPLE_444: return AVIF_PIXEL_FORMAT_YUV444;
        case SUBSAMPLE_422: return AVIF_PIXEL_FORMAT_YUV422;
        case SUBSAMPLE_420: return AVIF_PIXEL_FORMAT_YUV420;
    }
    std::cerr << "Invalid subsampling provided, using AVIF_PIXEL_FORMAT_YUV444";
    return AVIF_PIXEL_FORMAT_YUV444;
}
inline avifRGBFormat CONVERT_TO_AVIF_RGBFORMAT (Format format)
{
    switch (format) {
        case Iris::FORMAT_UNDEFINED:
            std::cerr << "FORMAT_UNDEFINED provided, returning AVIF_RGB_FORMAT_COUNT";
            return AVIF_RGB_FORMAT_COUNT;
            
        case Iris::FORMAT_B8G8R8:       return AVIF_RGB_FORMAT_BGR;
        case Iris::FORMAT_R8G8B8:       return AVIF_RGB_FORMAT_RGB;
        case Iris::FORMAT_B8G8R8A8:     return AVIF_RGB_FORMAT_BGRA;
        case Iris::FORMAT_R8G8B8A8:     return AVIF_RGB_FORMAT_RGBA;
    }
    std::cerr << "Invalid format provided, returning AVIF_RGB_FORMAT_COUNT";
    return AVIF_RGB_FORMAT_COUNT;
}
__INTERNAL__Context::__INTERNAL__Context    (const ContextCreateInfo& info) :
_device                                     (nullptr)
{
    
}
__INTERNAL__Context::~__INTERNAL__Context ()
{
    
}
inline void SIMPLY_COPY (const Buffer& src, Buffer& dst)
{
    memcpy(dst->append(src->size()), src->data(), src->size());
}
inline Buffer COMPRESS_JPEG (const Buffer &src,
                             Format format,
                             Quality quality,
                             Subsampling subsampling)
{
    tjhandle turbo_handle = NULL;
    auto dst = Create_strong_buffer(tjBufSize(TILE_PIX_LENGTH, TILE_PIX_LENGTH,
                                              CONVERT_TO_TJSAMP(subsampling)));
    try {
        size_t size     = dst->capacity();
        auto dst_ptr    = (BYTE*)dst->data();
        turbo_handle    = tj3Init (TJINIT_COMPRESS);
        if (turbo_handle == NULL)
            throw std::runtime_error("Failed to create a TURBO_JPEG Context");
        // Set the desired image quality
        if (tj3Set(turbo_handle, TJPARAM_QUALITY, quality))
            throw std::runtime_error("Failed to configure TURBO_JPEG Context -- " +
                                     std::string(tj3GetErrorStr(turbo_handle)));
        // Set the chromatic image subsampling level
        if (tj3Set(turbo_handle, TJPARAM_SUBSAMP, CONVERT_TO_TJSAMP(subsampling)))
            throw std::runtime_error("Failed to configure TURBO_JPEG Context -- " +
                                     std::string(tj3GetErrorStr(turbo_handle)));
        // Compress the image
        if (tj3Compress8(turbo_handle, static_cast<BYTE*>(src->data()),
                         TILE_PIX_LENGTH, 0, TILE_PIX_LENGTH,
                         CONVERT_TO_TJPIXEL_FORMAT(format),
                         &dst_ptr, &size))
            throw std::runtime_error("TURBO_JPEG failed to compress tile data --" +
                                     std::string(tj3GetErrorStr(turbo_handle)));
        tj3Destroy  (turbo_handle);
        
        // If JPEG_TURBO reallocated the pointer, copy the data out of the new pointer
        // and return that instead. This should never happen...
        if (dst_ptr != dst->data())
            dst = Copy_strong_buffer_from_data(dst_ptr, size);
        // Make sure to update the size of the buffer and return.
        else dst->set_size(size);
        return dst;
    } catch (std::runtime_error &e) {
        if (turbo_handle) tjDestroy(turbo_handle);
        std::stringstream log;
        log << "Failed to compress JPEG tile: "
            << e.what() << "\n";
        throw std::runtime_error(log.str());
        return Buffer();
    }   return Buffer();
}
inline Buffer DECOMPRESS_JPEG (const DecompressTileInfo& info)
{
    auto&       src_buffer  = info.compressed;
    Buffer      dst_buffer  = info.optionalDestination;
    TJPF        format      = CONVERT_TO_TJPIXEL_FORMAT(info.desiredFormat);
    tjhandle    tjhandle    = NULL;
    size_t      buffer_size = TILE_PIX_AREA*BITS_PER_PIXEL(info.desiredFormat);

    if (format == TJPF_UNKNOWN || !buffer_size) throw std::runtime_error
        ("DECOMPRESS_JPEG failed due to undefined destination pixel format");
    
    if (!dst_buffer || buffer_size > dst_buffer->size())
        dst_buffer = Create_strong_buffer(buffer_size);
    
    try {
        tjhandle = tj3Init(TJINIT_DECOMPRESS);
        tj3Set(tjhandle, TJPARAM_JPEGWIDTH,  TILE_PIX_LENGTH);
        tj3Set(tjhandle, TJPARAM_JPEGHEIGHT, TILE_PIX_LENGTH);
        int result = tj3Decompress8
        (tjhandle, static_cast<const BYTE*>(src_buffer->data()),
         src_buffer->size(),
         static_cast<BYTE*>(dst_buffer->data()),
         0, format);
        
        if (result) throw std::runtime_error
            ("DECOMPRESS_JPEG failed with tj3error " +
             std::string(tj3GetErrorStr(tjhandle)));
        
    } catch (std::runtime_error& error) {
        std::cerr   << "Failed to decompress JPEG tile: "
                    << error.what() << "\n";
        dst_buffer  = NULL;
    }
    
    if (tjhandle) tj3Destroy (tjhandle);
    return dst_buffer;
}
inline Buffer COMPRESS_AVIF_CPU (const Buffer &src_buffer,
                                 Format format,
                                 Quality quality,
                                 Subsampling subsampling)
{
    Buffer          dst_buffer  = nullptr;
    avifImage*      image       = nullptr;
    avifEncoder*    encoder     = NULL;
    avifRWData      avifOutput  = AVIF_DATA_EMPTY;
    avifRGBImage    rgb         = AVIF_RGB_BLANK_IMAGE;
    
    try {
        image                   = avifImageCreate
        (TILE_PIX_LENGTH, TILE_PIX_LENGTH,
         BIT_DEPTH(format),
         CONVERT_TO_AVIF_SAMP(subsampling));
        
        if (!image) throw std::runtime_error
            ("failed to create AVIF dst image");
        
        avifRGBImageSetDefaults(&rgb, image);
        rgb.ignoreAlpha = true;
        rgb.format      = CONVERT_TO_AVIF_RGBFORMAT(format);
        rgb.maxThreads  = 1;
        rgb.pixels      = (uint8_t*)src_buffer->data();
        rgb.rowBytes    = TILE_PIX_LENGTH * BITS_PER_PIXEL(format);
        
        auto result = avifImageRGBToYUV(image, &rgb);
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("failed to convert to RGB image YUV -- "+
             std::string(avifResultToString(result)));
        
        encoder = avifEncoderCreate();
        if (encoder == NULL) throw std::runtime_error
            ("Failed to create AVIF encoder");
        encoder->maxThreads = 1;
        encoder->quality    = (int)quality;
        encoder->speed      = 10;
        
        result = avifEncoderAddImage(encoder, image, 1, AVIF_ADD_IMAGE_FLAG_SINGLE);
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("failed to add image to encoder: --"+
             std::string(avifResultToString(result)));
        
        
        result = avifEncoderFinish(encoder, &avifOutput);
        if (result != AVIF_RESULT_OK)throw std::runtime_error
            ("Failed to finish encode: "+
             std::string(avifResultToString(result)));
        
        
        // Transfer control of the data to an Iris buffer
        dst_buffer = Wrap_weak_buffer_fom_data(avifOutput.data, avifOutput.size);
        dst_buffer->change_strength(REFERENCE_STRONG);
        avifOutput = AVIF_DATA_EMPTY;
        
    } catch (std::runtime_error& error) {
        std::cerr   << "Failed to compress AVIF tile: "
                    << error.what() << "\n";
        dst_buffer = NULL;
    }

    if (image)   avifImageDestroy   (image);
    if (encoder) avifEncoderDestroy (encoder);
    avifRWDataFree (&avifOutput);
    return dst_buffer;
}
inline Buffer DECOMPRESS_AVIF_CPU (const DecompressTileInfo& info)
{
    auto&           src_buffer  = info.compressed;
    Buffer          dst_buffer  = info.optionalDestination;
    avifDecoder*    decoder     = NULL;
    size_t          buffer_size = TILE_PIX_AREA * BITS_PER_PIXEL(info.desiredFormat);
    
    // Reallocate buffer if insufficient space provided
    if (!dst_buffer || dst_buffer->size() < buffer_size)
        dst_buffer = Create_strong_buffer (buffer_size);
    
    try {
        avifRGBImage rgb    = AVIF_RGB_BLANK_IMAGE;
        rgb.format          = CONVERT_TO_AVIF_RGBFORMAT(info.desiredFormat);
        rgb.rowBytes        = TILE_PIX_LENGTH * BITS_PER_PIXEL(info.desiredFormat);
        rgb.depth           = BIT_DEPTH(info.desiredFormat);
        rgb.pixels          = (uint8_t*)dst_buffer->data();
        
        if (rgb.format == AVIF_RGB_FORMAT_COUNT || !buffer_size) throw std::runtime_error
            ("Failed due to undefined destination pixel format");

        decoder = avifDecoderCreate();
        if (decoder == NULL) throw std::runtime_error
            ("Failed to create AVIF encoder");
        decoder->maxThreads = 1;
        decoder->imageDimensionLimit = TILE_PIX_LENGTH;
        
        avifResult result = avifDecoderSetIOMemory
        (decoder, (uint8_t*)src_buffer->data(), src_buffer->size());
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("Failed to set memory IO for AVIF decoder -- "+
             std::string(avifResultToString(result)));
        
        result = avifDecoderParse(decoder);
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("Failed to decode AVIF tile -- "+
             std::string(avifResultToString(result)));
        
        result = avifDecoderNextImage(decoder);
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("Failed to read AVIF tile -- "+
             std::string(avifResultToString(result)));
        
        result = avifImageYUVToRGB(decoder->image, &rgb);
        if (result != AVIF_RESULT_OK) throw std::runtime_error
            ("Failed to convert YUV formatted tile -- "+
             std::string(avifResultToString(result)));
        
    } catch (std::runtime_error& error) {
        std::cerr   << "DECOMPRESS_AVIF_CPU error: "
                    << error.what() << "\n";
        dst_buffer = NULL;
    }
    if (decoder) avifDecoderDestroy(decoder);
    return dst_buffer;
}
Buffer __INTERNAL__Context::compress_tile(const CompressTileInfo &info)
{
    Buffer dst;
    switch (info.encoding) {
        case TILE_ENCODING_UNDEFINED:
            throw std::runtime_error("Encoding format in CompressTileInfo is undefined");
            return Buffer();
        case TILE_ENCODING_JPEG:
            return COMPRESS_JPEG (info.pixelArray, info.format, info.quality, info.subsampling);
        case TILE_ENCODING_AVIF:
            if (_gpuAV1Encode) {
                assert(false && "HARDWARE ENCODER AV1 IMPLEMENTATION NOT YET BUILT");
            } return COMPRESS_AVIF_CPU (info.pixelArray, info.format, info.quality, info.subsampling);
            break;
        case TILE_ENCODING_IRIS:
            assert(false && "IMPLEMENTATION NOT YET BUILT");
            break;
    } return dst;

//    if (info.destinationOptional && info.destinationOptional->capacity() >= dst_size)
}
Buffer __INTERNAL__Context::decompress_tile(const DecompressTileInfo &info)
{
    switch (info.encoding) {
        case TILE_ENCODING_UNDEFINED:
            throw std::runtime_error("Encoding format in DecompressTileInfo is undefined");
        case TILE_ENCODING_JPEG:
            return DECOMPRESS_JPEG(info);
        case TILE_ENCODING_AVIF:
            if (_gpuAV1Decode) {
                assert(false && "HARDWARE ENCODER AV1 IMPLEMENTATION NOT YET BUILT");
            } return DECOMPRESS_AVIF_CPU(info);
        case TILE_ENCODING_IRIS:
            assert(false && "IMPLEMENTATION NOT YET BUILT");
            break;
    } return Buffer();
}
} // END IRIS CODEC NAMESPACE
