### Base Plugin

``` python
import config
from plugins.pluginbase import PluginBase

class Name(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'name'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        pass
```

### Add to bot.py

```
# Add to imports
from plugins import ___,___,___,name
# Add to bottom
plugins.append(name.Name(bot))
```