'''
Factory object
==============

The factory can be used to automatically import any class from a module,
by specifying the module to import instead of the class instance.

The class list and available modules are automatically generated by setup.py.

Example for registering a class/module::

    >>> from kivy.factory import Factory
    >>> Factory.register('Widget', module='kivy.uix.widget')
    >>> Factory.register('Vector', module='kivy.vector')

Example of using the Factory::

    >>> from kivy.factory import Factory
    >>> widget = Factory.Widget(pos=(456,456))
    >>> vector = Factory.Vector(9, 2)

'''

__all__ = ('Factory', 'FactoryException')

from kivy.logger import Logger


class FactoryException(Exception):
    pass


class FactoryBase(object):

    def __init__(self):
        super(FactoryBase, self).__init__()
        self.classes = {}

    def register(self, classname, cls=None, module=None):
        '''Register a new classname refering to a real class or
           class definition in a module.
        '''
        if cls is None and module is None:
            raise ValueError('You must specify either cls= or module=')
        self.classes[classname] = {
            'module': module,
            'cls': cls}

    def __getattr__(self, name):
        classes = self.classes
        if name not in classes:
            raise FactoryException('Unknown class <%s>' % name)

        item = classes[name]
        cls = item['cls']

        # No class to return, import the module
        if cls is None:
            module = __import__(name=item['module'], fromlist='.')
            if not hasattr(module, name):
                raise FactoryException('No class named <%s> in module <%s>' % (
                    name, item['module']))
            cls = item['cls'] = getattr(module, name)

        return cls

    get = __getattr__


#: Factory instance to use for getting new classes
Factory = FactoryBase()

# Now import the file with all registers
# automatically generated by build_factory
import kivy.factory_registers
Logger.info('Factory: %d symbols loaded' % len(Factory.classes))

if __name__ == '__main__':
    Factory.register('Vector', module='kivy.vector')
    Factory.register('Widget', module='kivy.uix.widget')

