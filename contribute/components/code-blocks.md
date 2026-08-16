---
description: components and formatting examples used in Kleene's docs
title: Code blocks
toc_max: 3
---

# Code blocks

Rouge provides lots of different code block "hints". If you leave off the hint,
it tries to guess and sometimes gets it wrong. These are just a few hints that
we use often.

## Raw

Use the {% raw %}`{% raw %}`{% endraw %} markup tag to prevent Liquid from interpreting double
braces as templating language.

{% raw %}
````
{​% raw %}
```none
generic code block without syntax highlighting
$ some command with {{double braces}}
$ some other command
```
{​% endraw %}
````
{% endraw %}

## Bash

Use the `bash` language code block when you want to a Bash script:

```bash
#!/usr/bin/bash
pkg install -y kleene-daemon kleene-cli
```

If you want to illustrate an interactive shell, use `console` instead.
In cases where you use `console`, make sure to add a dollar character
for the user sign:

```console
$ sudo pkg install -y kleene-daemon kleene-cli
```

## Go

```go
incoming := map[string]interface{}{
    "asdf": 1,
    "qwer": []interface{}{},
    "zxcv": []interface{}{
        map[string]interface{}{},
        true,
        int(1e9),
        "tyui",
    },
}
```

## PowerShell

```powershell
$config = Get-Content -Path kleened_config.yaml
[System.Environment]::SetEnvironmentVariable("KLEENE_HOST", "10.0.0.1", "Machine")
Expand-Archive klee-0.1.0.zip -DestinationPath $Env:ProgramFiles -Force
```

## Python

```python
return html.format(name=os.getenv('NAME', "world"), hostname=socket.gethostname(), visits=visits)
```

## Ruby

```ruby
module Jekyll
  class RenderTimeTag < Liquid::Tag
    def render(context)
      "#{context.registers[:site].time}"
    end
  end
end
```

## JSON

```json
"server": {
  "address": "https://127.0.0.1:8085",
  "tls_key_file": "/usr/local/etc/kleened/certs/server-key.pem",
  "tls_cert_file": "/usr/local/etc/kleened/certs/server-cert.pem"
}
```

#### HTML

```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
</head>
</html>
```

## Markdown

```markdown
# Hello
```

If you want to include a triple-fenced code block inside your code block,
you can wrap your block in a quadruple-fenced code block:

`````markdown
````markdown
# Hello

```go
log.Println("did something")
```
````
`````

## ini

```ini
[supervisord]
nodaemon=true

[program:sshd]
command=/usr/sbin/sshd -D
```

## Dockerfile

```dockerfile
FROM FreeBSD-13.2-RELEASE:latest

RUN pkg install -y postgresql15-server

ENV PGDATA=/var/db/postgres/data15

USER postgres

RUN /usr/local/bin/initdb -D ${PGDATA} && \
    echo "host all all 0.0.0.0/0 md5" >> ${PGDATA}/pg_hba.conf && \
    echo "listen_addresses='*'" >> ${PGDATA}/postgresql.conf

CMD ["/usr/local/bin/postgres", "-D", "/var/db/postgres/data15"]
```

## YAML

```yaml
kleene_root: "zroot/kleene"
pf_config_template_path: "/usr/local/etc/kleened/pf.conf.kleene"
pf_config_path: "/etc/pf.conf"
api_listening_sockets:
  - address: "http:///var/run/kleened.sock"
enable_logging: true
log_level: "info"
```
