# ovos-PHAL-plugin - respeaker 2 mic

ported from https://github.com/JarbasHiveMind/HiveMind-PTT/commit/231d6a51761bb1e929d1456e799da0635a77a990

warning: contain GPL dependencies

TODO - universal donor policy does not allow GPL deps, exception for this repo ?

# Usage

By default, this plugin uses [ovos-i2csound](https://github.com/OpenVoiceOS/ovos-i2csound) to create a file called `i2c_platform` in `~/.config/mycroft`.  If you are not using ovos-i2csound, you need to create that file, or point to another file in your `~/.config/mycroft/mycroft.conf`

The file should contain a single line with the value `wm8960`

You can specify the location of the file in `~/.config/mycroft/mycroft.conf` by adding

```json
{
    "PHAL": {
        "ovos-PHAL-plugin-respeaker-2mic": {
            "i2c_platform": "full/path/to/your/file"
        }
    }
}
```
