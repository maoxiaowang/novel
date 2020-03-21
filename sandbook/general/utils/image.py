from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def process_user_avatar(avatar) -> InMemoryUploadedFile:
    """
    Process InMemoryUploadedFile
    return size: 256x256
    """

    im = Image.open(avatar)
    assert im.format.upper() in ('PNG', 'JPG', 'JPEG')

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    if width == height:
        region = im
    else:
        # (left, upper, right, lower)
        if width > height:
            delta = (width - height) / 2
            box = (delta, 0, delta + height, height)
        else:
            delta = (height - width) / 2
            box = (0, delta, width, delta + width)
        region = im.crop(box)

    a = region.resize((256, 256), Image.ANTIALIAS)  # anti-aliasing

    img_io = BytesIO()
    a.save(img_io, im.format)

    img_file = InMemoryUploadedFile(
        file=img_io,
        field_name=None,
        name=avatar.name,
        content_type=avatar.content_type,
        size=img_io.tell(),
        charset=None
    )
    return img_file


def process_novel_cover(cover):
    im = Image.open(cover)
    postfix = im.format.lower()
    assert postfix in ('png', 'jpg', 'jpeg')

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    # 1.414
    ratio = 1.414
    width, height = im.size
    if width * ratio == height:
        region = im
    else:
        # (left, upper, right, lower)
        if width * ratio > height:
            # 裁剪两边
            delta = (width * ratio - height) / 2  # 两边各减去多少
            box = (delta, 0, width - delta, height)
        else:
            # 上下裁剪
            delta = (height - width * ratio) / 2
            box = (0, delta, width, height - delta)
        region = im.crop(box)

    a = region.resize((210, 297), Image.ANTIALIAS)  # anti-aliasing

    img_io = BytesIO()
    a.save(img_io, im.format)

    img_file = InMemoryUploadedFile(
        file=img_io,
        field_name=None,
        name=cover.name,
        content_type=cover.content_type,
        size=img_io.tell(),
        charset=None
    )
    return img_file
