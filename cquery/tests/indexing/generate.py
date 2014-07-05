
import os
import random
import cquery


SEP = '/'

schemas = {
    'ROOT': 'content',
    'ASSETS': '$ROOT/assets',
    'SHOTS': '$ROOT/shots',
    'IMGSEQS': '$SHOT/images',
    'CACHESEQS': '$SHOT/cache',
    'VERSIONS': '$ASSET/public',
    'WORKSPACES': '$ASSET/private/$USER',
    'USER': ['marcus', 'nikki', 'lauda', 'liam']
}

classes = {
    'SHOT': 'Shot',
    'ASSET': 'Asset',
    'IMGSEQ': 'ImageSequence',
    'CACHESEQS': 'CacheSequence',
    'VERSION': 'Version',
    'WORKSPACE': 'Workspace'
}


def asset_name():
    assets = ['Peter', 'Mary', 'Spidey', 'Harry', 'Building',
              'Crane', 'Asfalt', 'City', 'Sky']
    return assets[random.randint(0, len(assets) - 1)]


def shot_name():
    return str(random.randint(1, 9)).ljust(4, "0")


def version_name():
    return "v" + str(random.randint(1, 200)).rjust(3, "0")


def random_name():
    s = "abcdef123"
    return ''.join(random.sample(s, len(s)))


def name_from_type(typ):
    return {'ASSETS': asset_name,
            'SHOTS': shot_name,
            'IMGSEQS': random_name,
            'CACHESEQS': random_name,
            'VERSIONS': version_name,
            'WORKSPACES': random_name,
            'USER': random_name}[typ]()


def resolve(schema):
    parts = schema.split(SEP)
    for part in parts:
        if part.startswith("$"):
            index = parts.index(part)
            schema = schemas[part[1:]]
            if isinstance(schema, list):
                schema = schema[random.randint(0, len(schema) - 1)]
            parts[index] = schema
    return SEP.join(parts)


def project(root,
            assets=10,
            subassets=0,
            shots=5,
            imgseqs=10,
            cacheseqs=5,
            versions=10,
            workspaces=20,
            cosmetics=2):

    """Generate a stub project at absolute path `root`

    Arguments:
        assets (int): Number of assets
        subassets (int): Number of subassets
        shots (int): Number of shots
        imgseqs (int): Number of image sequences
        cacheseqs (int): Number of cache sets
        versions (int): Number of versions
        cosmetics (int): Number of cosmetics directories

    """

    counts = (('ASSETS', assets),
              ('SHOTS', shots),
              ('IMGSEQS', imgseqs),
              ('CACHESEQS', cacheseqs),
              ('VERSIONS', versions),
              ('WORKSPACES', workspaces))

    for typ, count in counts:
        for index in xrange(count):
            name = name_from_type(typ)
            schema = schemas[typ]
            path = resolve(schema)
            path = SEP.join([path, name])

            typ_singular = typ[:-1]
            if not typ_singular in schemas:
                schemas[typ_singular] = list()

            count = 1
            unique_path = path + str(count)
            while unique_path in schemas[typ_singular]:
                count += 1
                unique_path = path + str(count)

            schemas[typ_singular].append(unique_path)

            fullpath = os.path.join(root, unique_path)
            normalised = os.path.normpath(fullpath)
            os.makedirs(normalised)

            cls = classes.get(typ_singular)
            if cls:
                cquery.tag(normalised, "." + cls)


if __name__ == '__main__':
    # project(root=r"c:\studio\content\jobs\test_large",
    #         assets=6000,
    #         subassets=0,
    #         shots=800,
    #         imgseqs=20000,
    #         cacheseqs=500,
    #         versions=800,
    #         workspaces=5000,
    #         cosmetics=2)

    project(root=r"c:\studio\content\jobs\test_small",
            assets=100,
            subassets=0,
            shots=10,
            imgseqs=20,
            cacheseqs=50,
            versions=80,
            workspaces=50,
            cosmetics=2)
