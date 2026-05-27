from imagekit.cachefiles import ImageCacheFile
from imagekit.registry import generator_registry


def image_url(field_file):
    if not field_file:
        return None
    try:
        return field_file.url
    except Exception:
        return None


def thumbnail_urls(field_file, specs):
    if not field_file:
        return {name: None for name in specs}

    urls = {}
    for name, spec_id in specs.items():
        try:
            generator = generator_registry.get(spec_id, source=field_file)
            urls[name] = ImageCacheFile(generator).url
        except Exception:
            urls[name] = None
    return urls


def generate_thumbnails(field_file, specs):
    for spec_id in specs.values():
        generator = generator_registry.get(spec_id, source=field_file)
        ImageCacheFile(generator).generate()


def delete_image_files(field_file, specs):
    if not field_file:
        return

    storage = field_file.storage
    names = [field_file.name]
    for spec_id in specs.values():
        try:
            generator = generator_registry.get(spec_id, source=field_file)
            names.append(ImageCacheFile(generator).name)
        except Exception:
            continue

    for name in names:
        if name and storage.exists(name):
            storage.delete(name)
