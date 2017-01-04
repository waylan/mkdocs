# MkDocs Plugins

A Guide to installing, using and creating MkDocs Plugins

---

## Installing Plugins.

Before a plugin can be used, it must be installed on the system. If you are
using a plugin which comes with MkDocs, then it was installed when you installed
MkDocs. However, to install third party plugins, you need to determine the
appropriate package name and install it using `pip`:

```python
pip install mkdocs-foo-plugin
```

Once a plugin has been successfully installed, it is ready to use. It just needs
to be [enabled](#using-plugins) in the configuration file.

## Using Plugins

The [`plugins`][config] configuration option should contain a list of plugins to
use when building the site. Each "plugin" must be a string name assigned to the
plugin (see the documentation for a given plugin to determine its "name"). A
plugin listed here must already be [installed](#installing-plugins).

```yaml
plugins:
    - search
```

Some plugins may provide configuration options of their own. If you would like
to set any configuration options, then you can nest a key/value mapping
(`option_name: option value`) of any options that a given plugin supports. Note
that a colon (`:`) must follow the plugin name and then on a new line the option
name and value must be indented and separated by a colon. If you would like to
define multiple options for a single plugin, each option must be defined on a
separate line.

```yaml
plugins:
    -search:
        lang: en
        foo: bar
```

For information regarding the configuration options available for a given plugin,
see that plugin's documentation.

## Developing Plugins

Like MkDocs, plugins must be written in Python. It is generally expected that
each plugin would be distributed as a separate Python module, although it is
possible to define multiple plugins in the same module. At a minimum, a MkDocs
Plugin must consist of a [`BasePlugin`](#baseplugin) subclass and an [entry
point](#entry-point) which points to it.

### BasePlugin

A subclass of `mkdocs.pluhgins.BasePlugin` should define the behavior of the plugin.
The class generally consists of actions to perform on specific events in the build
process as well as a configuration scheme for the plugin.

All `BasePlugin` subclasses contain the following attributes:

* __`config_scheme`__: a tuple of configuration validation class instances (to
  be defined in a subclass).
* __`config`__: a dictionary of configuration options set by the user (empty
  until `load_config` is called).

All `BasePlugin` subclasses contain the following method(s):

* __`load_config(options)`__: Loads configuration from a dictionary of options.
  Returns a tuple of `(errors, warnings)`.

* __`on_[event](...)`__: Optional methods which define the behavior for specific
  events. The plugin should define its behavior within these methods. The
  following events are supported:

    - `on_pre_nav`: TODO...
    
    - `on_post_nav`: TODO...
    
    - `on_post_config`: TODO...
    
    - `on_pre_build`: TODO...
    
    _ `on_pre_page`: TODO...
    
    - `on_pre_template`: TODO...
    
    - `on_post_page`: TODO...
    
    - `on_post_build`: TODO...
    
    - `on_serve`: TODO...

### Entry Point

TODO...

[config]: configuration.md#plugins