import shlex
import os
import tempfile
import stat
from .utils import get_config, get_command, register, get_command2, TaskError


def addargs(cmd, args):
    if args and "{}" not in cmd:
        raise TaskError(f"got argvs ({args}) but cmd (`{cmd}`) does not accept them")
    if not args and "{}" in cmd:
        raise TaskError(f"expecting argvs for cmd: `{cmd}`")
    return cmd.format(shlex.join(args))


@register
def venv(
    ctx,
    *,
    venv: "python requirements to install",
    cmd,
    python=None,
):
    cmd = addargs(cmd, ctx["args"])
    yield "uv"
    yield "run"
    yield "--no-project"
    if python:
        yield "--python"
        yield python
    pkgs = [i for i in venv.splitlines() if i]
    for pkg in pkgs:
        yield "--with"
        yield pkg
    yield "--"
    yield from shlex.split(cmd)


@register
def script(ctx, *, script):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(script)
    os.chmod(temp_file.name, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    yield temp_file.name
    for arg in ctx["args"]:
        yield arg


@register
def cmd(ctx, *, cmd):
    cmd = addargs(cmd, ctx["args"])
    yield from shlex.split(cmd)


@register
def shell(ctx, *, shell, shellcmd="sh -exc {} --"):
    for part in shlex.split(shellcmd):
        if part == "{}":
            yield shell
        else:
            yield part
    yield from ctx["args"]


def _docker(*, version="latest", image, image_port, user_port, envs):
    yield "docker"
    yield "run"
    if version is None:
        version = "latest"
    if user_port is None:
        user_port = image_port

    yield "-p"
    yield f"{image_port}:{user_port}"

    for env, env_val in envs.items():
        if env_val is not None:
            yield "-e"
            yield f"{env.upper()}={env_val}"

    yield f"{image}:{version}"


@register
def postgres(_, *, postgres, port=None, user=None, password=None, db=None, lang=None):
    return _docker(
        version=postgres,
        user_port=port,
        image="postgres",
        image_port=5432,
        envs={
            "POSTGRES_PASSWORD": password,
            "POSTGRES_USER": user,
            "POSTGRES_DB": db,
            "LANG": lang,
        },
    )


@register
def mysql(_, *, mysql, port=None, user=None, password=None, db=None, lang=None):
    return _docker(
        version=mysql,
        user_port=port,
        image="mysql",
        image_port=3306,
        envs={
            "MYSQL_PASSWORD": password,
            "MYSQL_USER": user,
            "MYSQL_DATABASE": db,
        },
    )


@register
def redis(_, *, redis, port=None):
    return _docker(
        version=redis,
        user_port=port,
        image="redis",
        image_port=6379,
        envs={},
    )


@register
def nix(ctx, *, nix, cmd="{}"):
    cmd = addargs(cmd, ctx["args"])
    yield "nix-shell"
    yield "--packages"
    yield from [i for i in nix.splitlines() if i]
    yield "--run"
    yield cmd


@register
def use(ctx, *, use, **kw):
    try:
        use = dict(get_config()[use])
    except KeyError:
        raise TaskError(f"use: no such task: {use}")
    return get_command2(ctx["section_name"], dict(use, **kw), ctx["args"])


# @register
# def env(section_name, *, env, **kw):
#     kw["cmd"] = f"env {' '.join()} {kw['cmd']}"
#     return get_command2(section_name, kw)


@register
def assert_cmd(ctx, **kw):
    assert_cmd = kw.pop("assert_cmd")
    try:
        cmd = get_command2(ctx["section_name"], kw, ctx["args"])
    except TaskError as exc:
        assert 0, exc.args[0]
    cmd_str = shlex.join(cmd)
    if cmd_str != assert_cmd:
        raise TaskError(
            f"assert failed at {ctx['section_name']}:\nexpected: {assert_cmd}\nactual:   {cmd_str}"
        )
    yield "true"


@register
def assert_err(ctx, **kw):
    assert_err = kw.pop("assert_err")
    try:
        get_command2(ctx["section_name"], kw, ctx["args"])
    except TaskError as exc:
        if assert_err.upper() not in exc.args[0].upper():
            raise TaskError(
                (
                    f"{ctx['section_name']}: assert failed - "
                    f"{repr(assert_err)} not in {repr(exc.args[0])}"
                )
            )
        yield "true"
    else:
        raise TaskError(f"{ctx['section_name']}: assert failed - no error")


@register
def help(ctx, *, help=None, **kw):
    print(help)
    print()
    print("Subcommands:")
    max_key = max(len(i) for i in kw.keys())
    for key, val in kw.items():
        print(key.ljust(max_key + 2), val)
    yield "true"


@register
def env(ctx, *, env=None, **kw):
    yield "env"
    for key, val in kw.items():
        yield f"{key}={val}"
    yield from ctx["args"]


@register
def getcmd(ctx, *, getcmd=None):
    args = list(ctx["args"])
    cmd = args.pop(0)
    yield "echo"
    yield shlex.join(get_command(cmd, args))


@register
def services(ctx, *, services):
    import json

    services = [i for i in services.splitlines() if i]
    config = {"version": "0.5", "processes": {}}
    for service in services:
        cmd = get_command(service, ctx["args"])
        config["processes"][service] = {"command": shlex.join(cmd)}
    source = json.dumps(config)
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(source)
    yield "process-compose"
    yield "--config"
    yield temp_file.name
