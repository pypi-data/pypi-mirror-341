from netbox.plugins import PluginTemplateExtension

class CableExtensionTemplateExtension(PluginTemplateExtension):
    models = ['dcim.cable']

    def right_page(self):
        cable = self.context['object']
        extension = getattr(cable, 'extension', None)
        if not extension:
            return ""

        return self.render('cable_extension/cable_extension_panel.html', {
            'extension': extension
        })

template_extensions = [CableExtensionTemplateExtension]
