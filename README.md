## Mononobe Music

### Modules

- mononobe_api    The music source providers
- mononobe_cli    A simple cli client interface
- mononobe_core   The core part of "Mononobe Music"
- mononobe_music  The main collection package of all client interfaces

### CLI client

```bash
# Install dependencies by poetry
poetry install
# A simple search implement
mononobe-cli search -s netease 'yousa'
# A simple player based on libvlc // blocking
mononobe-cli play -s netease 1824222230
```
