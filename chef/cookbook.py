from chef.base import ChefObject

class Cookbook(ChefObject):
    """A Chef cookbook object.

    >>> Cookbook.list(api=api)
        [cookbook list]

    >>> Cookbook('name').attr('recipes')
        json format recipe
    """

    url = '/cookbooks'
    attributes_list = []
    attributes = {
        'templates': list,
        'files': list,
        'chef_type': str,
        'name': str,
        'providers': list,
        'recipes': list,
        'libraries': list,
        'json_class': str,
        'frozen?': bool,
        'version': str,
        'cookbook_name': str,
        'attributes': list,
        'definitions': list,
        'root_files': list,
        'resources': list,
        'metadata': dict
    }

    def _attributes(self, version):
        attributes = self.attributes
        specs = self.api[self.url + '/' + version]
        for spec in specs.keys():
            if spec in attributes:
                attributes[spec] = specs[spec]
        return attributes

    def _populate(self, data):
        self.attributes_list = []
        for v in self.version(latest=False):
            self.attributes_list.append(self._attributes(self.version()))

    def attr(self, key=None, latest=True):
        attrs = []
        if not latest:
            for attr in self.attributes_list:
                try:
                    attrs.append(attr[key])
                except:
                    attrs.append(attr)
            return attrs
        else:
            try:
                attrs = self.attributes_list[0][key]
            except:
                attrs = self.attributes_list[0]
        return attrs

    def version(self, latest=True, api=None):
        api = api or self.api
        versions = '0' if latest else []
        for v in api[self.url][self.name]['versions']:
            if latest:
                if int(versions.replace('.','')) < int(v['version'].replace('.','')):
                    versions = v['version']
            else:
                versions.append(v['version'])
        return versions

    def recipes(self, version=None, api=None):
        api = api or self.api
        return api[self.url + '/' + self.version()]['recipes'] or []
