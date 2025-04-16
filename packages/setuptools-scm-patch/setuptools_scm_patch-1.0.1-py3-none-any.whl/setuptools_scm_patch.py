def simple_version_scheme(version):
    parts = str(version.tag).split('.') + ['0', '0', '0']
    parts[2] = str(int(parts[2]) + (version.distance or 0))
    return '.'.join(parts[:3])
