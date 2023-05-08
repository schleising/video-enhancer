from typing import Optional
from pydantic import BaseModel

class Disposition(BaseModel):
    default: int
    dub: int
    original: int
    comment: int
    lyrics: int
    karaoke: int
    forced: int
    hearing_impaired: int
    visual_impaired: int
    clean_effects: int
    attached_pic: int
    timed_thumbnails: int
    captions: int
    descriptions: int
    metadata: int
    dependent: int
    still_image: int

class Tags(BaseModel):
    language: str
    handler_name: str
    vendor_id: str
    encoder: Optional[str] = None

class Stream(BaseModel):
    index: int
    codec_name: str
    codec_long_name: str
    profile: str
    codec_type: str
    codec_tag_string: str
    codec_tag: str
    width: Optional[int] = None
    height: Optional[int] = None
    coded_width: Optional[int] = None
    coded_height: Optional[int] = None
    closed_captions: Optional[int] = None
    film_grain: Optional[int] = None
    has_b_frames: Optional[int] = None
    pix_fmt: Optional[str] = None
    level: Optional[int] = None
    color_range: Optional[str] = None
    color_space: Optional[str] = None
    color_transfer: Optional[str] = None
    color_primaries: Optional[str] = None
    chroma_location: Optional[str] = None
    field_order: Optional[str] = None
    refs: Optional[int] = None
    is_avc: Optional[bool] = None
    nal_length_size: Optional[str] = None
    id: str
    r_frame_rate: str
    avg_frame_rate: str
    time_base: str
    start_pts: int
    start_time: str
    duration_ts: int
    duration: float
    bit_rate: int
    bits_per_raw_sample: Optional[int] = None
    nb_frames: int
    extradata_size: int
    disposition: Disposition
    tags: Tags
    sample_fmt: Optional[str] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    channel_layout: Optional[str] = None
    bits_per_sample: Optional[int] = None
    initial_padding: Optional[int] = None

class Tags1(BaseModel):
    major_brand: str
    minor_version: str
    compatible_brands: str
    encoder: str

class Format(BaseModel):
    filename: str
    nb_streams: int
    nb_programs: int
    format_name: str
    format_long_name: str
    start_time: float
    duration: float
    size: int
    bit_rate: int
    probe_score: int
    tags: Tags1

class VideoInformation(BaseModel):
    streams: list[Stream]
    format: Format
