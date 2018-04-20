# Snarky Doorbell

Snarky Doorbell is an IoT doorbell with an attitude. Instead of a monotonic "ding-dong",
it responds with a snarky voice comment whenever our office doorbell is rung.

[![snarky-doorbell](https://raw.githubusercontent.com/anroots/snarky-doorbell/master/img/cover.jpg)](https://www.youtube.com/watch?v=ut_KckcVxW0)

Read a longer [blog post](https://sqroot.eu/2017/snarky-doorbell) on how this was built,
or watch a [project build video from YouTube](https://www.youtube.com/watch?v=ut_KckcVxW0).

## Features

- Several custom voice personals ("Easily excitable manager")
- Settings (voice, language, volume) can be changed via buttons on the front panel
- Built-in WiFi HTTP RESTful API server (statistics on doorbell rings)
- Open source project plans
- Non-intrusive integration with the existing doorbell system (uses the same doorbell button)

## Project Structure

- `ansible/` - Ansible playbook for installing and configuring the Raspberry "brain"
- `doc/` - Misc documentation files (voice persona lines)
- `firmware/` - Arduino firmware for the doorbell RF receiver module
- `hardware/` - Hardware schematics
- `src/` - Python daemon (doorbell controller) and webserver code for the Raspberry
- `wav/` - Doorbell ringtones

## Voices

The doorbell has "ringtones" of different voices and styles. Voice files are under `wav/voices`, split into three sub-folders:

- `english`
- `estonian`
- `system` (system speech, ie "volume maximum")

### Voice Actor Credits

Doorbell voices were graciously recorded by:

- Julian Linke
- Maarit Cimolonskas
- Harles Paesüld
- Tormi Tuuling
- Kaupo Toom
- Ken Kanarik
- Nele Sergejeva
- Ando Roots
- Maria Liiger
- Rauno Meronen
- Tanel Sirp
- Toivo Värbu

## License

Built with love and buckets of mischief by [Ando Roots](https://sqroot.eu).

This project (software, schematics and recorded voices) are licenced under
[Apache License 2.0 (Apache-2.0)](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0)).
